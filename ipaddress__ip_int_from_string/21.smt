(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *ip_str () String)
(declare-fun *@ss268 () String )
(declare-fun *@ss2682 () String )
(declare-fun *@ss2680 () String )
(declare-fun *@ss2681 () String )
(declare-fun *@slen260 () String )
(declare-fun *@slen261 () String )
(declare-fun *@slen262 () String )
(declare-fun *@sstring25 () String )
(declare-fun *@slen250 () String )
(declare-fun *@slen251 () String )
(declare-fun *@slen252 () String )
(declare-fun *@slen253 () String )
(declare-fun *@slen254 () String )
(declare-fun *@slen255 () String )
(declare-fun *@slen256 () String )
(declare-fun *@slen257 () String )
(declare-fun *@slen258 () String )
(declare-fun *@slen259 () String )
(declare-fun *@sstring268 () String )
(assert (not (= (str.len *ip_str) 0)  ) )
(assert (not (str.contains *@ss2682 ".")  ) )
(assert (= *ip_str (str.++  *@ss2680 ":"  *@ss2681 ":"  *@ss2682 *@sstring268 )))
(assert (not (str.contains *@slen260 ":")))
(assert (not (str.contains *@slen261 ":")))
(assert (not (str.contains *@slen262 ":")))
(assert (not (or (= *@ss268 (str.++  *@slen260  ""))(or (= *@ss268 (str.++  *@slen260  ":" *@slen261  ""))(or (= *@ss268 (str.++  *@slen260  ":" *@slen261  ":" *@slen262  "")) false )))))
(assert (= *ip_str *@ss268)) 
(assert (= *@ss268 (str.++ *@slen250  ":" *@slen251  ":" *@slen252  ":" *@slen253  ":" *@slen254  ":" *@slen255  ":" *@slen256  ":" *@slen257  ":" *@slen258  ":"  *@slen259 *@sstring25  )))
(assert (= *ip_str *@ss268)) 
(check-sat)
 (get-model)
