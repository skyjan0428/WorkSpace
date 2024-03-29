(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss601 () String )
(declare-fun *@ss6011 () String )
(declare-fun *@ss6010 () String )
(declare-fun *@sstring601 () String )
(declare-fun *@ss570 () String )
(declare-fun *@ss5700 () String )
(declare-fun *@ss5701 () String )
(declare-fun *@sstring570 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss570) 2))  ) )
(assert (not (str.is_digit *@ss5700)  ) )
(assert (str.is_digit *@ss5700)  )
(assert (str.is_digit *@ss5700)  )
(assert (str.is_digit *@ss5701)  )
(assert (not (>= (str.to_int *@ss5700) 1)  ) )
(assert (>= (str.to_int *@ss5700) 2)  )
(assert (not (>= (str.to_int *@ss5701) 0)  ) )
(assert (= *version (str.++  *@ss6010 "/"  *@ss6011 *@sstring601 )))
(assert (= *@ss6011 (str.++  *@ss5700 "."  *@ss5701 *@sstring570 )))
(check-sat)
 (get-model)
