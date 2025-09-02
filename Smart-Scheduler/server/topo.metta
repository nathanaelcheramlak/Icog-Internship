; -----------------------------
; Example graph: A → B, B → C, A → C
; -----------------------------
(Edge A B)
(Edge B C)
(Edge A C)

; -----------------------------
; Find all neighbors of a node
; -----------------------------
(= (neighbors $x)
   (match &self (Edge $x $y) $y))

; -----------------------------
; contains? : check if element is in list
; -----------------------------
(= (contains $x ()) False)
(= (contains $x (:: $x $xs)) True)
(= (contains $x (:: $y $ys)) (contains $x $ys))

; -----------------------------
; visit-all : DFS on a list of nodes
; -----------------------------
(= (visit-all () $visited) $visited)
(= (visit-all (:: $n $ns) $visited)
   (visit-all $ns (visit $n $visited)))

; -----------------------------
; visit : recursive DFS
; -----------------------------
(= (visit $node $visited)
   (if (contains $node $visited)
       $visited
       (post-visit $node (visit-all (neighbors $node) $visited))))

; -----------------------------
; post-visit : prepend node
; -----------------------------
(= (post-visit $node $visited)
   (:: $node $visited))

; -----------------------------
; toposort : run DFS for each node
; -----------------------------
(= (toposort $nodes)
   (visit-all $nodes ()))

; -----------------------------
; Example Run
; -----------------------------
! (toposort (:: A (:: B (:: C ()))))
