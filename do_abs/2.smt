(set-option :produce-models true)
 (set-logic ALL)
(define-fun do_abs ((a Int)) Int 
 (ite (< a 0) (* (- 0 1) a) a))
(assert (>= (do_abs *a) (do_abs *b))  )
(check-sat)
 (get-model)
