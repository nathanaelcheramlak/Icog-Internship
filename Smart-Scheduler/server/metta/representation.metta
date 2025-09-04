;; =============================================================================
;; SMART TASK SCHEDULER - KNOWLEDGE REPRESENTATION SCHEMA
;; =============================================================================
;; This file defines the core data structures and relationships for the
;; Smart Task Scheduler system using MeTTa (Meta Type Theory).
;; 
;; The schema is designed for:
;; - Efficient pattern matching and logical inference
;; - Clear representation of task dependencies and constraints
;; - Optimal scheduling algorithm support
;; =============================================================================

;; =============================================================================
;; CORE TASK ENTITY
;; =============================================================================
;; Represents a task with its essential metadata
;; 
;; Format: (Task <task_id> (Name <task_name>) (Description <task_description>))
;; 
;; Example:
;; (Task 1 (Name "Complete Project Report") (Description "Write quarterly report"))
;; =============================================================================

;; =============================================================================
;; TASK PRIORITY CLASSIFICATION
;; =============================================================================
;; Assigns priority levels to tasks for scheduling decisions
;; 
;; Format: (Priority <task_id> <priority_level>)
;; Priority Levels: Low, Medium, High
;; 
;; Example:
;; (Priority 1 High)
;; =============================================================================

;; =============================================================================
;; TASK DEADLINE CONSTRAINT
;; =============================================================================
;; Defines temporal constraints for task completion
;; 
;; Format: (Deadline <task_id> <deadline_date>)
;; Date Format: YYYYMMDD (efficient for sorting and comparison)
;; 
;; Example:
;; (Deadline 1 20231202)
;; =============================================================================

;; =============================================================================
;; TASK DEPENDENCY RELATIONSHIPS
;; =============================================================================
;; Represents directed edges in the task dependency graph
;; 
;; Format: (DirectedEdge <source_task_id> <target_task_id>)
;; Meaning: source_task must be completed before target_task
;; 
;; Example:
;; (DirectedEdge 1 2)  ; Task 1 must be completed before Task 2
;; =============================================================================

;; =============================================================================
;; TASK IN-DEGREE TRACKING
;; =============================================================================
;; Tracks the number of dependencies for each task
;; Used for topological sorting and parallel execution detection
;; 
;; Format: (Indegree <task_id> <dependency_count>)
;; 
;; Example:
;; (Indegree 2 1)  ; Task 2 has 1 dependency
;; =============================================================================

;; =============================================================================
;; SAMPLE TASK DATA
;; =============================================================================
;; Example task definitions demonstrating the schema usage
;; =============================================================================

;; Task 1: High priority task with no dependencies
(Task 1 (Name "Project Planning") (Description "Create project timeline and milestones"))
(Priority 1 High)
(Deadline 1 20231201)
(Indegree 1 0)

;; Task 2: Medium priority task that depends on Task 1
(Task 2 (Name "Research Phase") (Description "Conduct market research and analysis"))
(Priority 2 Medium)
(Deadline 2 20231205)
(Indegree 2 1)
(DirectedEdge 1 2)

;; Task 3: Low priority task that also depends on Task 1
(Task 3 (Name "Documentation") (Description "Prepare project documentation"))
(Priority 3 Low)
(Deadline 3 20231210)
(Indegree 3 1)
(DirectedEdge 1 3)