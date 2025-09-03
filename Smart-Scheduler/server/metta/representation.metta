;; =============================================================================
;; SMART SCHEDULER - TASK REPRESENTATION SCHEMA
;; =============================================================================
;; This file defines the core data structures and relationships for task
;; management in the Smart Scheduler system. The schema is designed for
;; efficient pattern matching and logical inference.
;; =============================================================================

;; =============================================================================
;; TASK ENTITY REPRESENTATION
;; =============================================================================
;; Format: (Task <task_id> (Name <task_name>) (Description <task_description>))
;; Purpose: Defines the core task entity with unique identifier and metadata
;; =============================================================================

(Task 1 (Name "Task-A") (Description "Write Proposal"))

;; =============================================================================
;; TASK PRIORITY REPRESENTATION
;; =============================================================================
;; Format: (Priority <task_id> <priority_level>)
;; Priority Levels: Low, Medium, High, Critical
;; Purpose: Assigns priority classification to tasks for scheduling decisions
;; =============================================================================

(Priority 1 High)

;; =============================================================================
;; TASK DEADLINE REPRESENTATION
;; =============================================================================
;; Format: (Deadline <task_id> <deadline_date>)
;; Date Format: YYYYMMDD (serialized for efficient sorting and comparison)
;; Purpose: Defines temporal constraints for task completion
;; =============================================================================

(Deadline 1 20231202)

;; =============================================================================
;; TASK DEPENDENCY REPRESENTATION
;; =============================================================================
;; Format: (Dependency <task_id> (<dependent_task_ids>))
;; Purpose: Defines prerequisite relationships between tasks
;; Note: Task with ID <task_id> cannot start until all dependent tasks complete
;; =============================================================================

(Dependency 1 (2 3)) ;; Task 1 requires completion of Tasks 2 and 3


(Indegree 1 2)

;; Makes querying faster and built at runtime
(DirectedEdge 1 2)