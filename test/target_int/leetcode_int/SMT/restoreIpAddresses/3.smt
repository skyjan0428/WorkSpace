(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun s () String)
(assert (not (or (or (= (str.len s) 0) (> (str.len s) 12)) (> (str.to.int s) 0))))

(check-sat)
(get-model)