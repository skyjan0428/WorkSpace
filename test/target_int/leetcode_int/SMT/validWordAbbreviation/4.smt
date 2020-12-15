(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(define-fun isDigit ((a String)) Bool
    (str.in.re a (re.++ (re.* (str.to.re "0")) (re.* (str.to.re "1")) (re.* (str.to.re "2")) (re.* (str.to.re "3")) (re.* (str.to.re "4")) (re.* (str.to.re "5")) (re.* (str.to.re "6")) (re.* (str.to.re "7")) (re.* (str.to.re "8")) (re.* (str.to.re "9")))))
 
(declare-fun word () String)
(declare-fun abbr () String)
(assert (isDigit "123"))
(check-sat)
(get-model)