(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *ip_str () String)
(declare-fun *@ss337 () String )
(declare-fun *@ss3372 () String )
(declare-fun *@ss3373 () String )
(declare-fun *@ss3370 () String )
(declare-fun *@ss3371 () String )
(declare-fun *@slen450 () String )
(declare-fun *@slen451 () String )
(declare-fun *@slen452 () String )
(declare-fun *@sstring89 () String )
(declare-fun *@slen890 () String )
(declare-fun *@slen891 () String )
(declare-fun *@slen892 () String )
(declare-fun *@slen893 () String )
(declare-fun *@slen894 () String )
(declare-fun *@slen895 () String )
(declare-fun *@slen896 () String )
(declare-fun *@slen897 () String )
(declare-fun *@slen898 () String )
(declare-fun *@slen899 () String )
(declare-fun *@slen850 () String )
(declare-fun *@slen851 () String )
(declare-fun *@slen852 () String )
(declare-fun *@slen853 () String )
(declare-fun *@slen854 () String )
(declare-fun *@slen855 () String )
(declare-fun *@slen856 () String )
(declare-fun *@slen857 () String )
(declare-fun *@sstring337 () String )
(assert (not (= (str.len *ip_str) 0)  ) )
(assert (not (str.contains *@ss3372 ".")  ) )
(assert (not (= (str.len *@ss3373) 0)  ) )
(assert (not (= (str.len *@ss3372) 0)  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss3373 0 )))  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss3373 1 )))  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss3373 2 )))  ) )
(assert (not (> (str.len *@ss3373) 4)  ) )
(assert (not (= (str.at *@ss3373 0 ) "a")  ) )
(assert (not (= (str.at *@ss3373 0 ) "A")  ) )
(assert (not (= (str.at *@ss3373 0 ) "b")  ) )
(assert (not (= (str.at *@ss3373 0 ) "B")  ) )
(assert (not (= (str.at *@ss3373 0 ) "c")  ) )
(assert (not (= (str.at *@ss3373 0 ) "C")  ) )
(assert (= (str.at *@ss3373 0 ) "d")  )
(assert (= *ip_str (str.++  *@ss3370 ":"  *@ss3371 ":"  *@ss3372 ":"  *@ss3373 *@sstring337 )))
(assert (not (str.contains *@slen450 ":")))
(assert (not (str.contains *@slen451 ":")))
(assert (not (str.contains *@slen452 ":")))
(assert (or (= *@ss337 (str.++  *@slen450  ""))(or (= *@ss337 (str.++  *@slen450  ":" *@slen451  ""))(or (= *@ss337 (str.++  *@slen450  ":" *@slen451  ":" *@slen452  "")) false ))))
(assert (= *ip_str *@ss337)) 
(assert (= *@ss337 (str.++ *@slen890  ":" *@slen891  ":" *@slen892  ":" *@slen893  ":" *@slen894  ":" *@slen895  ":" *@slen896  ":" *@slen897  ":" *@slen898  ":"  *@slen899 *@sstring89  )))
(assert (= *ip_str *@ss337)) 
(assert (= *@ss337 (str.++ *@slen850  ":" *@slen851  ":" *@slen852  ":" *@slen853  ":" *@slen854  ":" *@slen855  ":" *@slen856  ":"  *@slen857  "")))
(assert (= *ip_str *@ss337)) 
(check-sat)
 (get-model)
