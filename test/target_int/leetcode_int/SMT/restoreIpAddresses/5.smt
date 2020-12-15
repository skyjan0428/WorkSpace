(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun s () String)
(assert (or (or (= (str.len s) 0) (> (str.len s) 12)) (> (str.to.int s) 0)))
(assert (= (str.len (str.substr s 0 1)) 1))
(assert (= (str.at (str.substr s 1 2) 0) "0"))
(assert (<= (str.to.int (str.substr s 2 3)) 255))
(assert (= (str.len (str.substr s 3 (str.len s))) 1))

(check-sat)
(get-model)




ls = (str.len s)
if (or (or (= ls 0) (> ls 12)) (not s.isdigit()))

res = []
m = (- (- (- ls 1) 1) 1)

if (and (> m 0) (<= m 3))
	add1 = (str.sub s 0 1)
	add2 = (str.sub s 1 2)
	add3 = (str.sub s 2 3)
	add4 = (str.sub s 3 (str.len s))
	if (and (and (and (= (str.len add1) 1) (= (str.at add2 0) 0)) (<= (str.to.int add3) 255)) (= (str.len add4) 1))
