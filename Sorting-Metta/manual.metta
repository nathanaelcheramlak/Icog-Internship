;; list type structure to - defined as recursive data structure
;; the Cons and Nil are conventinally used to define the recursive data struture but do not have special meaning

(Cons 1 (Cons 2 Nil))
;; We can define the type for the above data structure as follows 
;; Since Nil points the end of the list -- it has to be defined as a List it self -- list of some type
(: List (-> $a Type))
(: Nil (List $a))
(: Cons (-> $a (List $a) (List $a)))

;; so, anything that is wrapped in the Cons type maker(constructor) will qualify as (List $a) type
;; if $a is a number -- and 
; ! (get-type (Cons 0 (Cons 1 Nil))) ;; (List Number)
; ! (get-atoms &self)
;; We can also construct list of anything by making custom type constructors from grounded types

(: Size Type)
;; next dedine a type constructor that takes a number and returns Size type
(: mkSize (-> Number Size))

;; now if we build a list that takes Size type arguments as follows
(Cons (mkSize 1) (Cons (mkSize 2) Nil))
;; The type of the above should be (List Size)
; ! (get-type (Cons (mkSize 1) (Cons (mkSize 2) Nil))) ;; (List Size)

;; when defining functions that take these types as argument we do it as follows
(: len (-> (List Number) Number)) ;; for list of numbers
;; for list of Size -- by overloading the above type definition 
(: len (-> (List Size) Number))
(= (len Nil) 0)
(= (len (Cons $x $xs))
    (+ 1 (len $xs)))
; ! (len (Cons 1 (Cons 3 Nil))) ;; 2
; ! (len (Cons (mkSize 1) (Cons (mkSize 3) Nil))) ;; 2

;; An instance is just a vector of numbers
(: Instance Type)
(: mkInst (-> (List Number) Instance))

;; to make an Instance Type use the type constructor, mkInst, and pass it List of numbers
; ! (mkInst (Cons 5 (Cons 4 Nil)));; this is a valid Instance 
;; to verify that 
; ! (get-type (mkInst (Cons 5 (Cons 4 Nil))))
;; A scored instance is just a pair of instance and it's score.

;; A pair type definition
(: Pair (-> $a $b Type))
(: mkPair (-> $a $b (Pair $a $b)))

;; ScoredInstance -- takes a the type of the score -- because we can have different kinds of scores -- 
;; just like the list -- we can have list of numbers as well as other types

;; a scored instance which is represented here with ScoredInstance can be constructed using the mkSInst type maker
(: ScoredInstance (-> $score Type))
(: mkSInst (-> (Pair Instance $score) (ScoredInstance $score)))

;; a valid scored instance is sth like this
;; first lets define a score type
(: Cscore Type)
(: mkCscore (-> Number Number Cscore))

;; scored instance
; ! (mkSInst (mkPair (mkInst (Cons 1 Nil)) (mkCscore 1 2)))
; ! (get-type (mkSInst (mkPair (mkInst (Cons 1 Nil)) (mkCscore 1 2)))) ;; (ScoredInstance Cscore)
;; An instance set is a list of scored instances.

;; a scored instance set is a list of scored instances 
(: InstanceSet (-> $score Type))
(: mkSInstSet (-> (List (ScoredInstance $score)) (InstanceSet $score)))

;; a sample instance set is with just two scored instances 
; ! (mkSInstSet (Cons (mkSInst (mkPair (mkInst (Cons 1 Nil)) (mkCscore 1 2))) (Cons (mkSInst (mkPair (mkInst (Cons 2 Nil)) (mkCscore 2 3))) Nil)))
; ! (get-type (mkSInstSet (Cons (mkSInst (mkPair (mkInst (Cons 1 Nil)) (mkCscore 1 2))) (Cons (mkSInst (mkPair (Cons 2 Nil)) (mkCscore 2 3))) Nil))) ;; (InstanceSet Cscore)

;; So the task is to implement sorting algorithms for sored instance set in metta using the 2nd part of the Cscore value
;; Partial sort as well as full sort -- select two algorithms implement them and comparet the time complexity -- theorerical and time metta execution time

;; whenever possible, make use of builtin functions for speed of execution (mkInst)

;; Helper functions to access Cscore components
(: cscore-1 (-> Cscore Number))
(= (cscore-1 (mkCscore $x $y)) $x)

(: cscore-2 (-> Cscore Number))
(= (cscore-2 (mkCscore $x $y)) $y)

;; Helper to get the score from a ScoredInstance
(: get-score (-> (ScoredInstance $s) $s))
(= (get-score (mkSInst (mkPair $inst $score))) $score)

;; Helper to get the instance from a ScoredInstance
(: get-inst (-> (ScoredInstance $s) Instance))
(= (get-inst (mkSInst (mkPair $inst $score))) $inst)

;; Compare two ScoredInstances based on the second part of their Cscore
(: compare-sinst (-> (ScoredInstance Cscore) (ScoredInstance Cscore) Bool))
(= (compare-sinst $a $b)
   (> (cscore-2 (get-score $a)) (cscore-2 (get-score $b))))


;; Quicksort implementation for InstanceSet
(: quicksort (-> (InstanceSet Cscore) (InstanceSet Cscore)))
(= (quicksort (mkSInstSet Nil)) (mkSInstSet Nil))
(= (quicksort (mkSInstSet (Cons $pivot $rest)))
   (let* (($pivot-score (get-score $pivot))
         ($left (filter (lambda ($x) (< (cscore-2 (get-score $x)) 
                                       (cscore-2 $pivot-score))) $rest))
         ($right (filter (lambda ($x) (>= (cscore-2 (get-score $x)) 
                                        (cscore-2 $pivot-score))) $rest))
         ($sorted-left (quicksort (mkSInstSet $left)))
         ($sorted-right (quicksort (mkSInstSet $right))))
     (mkSInstSet (concat $sorted-left (Cons $pivot $sorted-right)))))

