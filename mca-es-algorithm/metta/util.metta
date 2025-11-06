(= (getMatrixValue $matrix $rowIdx $colIdx) (
    let $row (index-atom $matrix $rowIdx) (index-atom $row $colIdx)
))

(= (sqrt $x) (
    (py-atom math.sqrt) $x
))

(= (exp $x) (
    (py-atom math.exp) $x
))

(=(reverse $list $acc) (
    if(== $list ()) 
      $acc
      (let ($head $tail ) (decons-atom $list) (reverse $tail (cons-atom $head $acc) ))
))

(= (sum ()) 0)
(= (sum $list) (
    let* (
        (($head $tail) (decons-atom $list))
        ($total (sum $tail))
    ) (+ $head $total)
))