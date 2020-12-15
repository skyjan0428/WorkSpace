(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@ss494 () String )
(declare-fun *@ss4941 () String )
(declare-fun *@ss4940 () String )
(declare-fun *@sstring494 () String )
(declare-fun *@ss938 () String )
(declare-fun *@ss9380 () String )
(declare-fun *@ss9381 () String )
(declare-fun *@sstring938 () String )
(assert (str.prefixof "HTTP/" *version )  )
(assert (not (not (= (str.len *@ss938) 2))  ) )
(assert (str.is_digit *@ss9380)  )
(assert (str.is_digit *@ss9381)  )
(assert (str.is_digit *@ss9380)  )
(assert (str.is_digit *@ss9381)  )
(assert (>= (str.to_int *@ss9380) 1)  )
(assert (not (>= (str.to_int *@ss9381) 1)  ) )
(assert (>= (str.to_int *@ss9380) 2)  )
(assert (>= (str.to_int *@ss9381) 0)  )
(assert (= *version (str.++  *@ss4940 "/"  *@ss4941 *@sstring494 )))
(assert (= *@ss4941 (str.++  *@ss9380 "."  *@ss9381 *@sstring938 )))
(check-sat)
 (get-model)