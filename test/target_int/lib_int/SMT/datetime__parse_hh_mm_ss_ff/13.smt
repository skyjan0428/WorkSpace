(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun tstr () String)
(assert (not (< (- (str.len tstr) 0) 2)))
(assert (not (>= 3 (str.len tstr))))
(assert (not (not (= (str.substr tstr 2  3) ":"))))
(assert (< 9 (str.len tstr)))
(assert (not (not (= (str.at tstr 9) "."))))
(assert (not (not (or (= (- (str.len tstr) 10) 3) (= (- (str.len tstr) 10) 6)))))
(assert ((= (- (str.len tstr) 10) 3) ))
(assert (not (> (str.to.int(str.substr tstr 0 2)) 12)))
(assert (not (< (str.to.int(str.substr tstr 0 2)) 0)))
(assert (not (> (str.to.int(str.substr tstr 3 5)) 60))
(assert (not (< (str.to.int(str.substr tstr 3 5)) 0)))
(assert (not (> (str.to.int(str.substr tstr 6 8)) 60)))
(assert (not (< (str.to.int(str.substr tstr 6 8)) 0)))
(check-sat)
(get-model)


len_str = (str.len tstr)

time_comps = [0,0,0,0]
pos = 0
for 0~2
	if (< (- len_str pos) 2)

	if (>= (+ pos 1) (str.len tstr))

	if (not (= (str.substr tstr pos (+ pos 1)) ":"))

	pos += 

if pos < len_str
	if (not (= (str.at tstr pos) "."))

	else
		pos += 1
		if (not (or (= (- len_str pos) 3) (= (- len_str pos) 6)))

		if (= (- len_str pos) 3) 


if (> (str.to.int(str.substr tstr 0 2)) 12)

if (< (str.to.int(str.substr tstr 0 2)) 0)

if (> (str.to.int(str.substr tstr 3 5)) 60)

if (< (str.to.int(str.substr tstr 3 5)) 0)

if (> (str.to.int(str.substr tstr 6 8)) 60)

if (< (str.to.int(str.substr tstr 6 8)) 0)






