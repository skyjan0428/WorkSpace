(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun dtstr () String)
(assert (not (= (str.len dtstr) 10)))
(check-sat)
(get-model)
