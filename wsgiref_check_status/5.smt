(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *status () String)
(declare-fun *@ss815 () String )
(declare-fun *@ss8150 () String )
(declare-fun *@sstring815 () String )
(assert (not (= (str.len *@ss8150) 3))  )
(assert (= *status (str.++  *@ss8150 *@sstring815 )))
(check-sat)
 (get-model)