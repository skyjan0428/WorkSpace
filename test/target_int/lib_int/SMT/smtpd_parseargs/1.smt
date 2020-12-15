(set-option :produce-models true)
(set-logic ALL)

(declare-fun arg1 () String)
(declare-fun arg2 () String)
(assert (= (str.len arg1) 0)
(assert (= (str.len arg2) 0)
(check-sat)
(get-model)
