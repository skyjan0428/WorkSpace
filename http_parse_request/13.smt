(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss930 () String )
(declare-fun *@ss9301 () String )
(declare-fun *@ss9300 () String )
(declare-fun *@sstring930 () String )
(declare-fun *@ss354 () String )
(declare-fun *@ss3540 () String )
(declare-fun *@ss3541 () String )
(declare-fun *@sstring354 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss354) 2))  ) )
(assert (str.is_digit *@ss3540)  )
(assert (str.is_digit *@ss3541)  )
(assert (str.is_digit *@ss3540)  )
(assert (str.is_digit *@ss3541)  )
(assert (>= (str.to_int *@ss3540) 1)  )
(assert (not (>= (str.to_int *@ss3541) 1)  ) )
(assert (>= (str.to_int *@ss3540) 2)  )
(assert (not (>= (str.to_int *@ss3541) 0)  ) )
(assert (= *version (str.++  *@ss9300 "/"  *@ss9301 *@sstring930 )))
(assert (= *@ss9301 (str.++  *@ss3540 "."  *@ss3541 *@sstring354 )))
(check-sat)
 (get-model)
