;; findAndReplace: Replace all occurrences of a value in a list

(: findAndReplace' (-> Expression Number Number Expression))
(= (findAndReplace' () $oldVal $newVal) ())
(= (findAndReplace' $list $oldVal $newVal) (
    let* (
        (($head $tail) (decons-atom $list))
        ($rest (findAndReplace' $tail $oldVal $newVal))
    ) (if (== $head $oldVal) 
        (cons-atom $newVal $rest) 
        (cons-atom $head $rest))
))


(: findAndReplace (-> Expression Number Number Expression))
(= (findAndReplace $list $oldVal $newVal) (
    let $newList (collapse (let $member (superpose $list) (if (== $member $oldVal) $newVal $member)))
    $newList
))

;; Test
!("Non-Deterministic")
!(findAndReplace (1 2 3 4 2) 2 0)
!(findAndReplace (1 2 3 4) 1 0)
!(findAndReplace (1 2 3 4) 5 0)

!("Deterministic")
!(findAndReplace' (1 2 3 4 2) 2 0)
!(findAndReplace' (1 2 3 4) 1 0)
!(findAndReplace' (1 2 3 4) 5 0)