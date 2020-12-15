(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun tstr () String)
(assert (not (< (- (str.len tstr) 0) 2)))
(assert (not (>= 3 (str.len tstr))))
(assert (not (= (str.substr tstr 2  3) ":")))
(check-sat)
(get-model)

