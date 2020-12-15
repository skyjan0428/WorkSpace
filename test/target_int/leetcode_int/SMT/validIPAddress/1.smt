(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))
(declare-fun IP () String)
(assert (str.contains IP "."))
(assert (not (= (str.len (IP.split("."))) 4)))
(assert (or (or (not (IP.split("."))[0].isdigit()) (> (str.to.int (IP.split("."))[0]) 255)) (and ( = IP.split(".")[0][0] "0") (> str.len (IP.split(".")[0]) 1))))
(check-sat)
(get-model)
