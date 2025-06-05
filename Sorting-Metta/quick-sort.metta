(= (filterLess $pivot $list)
   (if (== $list ())
       () ; Base case: empty list
       (let*
           (
              ($head (car-atom $list))
              ($tail (cdr-atom $list))
              ($restFiltered (filterLess $pivot $tail)) ; Recursive filtering
           )
           (if (< $head $pivot)
               (cons-atom $head $restFiltered) ; Include $head if it's less than $pivot
               $restFiltered ; Skip $head otherwise
           )
       )
   )
)

(= (filterGreaterEqual $pivot $list)
   (if (== $list ())
       () ; Base case: empty list
       (let*
           (
              ($head (car-atom $list))
              ($tail (cdr-atom $list))
               ($restFiltered (filterGreaterEqual $pivot $tail)) ; Recursive filtering
           )
           (if (>= $head $pivot)
               (cons-atom $head $restFiltered) ; Include $head if it's greater or equal to $pivot
               $restFiltered ; Skip $head otherwise
           )
       )
   )
)

(= (sort $list)
   (if (== $list ())
       () ; Base case: empty list is already sorted
       (let*
           (
               ($pivot (car-atom $list)) ; Split into pivot and rest
               ($rest (cdr-atom $list))
               ($smaller (filterLess $pivot $rest)) ; Elements smaller than pivot
               ($greater (filterGreaterEqual $pivot $rest)) ; Elements greater or equal to pivot
               ($greaterRemaining (sort $greater))
               ($smallerRemaining (sort $smaller))
               ($greater-pivot (cons-atom $pivot $greaterRemaining))
           )
            (union-atom $smallerRemaining $greater-pivot)
       )
   )
)


!(sort (3 1 4 0 6 4))
