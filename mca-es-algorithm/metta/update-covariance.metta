;; Compute one column of the delta_mean matrix
;; computes normalized deviations of selected parents
(= (calculate-col $selected-solutions $previous-mean $step-size $i $j) (
    if (== $j 5)
        ()
        (let* (
            ($value (getMatrixValue $selected-solutions $j $i))
            ($prev-mean-val (index-atom $previous-mean $j))
            ($res (/ (- $value $prev-mean-val) $step-size))
            ($rest (calculate-col $selected-solutions $previous-mean $step-size $i (+ 1 $j)))
        ) (cons-atom $res $rest))
))

;; captures momentum of evolution path
(= (calculate-delta-mean-helper $selected-solutions $previous-mean $step-size $i) (
    if (== $i (size-atom $selected-solutions))
        ()
        (let* (
            ($col (calculate-col $selected-solutions $previous-mean $step-size $i 0))
            ($rest (calculate-delta-mean-helper $selected-solutions $previous-mean $step-size (+ 1 $i)))
        ) (cons-atom $col $rest))
))

(= (calculate-delta-mean $selected-solutions $previous-mean $step-size) (
    calculate-delta-mean-helper $selected-solutions $previous-mean $step-size 0
))

(= (rank-one-row $vector $i $j)
    (if (== $j (size-atom $vector))
        ()
        (let* (
            ($vi (index-atom $vector $i))
            ($vj (index-atom $vector $j))
            ($prod (* $vi $vj))
            ($rest (rank-one-row $vector $i (+ 1 $j)))
        )
        (cons-atom $prod $rest)))
)

(= (rank-one-update-helper $vector $i)
    (if (== $i (size-atom $vector))
        ()
        (let* (
            ($row (rank-one-row $vector $i 0))
            ($rest (rank-one-update-helper $vector (+ 1 $i)))
        )
        (cons-atom $row $rest)))
)

(= (rank-one-update $vector)
    (rank-one-update-helper $vector 0)
)

(= (rankMuUpdater'' $recombination-weights $delta-mean $i $j $k $num-selected) (
    if (== $k $num-selected)
        0
        (let* (
            ($weight-val (index-atom $recombination-weights $k))
            ($delta-i (getMatrixValue $delta-mean $k $i))
            ($delta-k (getMatrixValue $delta-mean $k $j))
            ($res (* (* $weight-val $delta-i) $delta-k))
            ($rest (rankMuUpdater'' $recombination-weights $delta-mean $i $j (+ 1 $k) $num-selected))
        ) (+ $rest $res))
))

(= (rankMuUpdater' $recombination-weights $delta-mean $i $j $num-selected) (
    if (== $j 5)
        ()
        (let* (
            ($val (rankMuUpdater'' $recombination-weights $delta-mean $i $j 0 $num-selected))
            ($rest (rankMuUpdater' $recombination-weights $delta-mean $i (+ 1 $j) $num-selected))
        ) (cons-atom $val $rest))
))

(= (rankMuUpdater $recombination-weights $delta-mean $i $num-selected) (
    if (== $i 5)
        ()
        (let* (
            ($row (rankMuUpdater' $recombination-weights $delta-mean $i 0 $num-selected))
            ($rest (rankMuUpdater $recombination-weights $delta-mean (+ 1 $i) $num-selected))
        ) (cons-atom $row $rest))
))

(= (updateRankMu $recombination-weights $delta-mean $num-selected) (
    rankMuUpdater $recombination-weights $delta-mean 0 $num-selected
))

(= (updateCovHelper' $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov $i $j) (
    if (== $j 5)
        ()
        (let* (
            ($cov-value (getMatrixValue $covariance-matrix $i $j))
            ($base (* $cov-value (- (- 1 $learning-rate-rank1) $learning-rate-rank-mu)))
            ($rank-one-update-val (getMatrixValue $rank-one-update $i $j))
            ($rank-mu-update-val (getMatrixValue $rank-mu-update $i $j))
            ($one (- 1 $hsig-condition))
            ($two (* $cumulation-time-constant-cov (- 2 $cumulation-time-constant-cov)))
            ($rank-one (* $learning-rate-rank1 (+ $rank-one-update-val (* $one (* $two $cov-value)))))
            ($rank-mu (* $learning-rate-rank-mu $rank-mu-update-val))
            ($res (+ $base (+ $rank-mu $rank-one)))
            ($rest (updateCovHelper' $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov $i (+ 1 $j)))
        ) (cons-atom $res $rest))
))

(= (updateCovHelper $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov $i) (
    if (== $i 5)
        ()
        (let* (
            ($val (updateCovHelper' $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov $i 0))
            ($rest (updateCovHelper $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov (+ 1 $i)))
        ) (cons-atom $val $rest))
))

(= (updateCov $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov) (
    updateCovHelper $learning-rate-rank1 $learning-rate-rank-mu $rank-mu-update $covariance-matrix $rank-one-update $hsig-condition $cumulation-time-constant-cov 0
))