(set-option :produce-models true)
 (set-logic ALL)
 (declare-fun *a () Int)
(declare-fun *b () Int)
(define-fun max ((a Int) (b Int)) Int 
 (ite (>= a b) a b))
(define-fun min ((a Int) (b Int)) Int 
 (ite (<= a b) a b))

(define-fun abs ((a Int)) Int 
 (ite (< a 0) (* -1 a) a))
(assert (> (+ (+ 1 (+ 2 (+ 3 (+ *a *b)))) (min *b 0)) (max *a 100))  )
(check-sat)
 (get-model)
