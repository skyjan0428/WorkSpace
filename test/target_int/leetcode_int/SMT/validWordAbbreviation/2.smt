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
(assert (isDigit (str.at abbr 0))) 
(assert (not (and (= (str.to.int (str.at abbr 0)) 0) (= 0 0))))
(assert (not (isDigit (str.at abbr 1))))
(assert (>= (str.to.int (str.++ "0" (int.to.str (str.to.int (str.at abbr 0))))) (str.len word)))
(check-sat)
(get-model)

