!(register-module! ../../metta)
!(import! &self metta:utils)


;; Filter Test
!(assertEqual (filter (1 2 3 4 5 1 2 3) 3) (1 2 4 5 1 2))

;;; Update Atom Test
(Parent Tom)
!(update-atom &self (Parent Tom) (Parent Jerry))
!(assertEqual (match &self (Parent $x) $x) Jerry)

;; Get Neighbours Test
(DirectedEdge 1 2)
(DirectedEdge 1 3)
!(assertEqual (getNeighbours 1 &self) (2 3))

;; Get Neighbours for Multiple Tasks Test
(DirectedEdge 2 4)
!(assertEqual (getNeighboursForMultipleTasks (1 2) &self ()) (2 3 4))

;; Get Indegree Test
(Indegree 1 1)
(Indegree 2 0)
(Indegree 3 0)
!(assertEqual (getIndegree 1 &self) 1)
!(assertEqual (getIndegree 2 &self) 0)
!(assertEqual (getIndegree 3 &self) 0)

;; Update Indegree Test
!(assertEqual (updateIndegree 1 5 &self) 5)
!(assertEqual (getIndegree 1 &self) 5)

;; Find With Indegree Test
!(assertEqual (findWithIndegree 0 &self) (3 2))

;; Get Zero Indegree Test
!(assertEqual (getZeroIndegree (1 2 3) &self) (2 3))

;; Decrement Indegree for Multiple Tasks Test
!(decrementIndegreeForMultipleTasks (1) &self)
!(assertEqual (getIndegree 1 &self) 4)