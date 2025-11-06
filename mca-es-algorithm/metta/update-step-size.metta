(= (calculate-euclidean-norm $evol-path-sigma) (
    let $sum (sum (collapse (let $val (superpose $evol-path-sigma) (* $val $val)))) (sqrt $sum)
))

(= (update-step-size $step-size $evol-path-sigma $cumulation-time-constant-sigma $damping-sigma $expected-norm) (
    let* (
        ($norm (calculate-euclidean-norm $evol-path-sigma))
        ($exponent (* (/ $cumulation-time-constant-sigma $damping-sigma) (- (/ $norm $expected-norm) 1)))
    ) (* $step-size (exp $exponent))
))