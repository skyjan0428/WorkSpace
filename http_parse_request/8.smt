(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss762 () String )
(declare-fun *@ss7621 () String )
(declare-fun *@ss7620 () String )
(declare-fun *@sstring762 () String )
(declare-fun *@ss870 () String )
(declare-fun *@ss8700 () String )
(declare-fun *@sstring870 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss870) 2))  ) )
(assert (not (str.is_digit *@ss8700)  ) )
(assert (not (str.is_digit *@ss8700)  ) )
(assert (= *version (str.++  *@ss7620 "/"  *@ss7621 *@sstring762 )))
(assert (= *@ss7621 (str.++  *@ss8700 *@sstring870 )))
(check-sat)
 (get-model)
