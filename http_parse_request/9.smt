(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss994 () String )
(declare-fun *@ss9941 () String )
(declare-fun *@ss9940 () String )
(declare-fun *@sstring994 () String )
(declare-fun *@ss532 () String )
(declare-fun *@ss5320 () String )
(declare-fun *@ss5321 () String )
(declare-fun *@sstring532 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss532) 2))  ) )
(assert (str.is_digit *@ss5320)  )
(assert (str.is_digit *@ss5321)  )
(assert (str.is_digit *@ss5320)  )
(assert (str.is_digit *@ss5321)  )
(assert (not (>= (str.to_int *@ss5320) 1)  ) )
(assert (not (>= (str.to_int *@ss5320) 2)  ) )
(assert (= *version (str.++  *@ss9940 "/"  *@ss9941 *@sstring994 )))
(assert (= *@ss9941 (str.++  *@ss5320 "."  *@ss5321 *@sstring532 )))
(check-sat)
 (get-model)
