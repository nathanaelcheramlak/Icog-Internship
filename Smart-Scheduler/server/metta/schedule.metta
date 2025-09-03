; !(register-module! ../metta)
; !(import! &self metta:util)

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

(= (scheduleHelper $schedules $ready $space) (
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
        ) (scheduleHelper $newSchedules $nextReady $space))
))

(= (schedule) (
    let* (
        ($allTasks (collapse (match &self (Deadline $taskId $_) $taskId)))
        ($_ (println! (All Tasks: $allTasks)))
        ($ready (getZeroIndegree $allTasks &self))
        ($_ (println! (Initial Ready: $ready)))
        ($schedules (scheduleHelper () $ready &self))
        ($reversedSchedules (reverse $schedules ()))
    ) $reversedSchedules)
)

;; Tests
; (Task 1 (Name "Task-A") (Description "Write Proposal"))
; (Task 2 (Name "Task-B") (Description "Seal Proposal"))
; (Task 3 (Name "Task-C") (Description "Submit Proposal"))

; (Deadline 1 0)
; (Deadline 2 1)
; (Deadline 3 1)

; (Dependency 1 ())
; (Dependency 2 (1))
; (Dependency 3 (2))

; (Indegree 1 0)
; (Indegree 2 1)
; (Indegree 3 1)

; (DirectedEdge 1 2)
; (DirectedEdge 2 3)
; !(schedule)

;; Test 2
; (Task 1 (Name "a") (Description "No Description"))
; (Task 2 (Name "b") (Description "No Description"))

; (Priority 1 High)
; (Priority 2 High)

; (Indegree 2 1)
; (Indegree 1 0)

; (Deadline 2 21042022)
; (Deadline 1 21042022)

; (DirectedEdge 1 2)
; !(schedule)