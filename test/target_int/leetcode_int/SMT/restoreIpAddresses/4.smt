(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun s () String)
(assert (or (or (= (str.len s) 0) (> (str.len s) 12)) (> (str.to.int s) 0)))
(assert (not (= (str.len (str.substr s 0 2)) 1)))
(assert (= (str.at (str.substr s 2 3) 0) "0"))

(check-sat)
(get-model)

