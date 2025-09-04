; !(register-module! ../../metta)
; !(import! &self metta:schedule)

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