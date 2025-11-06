;; Calculate weighted sum down one column of selected solutions
;; Variables:
;;  $weights: recombination weights w
;;  $matrix: selected solutions matrix (μ x dim)
;;  $rowIdx: current row index (parent index)
;;  $colIdx: feature (dimension) index
(= (calculate-col-weight () $matrix $rowIdx $) 0)
(= (calculate-col-weight $weights $matrix $rowIdx $colIdx) (
    let* (
        (($curr-weight $rest-weights) (decons-atom $weights))
        ($value (getMatrixValue $matrix $rowIdx $colIdx))
        ($calculated-val (* $value $curr-weight))
        ($total (calculate-col-weight $rest-weights $matrix (+ $rowIdx 1) $colIdx))
    ) (+ $calculated-val $total)
))

;; Build mean vector by aggregating weighted columns
;; Variables: see above; $colIdx is processed from right to left
(= (update-mean-helper $selected-solutions $recombination-weights $colIdx) (
    if (== $colIdx -1) 
        () 
        (let* (
            ($weighted-sum (calculate-col-weight $recombination-weights $selected-solutions 0 $colIdx))
            ($total (update-mean-helper $selected-solutions $recombination-weights (- $colIdx 1)))
        ) (cons-atom $weighted-sum $total))
))

;; Public entry: compute new mean vector from selected solutions and weights
(= (update-mean $selected-solutions $recombination-weights) (
    let* (
        ($colCount (size-atom $recombination-weights))
        ($colIdx (- $colCount 1))
        ($reversed-mean (update-mean-helper $selected-solutions $recombination-weights $colIdx))
        ($new-mean (reverse $reversed-mean ()))
    ) $new-mean
))