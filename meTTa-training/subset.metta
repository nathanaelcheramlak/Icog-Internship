; Generate all subsets (the power set) of a given list.

; Recursive helper
(: helper (-> Expression Number Expression Expression Expression))
(= (helper $list $index $acc $current)
    (if (== $index (size-atom $list))
        (cons-atom $current $acc)                    
        (let* (
            ($new-index (+ $index 1))
            ; no pick branch
            ($acc1 (helper $list $new-index $acc $current))
            ; pick branch
            ($element (index-atom $list $index))
            ($new-current (union-atom $current ($element)))
            ($acc2 (helper $list $new-index $acc1 $new-current))
        ) $acc2)
    )
)

(: subset (-> Expression Expression))
(= (subset $list) (
    if (== $list ())
        ()
        (helper $list 0 () ())
))

;; Test
!(subset (1 2 3))
!(subset ())
!(subset (a b))
; !(subset (1 a 2 b 3))
