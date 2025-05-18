; Functions
(=(h) helloworld)
!(h)

;Add Numbers
(= (add_two_nums $x $y) (+ $x $y))
!(add_two_nums 5 21)

; Basic Recurrsion
(= (count_length ()) 0)
(= (count_length (:: $letter $next)) (+ 1 (count_length $next)))

!(count_length (:: A (:: B (:: C ()) )))


; Apply Twice
(= (apply-twice $function $num) (square ($function $num)))
(= (square $x) (* $x $x))

!(apply-twice square 4)


; Factorial Calculation
(= (factorial $num) 
    (if (> $num 0) 
        (* $num (factorial (- $num 1))) 
        1
    )
)

!(factorial 5)

; Recursive Summation
(= (add_nums $num) (
    if (== $num 0) 0 (+ $num (add_nums (- $num 1)))
))

!(add_nums 10)


; Check Ones
(= (check_one $expression) (
    if (== $expression 1) 1 0
))

; Count Ones
(= (count_ones ()) 0)
(= (count_ones $expression) (
    let $sum (+ (check_one (car-atom $expression)) (count_ones (cdr-atom $expression)))
    $sum
))

!(count_ones (1 0 1 3 1 1))



(Parent Bob Ann)
; This match will be successful
! (match &self (Parent Bob Ann) (Bob is Ann`s father))
; The following line will return []
! (match &self (Parent Bob Joe) (Bob is Joe`s father))

; Swap Characters
(= (swap $x $y) ($y $x))
!(swap 5 3)


;Learn Let

!(let $x (let $y 5 $y) $x)
!($x)

(A B)
(A c)
!(let $x (match &self (A $next) ($next)) $x)