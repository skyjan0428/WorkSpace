(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun num1 () String)
(declare-fun num2 () String)
(assert (or (= (str.len num1) 0) (<= (str.to.int num1) 0)))
(assert (or (= (str.len num2) 0) (<= (str.to.int num2) 0)))
(assert (>= (- (min (str.len num1) (str.len num2)) 1) 0))
(assert (>= (+ (+ (str.to.int (str.at num1 (- (str.len num1) 1))) (str.to.int (str.at num2 (- (str.len num2) 1)))) 0) 10))
(assert (not (>= (- (min (str.len num1) (str.len num2)) 2) 0)))
(assert (>= (- (str.len num1) 2) 0))
(assert (>= (+ (str.to.int (str.at num1 (- (str.len num1) 1))) 1) 10))
(assert (not (>= (- (str.len num1) 3) 0)))
(assert (>= (- (str.len num2) 3) 0))
(assert (>= (+ (str.to.int (str.at num2 (- (str.len num2) 1))) 1) 10))
(assert (not (>= (- (str.len num1) 4) 0)))
(assert (> (str.len (str.++ (int.to.str (- (+ (+ (str.to.int (str.at num1 (- (str.len num1) 1))) (str.to.int (str.at num2 (- (str.len num2) 1)))) 0) 10)) (>= (+ (str.to.int (str.at num1 (- (str.len num1) 1))) 1) 10) (int.to.str (- (+ (str.to.int (str.at num2 (- (str.len num2) 1))) 1) 10)) '1')) (max((str.len num1) (str.len num2)))))
(check-sat)
(get-model)




res = []
carry = 0
ls = min(str.len num1, str.len num2)
pos = -1

while (>= (- ls pos) 0)
	curr = (+ (+ (str.to.int (str.at num1 (- (str.len num1) 1))) (str.to.int (str.at num2 (- (str.len num2) 1)))) carry)

	if (>= cur 10)
		res += (int.to.str (- curr 10))
		carry = 1
	else
		res += (int.to.str curr)
		carry = 0
	pos -= 1

while (>= (+ pos (str.len num1)) 0)
	curr = (+ (str.to.int (str.at num1 (- (str.len num1) 1))) carry)
	if (>= curr 10)
		res += (int.to.str (- curr 10))
		carry = 1
	else
		res += (int.to.str curr)
		carry = 0
	pos -=1

while (>= (+ pos (str.len num2)) 0)
	curr = (+ (str.to.int (str.at num2 (- (str.len num2) 1))) carry)
	if (>= curr 10)
		res += (int.to.str (- curr 10))
		carry = 1
	else
		res += (int.to.str curr)
		carry = 0
	pos -=1

if (not (= carry 0))
	res += (int.to.str carry)

l_len = max((str.len num1), (str.len num2))

if (> (str.len res) l_len)

else



