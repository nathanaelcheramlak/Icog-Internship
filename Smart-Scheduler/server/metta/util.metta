;; General Utils

;; Recives a list and a value, returns the list without the value
(: filter (-> Expression Number Expression))
(= (filter $exp $val) (
    if (== $exp ())
        ()
        (let* (
            (($head $tail) (decons-atom $exp))
            ($rest (filter $tail $val))
        ) (if (== $head $val)
            $rest
            (cons-atom $head $rest)
        ))
))

(= (reverse $list $acc) (
    if (== $list ()) 
        $acc
        (let ($head $tail ) (decons-atom $list) (reverse $tail (cons-atom $head $acc) ))
))

;; Recives a space, an old atom and a new atom, returns the space with the old atom replaced by the new atom
(: update-atom (-> Grounded Atom Atom (->)))
(= (update-atom $space $oldAtom $newAtom) (
    let $_ (remove-atom $space $oldAtom) (add-atom $space $newAtom)
))

;; Query Utils

(= (getName $taskId $space) (
    match $space (Task $taskId (Name $name) (Description $desc)) $name
))

(= (getDescription $taskId $space) (
    match $space (Task $taskId (Name $name) (Description $desc)) $desc
))

(= (getDependency $taskId $space) (
    match $space (Dependency $taskId $dependency) $dependency
))

(= (getNeighbours $taskId $space) (
    collapse (match $space (DirectedEdge $taskId $neighbour) $neighbour)
))

(= (getDeadline $taskId $space) (
    match $space (Deadline $taskId $deadline) $deadline
))

(= (getIndegree $taskId $space) (
    match $space (Indegree $taskId $val) $val 
))

(= (getPriority $taskId $space) (
    match $space (Priority $taskId $priority) $priority
))

;; Topological Sort Utils

(= (getNeighboursForMultipleTasks $tasks $space $neighbours) (
    if (== $tasks ())
        $neighbours
        (let* (
            (($head $tail) (decons-atom $tasks))
            ($nei (getNeighbours $head $space))
            ($newNeighbours (union-atom $neighbours $nei))
        ) (getNeighboursForMultipleTasks $tail $space $newNeighbours))
))

(= (updateIndegree $taskId $newVal $space) (
    let* (
        ($ind (getIndegree $taskId $space))
        ($d (update-atom $space (Indegree $taskId $ind) (Indegree $taskId $newVal)))
    ) $newVal
))

(= (findWithIndegree $indVal $space) (
    collapse (let $task (match $space (Indegree $node $indVal) $node) $task)
))

(= (getZeroIndegree $tasks $space) (
    if (== $tasks ())
        ()
        (let* (
            ; ($_ (println! (Getting zero indegree from tasks: $tasks)))
            (($head $tail) (decons-atom $tasks))
            ($headIndegree (getIndegree $head $space))
            ; ($_ (println! (Task: $head Indegree: $headIndegree)))
            ($rest (getZeroIndegree $tail $space))
        ) (if (== $headIndegree 0)
            (cons-atom $head $rest)
            $rest
        ))
))

(= (decrementIndegreeForMultipleTasks $tasks $space) (
    if (== $tasks ())
        ()
        (let* (
            (($taskId $tail) (decons-atom $tasks))
            ($taskIndegree (getIndegree $taskId $space))
            ; ($_ (println! (Decrementing indegree for task: $taskId from $taskIndegree to (- $taskIndegree 1))))
            ($a (updateIndegree $taskId (- $taskIndegree 1) $space))
            ; ($ind (getIndegree $taskId $space))
            ; ($c (println! (Indegree after decrement (Helper): $ind)))
        ) (decrementIndegreeForMultipleTasks $tail $space))
))

(= (incrementIndegreeForMultiple $tasks $space) (
    if (== $tasks ())
    ()
    (let* (
        (($taskId $tail) (decons-atom $tasks))
        ($taskIndegree (getIndegree $taskId $space))
        ($a (updateIndegree $taskId (+ $taskIndegree 1) $space))
    ) (incrementIndegreeForMultiple $tail $space))
))