(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss351 () String )
(declare-fun *@ss3511 () String )
(declare-fun *@ss3510 () String )
(declare-fun *@sstring351 () String )
(declare-fun *@ss659 () String )
(declare-fun *@ss6590 () String )
(declare-fun *@ss6591 () String )
(declare-fun *@sstring659 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss659) 2))  ) )
(assert (str.is_digit *@ss6590)  )
(assert (str.is_digit *@ss6591)  )
(assert (str.is_digit *@ss6590)  )
(assert (str.is_digit *@ss6591)  )
(assert (not (>= (str.to_int *@ss6590) 1)  ) )
(assert (>= (str.to_int *@ss6590) 2)  )
(assert (>= (str.to_int *@ss6591) 0)  )
(assert (= *version (str.++  *@ss3510 "/"  *@ss3511 *@sstring351 )))
(assert (= *@ss3511 (str.++  *@ss6590 "."  *@ss6591 *@sstring659 )))
(check-sat)
 (get-model)