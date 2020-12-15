(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun tstr () String)
(assert (< (- (str.len tstr) 0) 2))
(check-sat)
(get-model)

