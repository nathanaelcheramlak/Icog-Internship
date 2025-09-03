(: update-atom (-> Grounded Atom Atom (->)))
(= (update-atom $space $oatom $natom) (let $_ (remove-atom $space $oatom) (add-atom $space $natom)))

; Removes all val from exp
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

(= (getIndegree $taskId $space) (
    match $space (Indegree $taskId $val) $val 
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


(= (getDeadline $taskId $space) (
    match $space (Deadline $taskId $deadline) $deadline
))

(= (updateDeadline $taskId $newDeadline $space) (
    let* (
        ((Deadline $taskId $oldDeadline) (getDeadline $space $taskId))
        ($_ (update-atom $space (Deadline $taskId $oldDeadline) (Deadline $taskId $newDeadline)))
    )  ()
))

(= (getDependency $taskId $space) (
    match $space (Dependency $taskId $dependency) $dependency
))

;; Given a taskId it removes a one dependency task from the given task with the taskId it removes dep
(= (removeDependency $taskId $dep $space) (
    let* (
        ($oldDep (getDependency $space $taskId))
        ($newDep (filter $oldDep $dep))
        ($_ (update-atom $space (Dependency $taskId $oldDep) (Dependency $taskId $newDep)))
    ) $newDep
))

(= (getNeighbours $taskId $space) (
    collapse (match $space (DirectedEdge $taskId $neighbour) $neighbour)
))

(= (getNeighboursForMultipleTasks $tasks $space $neighbours) (
    if (== $tasks ())
        $neighbours
        (let* (
            (($head $tail) (decons-atom $tasks))
            ($nei (getNeighbours $head $space))
            ($newNeighbours (union-atom $neighbours $nei))
        ) (getNeighboursForMultipleTasks $tail $space $newNeighbours))
))

;; Given an list of tasks it filters out tasks with indegree more than 0
(= (getZeroIndegree $tasks $space) (
    if (== $tasks ())
        ()
        (let* (
            ($_ (println! (Getting zero indegree from tasks: $tasks)))
            (($head $tail) (decons-atom $tasks))
            ($headIndegree (getIndegree $head $space))
            ($_ (println! (Task: $head Indegree: $headIndegree)))
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
            ($_ (println! (Decrementing indegree for task: $taskId from $taskIndegree to (- $taskIndegree 1))))
            ($a (updateIndegree $taskId (- $taskIndegree 1) $space))
            ; ($ind (getIndegree $taskId $space))
            ; ($c (println! (Indegree after decrement (Helper): $ind)))
        ) (decrementIndegreeForMultipleTasks $tail $space))
))

(= (schedule $schedules $ready $space) (
    if (== $ready ())
        $schedules
        (let* (
            ; ($_ (buildIndegree $space))
            ($_ (println! (Scheduled: $schedules & Ready: $ready)))
            ($newSchedules (cons-atom $ready $schedules))
            ($neighbours (getNeighboursForMultipleTasks $ready $space ()))
            ($_ (println! (Neighbours: $neighbours)))
            ($_ (decrementIndegreeForMultipleTasks $neighbours $space))
            ; ($ind (match $space (Indegree $node $indVal) $indVal))
            ; ($c (println! (Indegree after decrement: $ind)))
            ($nextReady (getZeroIndegree $neighbours $space))
            ($_ (println! (Next Ready: $nextReady)))
        ) (schedule $newSchedules $nextReady $space))
))

;; Test
(Task 1 (Name "Task-A") (Description "Write Proposal"))
(Task 2 (Name "Task-B") (Description "Seal Proposal"))
(Task 3 (Name "Task-C") (Description "Submit Proposal"))

(Dependency 2 (1))
(Dependency 3 (2))

(Indegree 1 0)
(Indegree 2 0)
(Indegree 3 1)

; (DirectedEdge 1 2)
(DirectedEdge 2 3)


!(schedule () (1 2) &self)