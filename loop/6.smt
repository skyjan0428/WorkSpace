(set-option :produce-models true)
 (set-logic ALL)
 (declare-fun *a () Int)
(declare-fun *b () Int)
(assert (not (> *a 1)  ) )
(assert (> *a 1)  )
(check-sat)
 (get-model)