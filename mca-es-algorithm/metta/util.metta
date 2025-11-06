;; Access value at rowIdx, colIdx from a matrix represented as list-of-lists
;; $matrix: matrix, $rowIdx: row, $colIdx: column
(= (getMatrixValue $matrix $rowIdx $colIdx) (
    let $row (index-atom $matrix $rowIdx) (index-atom $row $colIdx)
))

;; Square root via Python binding
;; $x: numeric value
(= (sqrt $x) (
    (py-atom math.sqrt) $x
))

;; Exponential via Python binding
;; $x: numeric value
(= (exp $x) (
    (py-atom math.exp) $x
))

;; Reverse a list using accumulator
;; $list: input list, $acc: accumulator
(=(reverse $list $acc) (
    if(== $list ()) 
      $acc
      (let ($head $tail ) (decons-atom $list) (reverse $tail (cons-atom $head $acc) ))
))

;; Sum of a list of numbers
(= (sum ()) 0)
(= (sum $list) (
    let* (
        (($head $tail) (decons-atom $list))
        ($total (sum $tail))
    ) (+ $head $total)
))