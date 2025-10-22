;; isMember: Check if a value is in a list

(= (isMember' $list $val) (
    let* (
        (($head $tail) (decons-atom $list))
    ) (if (== $head $val) 
        True 
        (if (== $tail ()) 
            False 
            (isMember' $tail $val)))
))

(: isMember (-> Expression Number Bool))
(= (isMember $list $val) (
    let $exists (collapse (let $member (superpose $list) (if (== $member $val) True Empty)))
    (if (== $exists ()) False True)
))

;; Test
!("Non-Deterministic")
!(isMember (1 2 3 4) 1)
!(isMember (1 2 3 4) 5)

!("Deterministic")
!(isMember' (1 2 3 4) 1)
!(isMember' (1 2 3 4) 5)