(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *ip_str () String)
(declare-fun *@ss303 () String )
(declare-fun *@ss3032 () String )
(declare-fun *@ss3033 () String )
(declare-fun *@ss3030 () String )
(declare-fun *@ss3031 () String )
(declare-fun *@slen010 () String )
(declare-fun *@slen011 () String )
(declare-fun *@slen012 () String )
(declare-fun *@sstring01 () String )
(declare-fun *@slen010 () String )
(declare-fun *@slen011 () String )
(declare-fun *@slen012 () String )
(declare-fun *@slen013 () String )
(declare-fun *@slen014 () String )
(declare-fun *@slen015 () String )
(declare-fun *@slen016 () String )
(declare-fun *@slen017 () String )
(declare-fun *@slen018 () String )
(declare-fun *@slen019 () String )
(declare-fun *@slen170 () String )
(declare-fun *@slen171 () String )
(declare-fun *@slen172 () String )
(declare-fun *@slen173 () String )
(declare-fun *@slen174 () String )
(declare-fun *@slen175 () String )
(declare-fun *@slen176 () String )
(declare-fun *@slen177 () String )
(declare-fun *@sstring303 () String )
(assert (not (= (str.len *ip_str) 0)  ) )
(assert (not (str.contains *@ss3032 ".")  ) )
(assert (not (= (str.len *@ss3033) 0)  ) )
(assert (= (str.len *@ss3032) 0)  )
(assert (= *ip_str (str.++  *@ss3030 ":"  *@ss3031 ":"  *@ss3032 ":"  *@ss3033 *@sstring303 )))
(assert (not (str.contains *@slen010 ":")))
(assert (not (str.contains *@slen011 ":")))
(assert (not (str.contains *@slen012 ":")))
(assert (or (= *@ss303 (str.++  *@slen010  ""))(or (= *@ss303 (str.++  *@slen010  ":" *@slen011  ""))(or (= *@ss303 (str.++  *@slen010  ":" *@slen011  ":" *@slen012  "")) false ))))
(assert (= *ip_str *@ss303)) 
(assert (= *@ss303 (str.++ *@slen010  ":" *@slen011  ":" *@slen012  ":" *@slen013  ":" *@slen014  ":" *@slen015  ":" *@slen016  ":" *@slen017  ":" *@slen018  ":"  *@slen019 *@sstring01  )))
(assert (= *ip_str *@ss303)) 
(assert (= *@ss303 (str.++ *@slen170  ":" *@slen171  ":" *@slen172  ":" *@slen173  ":" *@slen174  ":" *@slen175  ":" *@slen176  ":"  *@slen177  "")))
(assert (= *ip_str *@ss303)) 
(check-sat)
 (get-model)
