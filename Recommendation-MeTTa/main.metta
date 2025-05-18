(food PBJ (ingredients Bread PeanutButter Jam))
(food BLT (ingredients Bread Lettuce Tomato))
(food Salad (ingredients Lettuce Tomato Cucumber))
(food EmptyDish (ingredients))
(food OneItem (ingredients Bread))

(my-ing (Bread PeanutButter Jam Banana Cucumber Avocado Tomato Cheese Lettuce))

; Checks if an ingredient exists in a pool of ingredients
; Returns 1 if found else 0
(= (find_ingredient $ing ()) 0)
(= (find_ingredient $ing $ingredients) (
    if (== (car-atom $ingredients) $ing) 1 (find_ingredient $ing (cdr-atom $ingredients))
))


; Count common ingredients
(= (count-common-ingredients $x ()) 0)
(= (count-common-ingredients $available-ingredients $all-ingredients) (
    + (find_ingredient (car-atom $all-ingredients) $available-ingredients) (count-common-ingredients $available-ingredients (cdr-atom $all-ingredients)))
)

; Count ingredients
(= (count-ingredients ()) 0)
(= (count-ingredients $ingredients) (
    + 1 (count-ingredients (cdr-atom $ingredients))
))


; Iterate over all the foods and find matches
(= (get-foods) (match &self (food $name $ingredients) (
    if (<= (count-ingredients (cdr-atom $ingredients)) (match &self (my-ing $ing) (count-common-ingredients $ing (cdr-atom $ingredients))))
    ($name)
    ()
)))


;Test Cases
;find_ingredient
!(find_ingredient Tomato (Tomato Onion Garlic))           ; Expect 1
!(find_ingredient Cheese (Tomato Onion Garlic))           ; Expect 0
!(find_ingredient Onion ())                               ; Expect 0
!(find_ingredient Bread (Bread Bread Butter))             ; Expect 1

; count-common-ingredients
!(count-common-ingredients (A B C) (C A H))               ; Expect 2
!(count-common-ingredients (A B C) (D E F))               ; Expect 0
!(count-common-ingredients (A B C D E F) (C B A))         ; Expect 3
!(count-common-ingredients () (A B C))                    ; Expect 0
!(count-common-ingredients (X X X) (X))                   ; Expect 1

; count-ingredients
!(count-ingredients (A B C))                              ; Expect 3
!(count-ingredients ())                                   ; Expect 0
!(count-ingredients (A))                                  ; Expect 1

; Total Test
!(get-foods)
