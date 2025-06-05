(= (replace () $x $y) ())
(= (replace (:: $curr-item $the-rest) $index $num) (
    let* (
        ; ($curr-item (car-atom $list))
        ; ($the-rest (cdr-atom $list))
        ($concat (replace $the-rest (- $index 1) $num))
    )
    (if (== $index 0)
        (cons-atom $num $concat)
        (cons-atom $curr-item $concat)
    )
))

(= (get-max $x $y) (
    if (>= $x $y)
        $x
        $y
))

(= (get-index () $num) ())
(= (get-index (:: $x $xs) $num) (
    if (== $x $num)
        0
        (+ (get-index $xs $num) 1)
))

; !(get-index (:: 1 (:: 2 (:: 5 (:: 3 ())))) 5)


(= (get-element () $index) ())
(= (get-element (:: $x $xs) $index) (
    if (== $index 0)
        $x
        (get-element $xs (- $index 1))
))

; !(get-element (:: 10 (:: 2 (:: 5 (:: 3 ())))) 0)

; (= (find-replace () $old $new) ())
; (= (find-replace (:: $x $xs) $old $new) (
;     (let* ($processed (find-replace $xs $old $new)))
;     (if (== $x $old)
;         (cons-atom $new $processed)
;         (cons-atom $x $processed)
;     )
; ))

(= (find-replace () $old $new) ())
(= (find-replace (cons $x $xs) $old $new) (
    (if (== $x $old)
        (cons $new (find-replace $xs $old $new))
        (cons $x (find-replace $xs $old $new))
    )
))

; Tests
!(find-replace (:: 1 (:: 2 (:: 5 (:: 3 ())))) 5 12)      ; Expect (9 2 3 9)
; !(find-replace a z (a b a c))      ; Expect (z b z c)
; !(find-replace x y ())             ; Expect ()
; !(find-replace you we (how are you)) ; Expect (how are we)

(= (swap () $x $y) ())
(= (swap (:: $x $xs) $xind $yind ) (
    (let* ($curr-item))
    if (== $yind 0)
        ()
))

; !(swap (1 2 3 4 5) 0 1)




; (= (remove $rm ()) ())
; (= (remove $rm (:: $x $xs))
;     (if (== $rm $x)
;         (remove $rm $xs)
;         (:: $x (remove $rm $xs))
;     )
; )
; ! (remove 2 (:: 1 (:: 2 (:: 5 (:: 3 ())))))

(= (append $y ()) (:: $y))
(= (append $y (:: $x $xs))
    (:: $x (append $y $xs))
)

! (append 3 (:: 1 (:: 2 ())))



; Replaces all occurrences of $old with $new in a list
; Base case: empty list
(= (find_and_replace $old $new ()) ())

(= (find_and_replace $old $new $list)
  (let* (
    (($head $tail) (decons-atom $list))
    ; process remaining elements recursively
    ($processed_tail (find_and_replace $old $new $tail))
  )
    (if (== $head $old)
        ; replace matched element if found
        (cons-atom $new $processed_tail)
        ; else keep original element
        (cons-atom $head $processed_tail))
  )
)

; Tests
!(find_and_replace 1 9 (1 2 3 1))      ; Expect (9 2 3 9)
!(find_and_replace a z (a b a c))      ; Expect (z b z c)
!(find_and_replace x y ())             ; Expect ()
!(find_and_replace you we (how are you)) ; Expect (how are we)



! (bind! toInt (py-atom int))

(= (selectSort $list $n $op)
    (if (== $n 0)
        $list
     (let* (
        ($fn (if (== $op <) min-atom max-atom))
        ($cur (toInt ($fn $list)))
        ($newList (subtraction-atom $list ($cur)))
        ($rest (selectSort $newList (- $n 1) $op))
    
    (cons-atom $cur $rest)
    ))
))

! (selectSort (4 5 8 9 3 2 1 6 7) 9 <)
