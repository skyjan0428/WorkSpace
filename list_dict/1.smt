(set-option :produce-models true)
 (set-logic ALL)
(assert (not (or (= *a *a)(= *a *b))  ) )
(check-sat)
 (get-model)