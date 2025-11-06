(= (calculate-col-weight () $matrix $rowIdx $) 0)
(= (calculate-col-weight $weights $matrix $rowIdx $colIdx) (
    let* (
        (($curr-weight $rest-weights) (decons-atom $weights))
        ($value (getMatrixValue $matrix $rowIdx $colIdx))
        ($calculated-val (* $value $curr-weight))
        ($total (calculate-col-weight $rest-weights $matrix (+ $rowIdx 1) $colIdx))
    ) (+ $calculated-val $total)
))

(= (update-mean-helper $selected-solutions $recombination-weights $colIdx) (
    if (== $colIdx -1) 
        () 
        (let* (
            ($weighted-sum (calculate-col-weight $recombination-weights $selected-solutions 0 $colIdx))
            ($total (update-mean-helper $selected-solutions $recombination-weights (- $colIdx 1)))
        ) (cons-atom $weighted-sum $total))
))

(= (update-mean $selected-solutions $recombination-weights) (
    let* (
        ($colCount (size-atom $recombination-weights))
        ($colIdx (- $colCount 1))
        ($reversed-mean (update-mean-helper $selected-solutions $recombination-weights $colIdx))
        ($new-mean (reverse $reversed-mean ()))
    ) $new-mean
))


!(update-mean ((1 2 3) (4 5 6)) (0.6 0.4))