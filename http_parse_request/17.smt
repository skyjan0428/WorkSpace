(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss869 () String )
(declare-fun *@ss8691 () String )
(declare-fun *@ss8690 () String )
(declare-fun *@sstring869 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (= (str.len (*@ss8691.split("."))) 2))  )
(assert (= *version (str.++  *@ss8690 "/"  *@ss8691 *@sstring869 )))
(check-sat)
 (get-model)
