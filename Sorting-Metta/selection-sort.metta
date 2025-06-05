; Bind 'toInt' to convert atoms to integers
! (bind! toInt (py-atom int))

; Selection sort implementation
(= (selectSort $list $n $op)
    (if (== $n 0)
        $list
        (let* (
            ; Choose min or max
            ($fn (if (== $op <) min-atom max-atom))
            ($cur (toInt ($fn $list)))
            ($newList (subtraction-atom $list ($cur)))
            ($rest (selectSort $newList (- $n 1) $op)))
            (cons-atom $cur $rest)
        )
    )
)

; Example usage
! (selectSort (3 1 4 7 0 5 2) 7 >)