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

;; Gets name given a task representation
(= (getName $taskId $space) (
    match $space (Task $taskId (Name $name) (Description $desc)) $name
))

;; Gets description given a task representation
(= (getDescription $taskId $space) (
    match $space (Task $taskId (Name $name) (Description $desc)) $desc
))

;; Gets the dependency of a given taskId
(= (getDependency $taskId $space) (
    match $space (Dependency $taskId $dependency) $dependency
))

;; Gets the neighbours of a given taskId
(= (getNeighbours $taskId $space) (
    collapse (match $space (DirectedEdge $taskId $neighbour) $neighbour)
))

;; Given a task it gets the deadline
(= (getDeadline $taskId $space) (
    match $space (Deadline $taskId $deadline) $deadline
))

;; Given a task it gets a the number of indegree's it has
(= (getIndegree $taskId $space) (
    match $space (Indegree $taskId $val) $val 
))

;; Given a taskId it gets the priority
(= (getPriority $taskId $space) (
    match $space (Priority $taskId $priority) $priority
))

;; Topological Sort Utils

;; Given the current tasks it combines all their unvisited neighbours
(= (getNeighboursForMultipleTasks $tasks $space $neighbours) (
    if (== $tasks ())
        $neighbours
        (let* (
            (($head $tail) (decons-atom $tasks))
            ($nei (getNeighbours $head $space))
            ($newNeighbours (union-atom $neighbours $nei))
        ) (getNeighboursForMultipleTasks $tail $space $newNeighbours))
))

;; Given tasks it updates their indegrees
(= (updateIndegree $taskId $newVal $space) (
    let* (
        ($ind (getIndegree $taskId $space))
        ($d (update-atom $space (Indegree $taskId $ind) (Indegree $taskId $newVal)))
    ) $newVal
))

;; Given a specific indegree value it returns tasks with the specified indegree
(= (findWithIndegree $indVal $space) (
    collapse (let $task (match $space (Indegree $node $indVal) $node) $task)
))

;; Given an expression of tasks it filters out tasks with indegree equal zero
(= (getZeroIndegree $tasks $space) (
    if (== $tasks ())
        ()
        (let* (
            (($head $tail) (decons-atom $tasks))
            ($headIndegree (getIndegree $head $space))
            ($rest (getZeroIndegree $tail $space))
        ) (if (== $headIndegree 0)
            (cons-atom $head $rest)
            $rest
        ))
))

;; Given tasks it decrements one from all the given tasks
(= (decrementIndegreeForMultipleTasks $tasks $space) (
    if (== $tasks ())
        ()
        (let* (
            (($taskId $tail) (decons-atom $tasks))
            ($taskIndegree (getIndegree $taskId $space))
            ($a (updateIndegree $taskId (- $taskIndegree 1) $space))
        ) (decrementIndegreeForMultipleTasks $tail $space))
))

;; Given tasks it increments one to all the given tasks
(= (incrementIndegreeForMultiple $tasks $space) (
    if (== $tasks ())
    ()
    (let* (
        (($taskId $tail) (decons-atom $tasks))
        ($taskIndegree (getIndegree $taskId $space))
        ($a (updateIndegree $taskId (+ $taskIndegree 1) $space))
    ) (incrementIndegreeForMultiple $tail $space))
))