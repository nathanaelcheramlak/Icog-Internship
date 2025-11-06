;; Calculate Euclidean norm of evolution path sigma
;; $evol-path-sigma: vector ps
(= (calculate-euclidean-norm $evol-path-sigma) (
    let $sum (sum (collapse (let $val (superpose $evol-path-sigma) (* $val $val)))) (sqrt $sum)
))

;; Update global step size using cumulative path length control
;; Variables:
;;  $step-size: current sigma
;;  $evol-path-sigma: ps vector
;;  $cumulation-time-constant-sigma: c_sigma
;;  $damping-sigma: damping factor
;;  $expected-norm: E||N(0,I)||
(= (update-step-size $step-size $evol-path-sigma $cumulation-time-constant-sigma $damping-sigma $expected-norm) (
    let* (
        ($norm (calculate-euclidean-norm $evol-path-sigma))
        ($exponent (* (/ $cumulation-time-constant-sigma $damping-sigma) (- (/ $norm $expected-norm) 1)))
    ) (* $step-size (exp $exponent))
))