(set-option :produce-models true)
(set-logic ALL)

(define-fun isDigit ((a String)) Bool
    (str.in.re a (re.++ (re.* (str.to.re "0")) (re.* (str.to.re "1")) (re.* (str.to.re "2")) (re.* (str.to.re "3")) (re.* (str.to.re "4")) (re.* (str.to.re "5")) (re.* (str.to.re "6")) (re.* (str.to.re "7")) (re.* (str.to.re "8")) (re.* (str.to.re "9")))))

(declare-fun version () String)
(assert (not (= (str.len (version.split("/")[1].split("."))) 2)))
(assert (not (and (not ( isdigit(version.split("/")[1].split(".")[0]))) (isdigit(version.split("/")[1].split(".")[1]))))
(assert (not (= (str.to.int version.split("/")[1].split(".")[0]) (- 0 1))))
(assert (not (= (str.to.int version.split("/")[1].split(".")[1]) (- 0 1))))
(assert (and (>= (str.to.int version.split("/")[1].split(".")[0]) 1) (>= (str.to.int version.split("/")[1].split(".")[0]) 1)))

(check-sat)
(get-model)