;; Partial sort to get top k elements
(: top-k (-> Number (InstanceSet Cscore) (InstanceSet Cscore)))
(= (top-k 0 $_) (mkSInstSet Nil))
(= (top-k $k (mkSInstSet Nil)) (mkSInstSet Nil))
(= (top-k $k (mkSInstSet $lst))
   (let* (($max (find-max $lst))
         ($rest (remove $max $lst)))
     (if (> $k 0)
         (mkSInstSet (Cons $max (top-k (- $k 1) (mkSInstSet $rest))))
         (mkSInstSet Nil))))

;; Helper to find the maximum element
(: find-max (-> (List (ScoredInstance Cscore)) (ScoredInstance Cscore)))
(= (find-max (Cons $x Nil)) $x)
(= (find-max (Cons $x $xs))
   (let (($max-rest (find-max $xs)))
     (if (compare-sinst $x $max-rest) $x $max-rest)))

;; Helper to remove an element from a list
(: remove (-> (ScoredInstance Cscore) (List (ScoredInstance Cscore)) 
              (List (ScoredInstance Cscore))))
(= (remove $x Nil) Nil)
(= (remove $x (Cons $y $ys))
   (if (equal? $x $y)
       $ys
       (Cons $y (remove $x $ys))))


;; Create a sample instance set
(: test-set (InstanceSet Cscore))
(= test-set 
   (mkSInstSet 
    (Cons (mkSInst (mkPair (mkInst (Cons 1 Nil)) (mkCscore 1 5))
    (Cons (mkSInst (mkPair (mkInst (Cons 2 Nil)) (mkCscore 2 3))
    (Cons (mkSInst (mkPair (mkInst (Cons 3 Nil)) (mkCscore 3 8))
    (Cons (mkSInst (mkPair (mkInst (Cons 4 Nil)) (mkCscore 4 1))
    (Cons (mkSInst (mkPair (mkInst (Cons 5 Nil)) (mkCscore 5 6)) Nil))))))))))))

;; Time the operations
! (quicksort test-set)  ;; Measure time for full sort
! (top-k 3 test-set)    ;; Measure time for partial sort



;; Redefine the helper functions with more precise type matching

;; Helper to get the inner list from an InstanceSet
(: get-sinst-list (-> (InstanceSet $s) (List (ScoredInstance $s))))
(= (get-sinst-list (mkSInstSet $lst)) $lst)

;; Revised quicksort with proper type handling
(: quicksort (-> (InstanceSet Cscore) (InstanceSet Cscore)))
(= (quicksort (mkSInstSet Nil)) (mkSInstSet Nil))
(= (quicksort (mkSInstSet (Cons $pivot $rest)))
   (let* (($pivot-score (get-score $pivot))
          ($left (filter (lambda ($x) (< (cscore-2 (get-score $x)) 
                                        (cscore-2 $pivot-score))) $rest))
          ($right (filter (lambda ($x) (>= (cscore-2 (get-score $x)) 
                                         (cscore-2 $pivot-score))) $rest))
     (mkSInstSet (concat (get-sinst-list (quicksort (mkSInstSet $left)))
                         (Cons $pivot 
                               (get-sinst-list (quicksort (mkSInstSet $right)))))))))

;; Revised top-k with better output
(: top-k (-> Number (InstanceSet Cscore) (InstanceSet Cscore)))
(= (top-k $k (mkSInstSet Nil)) (mkSInstSet Nil))
(= (top-k $k (mkSInstSet $lst))
   (if (<= $k 0) 
       (mkSInstSet Nil)
       (let* (($max (find-max $lst))
             ($rest (remove $max $lst)))
         (mkSInstSet (Cons $max 
                           (get-sinst-list (top-k (- $k 1) (mkSInstSet $rest))))))))

;; Create a more visible test set
(: test-set (InstanceSet Cscore))
(= test-set 
   (mkSInstSet 
    (Cons (mkSInst (mkPair (mkInst (Cons 1 Nil)) (mkCscore 1 5))
    (Cons (mkSInst (mkPair (mkInst (Cons 2 Nil)) (mkCscore 2 3))
    (Cons (mkSInst (mkPair (mkInst (Cons 3 Nil)) (mkCscore 3 8))
    (Cons (mkSInst (mkPair (mkInst (Cons 4 Nil)) (mkCscore 4 1))
    (Cons (mkSInst (mkPair (mkInst (Cons 5 Nil)) (mkCscore 5 6)) Nil))))))))))))

;; Add a function to visualize the output
(: show-sinst (-> (ScoredInstance Cscore) String))
(= (show-sinst (mkSInst (mkPair $inst (mkCscore $a $b)))) 
   (concat "(Score: " (toString $a) " " (toString $b) ")"))

(: show-instset (-> (InstanceSet Cscore) (List String)))
(= (show-instset (mkSInstSet Nil)) Nil)
(= (show-instset (mkSInstSet (Cons $x $xs))) 
   (Cons (show-sinst $x) (show-instset (mkSInstSet $xs))))

;; Now test with visible output
! (show-instset (quicksort test-set))
! (show-instset (top-k 3 test-set))