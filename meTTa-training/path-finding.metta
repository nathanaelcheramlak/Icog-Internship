!(bind! &shortest (new-space))
!(bind! &graph (new-space))

;; Initailize Weighted Graph Representation
(: init-graph (-> hyperon::space::DynSpace (->)))
(= (init-graph $space) (
    add-reduct $space (superpose 
        (
            ;; Test Graph
            ; (4 (Node A) (Node B))
            ; (4 (Node B) (Node A))

            ; (1 (Node A) (Node C))
            ; (1 (Node C) (Node A))

            ; (5 (Node A) (Node D))
            ; (5 (Node D) (Node A))

            ; (0 (Node B) (Node D))
            ; (0 (Node D) (Node B))

            ; (2 (Node C) (Node D))
            ; (2 (Node D) (Node C))

            ;; Smaller Test Graph
            (2 (Node A) (Node B))
            (3 (Node B) (Node C))
            (1 (Node A) (Node C))
            (3 (Node C) (Node B))
        )
    )
))
!(init-graph &graph)

;; get-graph-nodes: Get all unique nodes in the graph
(: get-graph-nodes (-> hyperon::space::DynSpace Expression))
(= (get-graph-nodes $graph) (
    let* (
        ($start (collapse (match $graph ($w $start-node $end-node) $start-node)))
        ($end (collapse (match $graph ($w $start-node $end-node) $end-node)))   
        ($both (union-atom $start $end))
        ($unique (unique-atom $both))
    ) $unique
))

(: get-graph-size-manually (-> hyperon::space::DynSpace Number))
(= (get-graph-size-manually $graph) (
    let* (
        ($nodes (get-graph-nodes $graph))
        ($size (size-atom $nodes))
        ($_ (add-reduct $graph (GraphSize $size)))
    )
    $size
))
!(get-graph-size-manually &graph) ;; Call this to make graph size query faster

;; get-graph-size: Get the size of the graph (pre-computed)
(: get-graph-size (-> hyperon::space::DynSpace Number))
(= (get-graph-size $graph) (
    match $graph (GraphSize $size) $size
))

;; add-to-shortest: Adds a computed shortest path to the shortest space
(: add-to-shortest (-> hyperon::space::DynSpace Expression Expression Expression (->)))
(= (add-to-shortest $shortest $start-node $node $path) ( 
    add-atom $shortest (Shortest $start-node $node $path)
))

;; in-shortest: Check if a node is already pre-computed (added to the shortest)
(: in-shortest (-> hyperon::space::DynSpace Expression Bool))
(= (in-shortest $shortest $node) (
    let $x (collapse (match $shortest (Shortest $start-node $node $path) $node)) (if (== (size-atom $x) 0) False True)
))

;; get-shortest: Get all computed shortest nodes
(: get-shortest (-> hyperon::space::DynSpace Expression))
(= (get-shortest $shortest) (
    collapse (get-atoms $shortest)
))

;; get-weight: Given start and end nodes, it reads the weight from the graph
(: get-weight (-> hyperon::space::DynSpace Expression Expression Number))
(= (get-weight $graph $start-node $end-node) ( 
    match $graph ($weight $start-node $end-node) $weight
))

;; get-graph: Get all nodes in the graph
(: get-graph (-> Expression))
(= (get-graph) ( 
    collapse (get-atoms &graph)
))

;; get-neighbours: Given a node, returns its neighbours based on the graph
(: get-neighbours (-> hyperon::space::DynSpace Expression Expression))
(= (get-neighbours $graph $node) ( 
    collapse (match $graph ($w $node $neighbour) $neighbour)
))

