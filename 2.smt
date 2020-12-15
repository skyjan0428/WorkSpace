(set-option :produce-models true)
 (set-logic ALL)
(define-fun max ((a Int) (b Int)) Int 
 (ite (>= a b) a b))
(define-fun min ((a Int) (b Int)) Int 
 (ite (<= a b) a b))
(assert ( (> (+ (+ 1 (+ 2 (+ 3 (+ *a *b)))) (min *b 0)) (max *a 100))  ))
(check-sat)
 (get-model)
