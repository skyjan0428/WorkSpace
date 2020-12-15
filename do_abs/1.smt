(set-option :produce-models true)
 (set-logic ALL)
(define-fun do_abs ((a Int)) Int 
 (ite (< a 0) (* (- 0 1) a) a))
(declare-fun *a () Int)
(declare-fun *b () Int)
(assert (not (>= (do_abs *a) (do_abs *b))  ) )
(check-sat)
 (get-model)
