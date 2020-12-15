(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss800 () String )
(declare-fun *@ss8001 () String )
(declare-fun *@ss8000 () String )
(declare-fun *@sstring800 () String )
(declare-fun *@ss994 () String )
(declare-fun *@ss9940 () String )
(declare-fun *@ss9941 () String )
(declare-fun *@sstring994 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss994) 2))  ) )
(assert (not (str.is_digit *@ss9940)  ) )
(assert (str.is_digit *@ss9940)  )
(assert (str.is_digit *@ss9940)  )
(assert (str.is_digit *@ss9941)  )
(assert (not (>= (str.to_int *@ss9940) 1)  ) )
(assert (not (>= (str.to_int *@ss9940) 2)  ) )
(assert (= *version (str.++  *@ss8000 "/"  *@ss8001 *@sstring800 )))
(assert (= *@ss8001 (str.++  *@ss9940 "."  *@ss9941 *@sstring994 )))
(check-sat)
 (get-model)
