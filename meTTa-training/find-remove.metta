;; findAndRemove: Remove the first occurrence of a value from a list

(: findAndRemove' (-> Expression Number Expression))
(= (findAndRemove' () $val) ())
(= (findAndRemove' $list $val) (
    let* (
        (($head $tail) (decons-atom $list))
        ($rest (findAndRemove' $tail $val))
    ) (if (== $head $val)
        $rest
        (cons-atom $head $rest))
))

(: findAndRemove (-> Expression Number Expression))
(= (findAndRemove $list $val) (
    let $newList (collapse (let $member (superpose $list) (if (== $member $val) Empty $member)))
    $newList
))

;; Test
!("Non-Deterministic")
!(findAndRemove (1 2 3 4 2) 2)
!(findAndRemove (1 2 3 4) 1)
!(findAndRemove (1 2 3 4) 5)

!("Deterministic")
!(findAndRemove' (1 2 3 4 2) 2)
!(findAndRemove' (1 2 3 4) 1)
!(findAndRemove' (1 2 3 4) 5)