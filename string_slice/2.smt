(set-option :produce-models true)
 (set-logic ALL)
 (declare-fun *a () String)
 (declare-fun *b () String)
(assert (str.contains (str.++ (str.substr *a 1 3) *b) "a")  )
(check-sat)
 (get-model)
