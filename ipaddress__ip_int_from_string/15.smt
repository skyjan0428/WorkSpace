(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *ip_str () String)
(declare-fun *@ss993 () String )
(declare-fun *@ss9932 () String )
(declare-fun *@ss9933 () String )
(declare-fun *@ss9930 () String )
(declare-fun *@ss9931 () String )
(declare-fun *@slen160 () String )
(declare-fun *@slen161 () String )
(declare-fun *@slen162 () String )
(declare-fun *@sstring47 () String )
(declare-fun *@slen470 () String )
(declare-fun *@slen471 () String )
(declare-fun *@slen472 () String )
(declare-fun *@slen473 () String )
(declare-fun *@slen474 () String )
(declare-fun *@slen475 () String )
(declare-fun *@slen476 () String )
(declare-fun *@slen477 () String )
(declare-fun *@slen478 () String )
(declare-fun *@slen479 () String )
(declare-fun *@slen980 () String )
(declare-fun *@slen981 () String )
(declare-fun *@slen982 () String )
(declare-fun *@slen983 () String )
(declare-fun *@slen984 () String )
(declare-fun *@slen985 () String )
(declare-fun *@slen986 () String )
(declare-fun *@slen987 () String )
(declare-fun *@sstring993 () String )
(assert (not (= (str.len *ip_str) 0)  ) )
(assert (not (str.contains *@ss9932 ".")  ) )
(assert (not (= (str.len *@ss9933) 0)  ) )
(assert (not (= (str.len *@ss9932) 0)  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss9933 0 )))  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss9933 1 )))  ) )
(assert (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss9933 2 )))  )
(assert (= *ip_str (str.++  *@ss9930 ":"  *@ss9931 ":"  *@ss9932 ":"  *@ss9933 *@sstring993 )))
(assert (not (str.contains *@slen160 ":")))
(assert (not (str.contains *@slen161 ":")))
(assert (not (str.contains *@slen162 ":")))
(assert (or (= *@ss993 (str.++  *@slen160  ""))(or (= *@ss993 (str.++  *@slen160  ":" *@slen161  ""))(or (= *@ss993 (str.++  *@slen160  ":" *@slen161  ":" *@slen162  "")) false ))))
(assert (= *ip_str *@ss993)) 
(assert (= *@ss993 (str.++ *@slen470  ":" *@slen471  ":" *@slen472  ":" *@slen473  ":" *@slen474  ":" *@slen475  ":" *@slen476  ":" *@slen477  ":" *@slen478  ":"  *@slen479 *@sstring47  )))
(assert (= *ip_str *@ss993)) 
(assert (= *@ss993 (str.++ *@slen980  ":" *@slen981  ":" *@slen982  ":" *@slen983  ":" *@slen984  ":" *@slen985  ":" *@slen986  ":"  *@slen987  "")))
(assert (= *ip_str *@ss993)) 
(check-sat)
 (get-model)