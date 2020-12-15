(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun word () String)
(declare-fun abbr () String)
(assert (or (>= (str.to.int (str.at abbr 0)) 0) (< (str.to.int (str.at abbr 0)) 0)))
(assert (not (and (= (str.to.int (str.at abbr 0)) 0) (= 0 0))))
(assert (not (or (>= (str.to.int (str.at abbr 1)) 0) (< (str.to.int (str.at abbr 1)) 0))))
(assert (>= (str.to.int (+ (int.to.str 0) (int.to.str (str.to.int (str.at abbr 0))))) (str.len word)))
(check-sat)
(get-model)


pos = curr = 0

for
	if (or (>= (str.to.int (str.at abbr 0)) 0) (< (str.to.int (str.at abbr 0)) 0))
		num = (str.to.int (str.at abbr 0))
		if (and (= num 0) (= curr 0))

		curr = (str.to.int (+ (int.to.str curr) (int.to.str num)))
	else
		pos += curr
		curr = 0
		if (>= pos (str.len word))

		if (not (= (str.at word pos) (str.at abbr 0)))

		pos += 1

pos += curr

if (= pos (str.len word))