;; get-unseen-neighbours: Given a node, returns neighbours that haven't been computed yet
(: get-unseen-neighbours (-> hyperon::space::DynSpace hyperon::space::DynSpace Expression Expression))
(= (get-unseen-neighbours $graph $shortest $node) ( 
    let* (
        ($neighbours (get-neighbours $graph $node))
        ($seen (collapse (let $nei (superpose $neighbours) (match $shortest (Shortest $node $nei $path) $nei))))
        ; ($unseen (subtraction (superpose $neighbours) (superpose $seen))) 
        ($unseen-left (subtraction-atom $neighbours $seen))
        ($unseen-right (subtraction-atom $seen $neighbours))
        ($unseen (union-atom $unseen-left $unseen-right))
    )
    $unseen
))

;; get-node: Given one heap element, it returns the node
(: get-node (-> Expression Expression))
(= (get-node ($w $node $path)) ( 
    $node
))

;; heappush: Pushes multiple nodes to the heap
(: heappush (-> hyperon::space::DynSpace Expression Expression Expression Expression))
(= (heappush $graph $heap $prev-edge $nodes) (
    if (== $nodes ())
        $heap
        (let* (
            (($head $tail) (decons-atom $nodes))
            (($prev-weight $prev-node $prev-path) $prev-edge)
            ($curr-weight (get-weight $graph $prev-node $head))
            ($new-weight (+ $curr-weight $prev-weight))
            ($new-path (union-atom $prev-path ($head)))
            ($new-heap (cons-atom ($new-weight $head $new-path) $heap))
        )
         (heappush $graph $new-heap $prev-edge $tail)
        )
))

; !(heappush &graph () (0 (Node A) ((Node A))) ((Node B) (Node C)))

;; remove: helper for heappop to remove an element
(: remove (-> Expression Expression (->)))
(= (remove $remove $expression) ( ;; helper for heappop to remove an element 
    collapse (let $item (superpose $expression) (if (== (get-node $item) (get-node $remove)) (empty) $item)))
)

;; find-min: helper for heappop, finds the min from the heap
(: find-min (-> Expression Expression))
(= (find-min ()) (-1 Nil Nil))
(= (find-min $heap) ( 
    let* (
        (($head $tail) (decons-atom $heap))
        (($weight $node $path) $head)
        ($minEdge (find-min $tail))
        (($minWeight $minNode $minPath) $minEdge)
    )(if (or (< $weight $minWeight) (== $minNode Nil))
        ($weight $node $path)
        ($minWeight $minNode $minPath)
    )
))

;; heappop: Pops the minimum edge from the heap
(: heappop (-> Expression Expression))
(= (heappop $heap) (
    let* (
        ($min-edge (find-min $heap))
        (($weight $start $end) $edge)
        ($new-heap (remove $min-edge $heap))
    )(if (== -1 $weight)
        ($min-edge ())
        ($min-edge $new-heap)
    )
))

;; Main Function
(: dijkstra (-> hyperon::space::DynSpace hyperon::space::DynSpace Expression Expression (->)))
(= (dijkstra $graph $shortest $heap $start-node) (
    let* (
        (($edge $new-heap) (heappop $heap))
        (($weight $node $path) $edge)
        ($node-in-shortest (in-shortest $shortest $node))
        ($unseen-nodes (get-unseen-neighbours $graph $shortest $node)) 
        ($_ (if $node-in-shortest () (add-to-shortest $shortest $start-node $node $path)))
        ($curr-shortest (get-shortest $shortest))
        ($graph-size (get-graph-size $graph))
        ; ($_ (println! (Calculated Nodes: (size-atom $curr-shortest)/ $graph-size)))
        ($curr-weight (get-weight $graph $node $nei)) ;; Weight between the current node to the neighbour
        ($updated-heap (heappush $graph $new-heap $edge $unseen-nodes))
    )(if (or (== 0 (size-atom $updated-heap)) (== (size-atom $curr-shortest) $graph-size)) ;; This number should be the total number of nodes in the graph
        ()
        (dijkstra $graph $shortest $updated-heap $start-node)
    )
))

;; Test

;; Function Structure:
;;   (dijkstra $graphSpace $resultSpace $initialHeap $startNode)
!(dijkstra &graph &shortest ((0 (Node A) ((Node A)))) (Node A))

!(get-atoms &shortest)