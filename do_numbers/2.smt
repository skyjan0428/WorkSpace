(set-option :produce-models true)
 (set-logic ALL)
 (declare-fun *a () Int)
(declare-fun *b () Int)s
(assert (not (> *a *b)  ) )
(assert (> 0 *a)  )
(check-sat)
 (get-model)
