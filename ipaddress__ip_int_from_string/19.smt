(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *ip_str () String)
(declare-fun *@ss186 () String )
(declare-fun *@ss1862 () String )
(declare-fun *@ss1863 () String )
(declare-fun *@ss1860 () String )
(declare-fun *@ss1861 () String )
(declare-fun *@slen450 () String )
(declare-fun *@slen451 () String )
(declare-fun *@slen452 () String )
(declare-fun *@sstring98 () String )
(declare-fun *@slen980 () String )
(declare-fun *@slen981 () String )
(declare-fun *@slen982 () String )
(declare-fun *@slen983 () String )
(declare-fun *@slen984 () String )
(declare-fun *@slen985 () String )
(declare-fun *@slen986 () String )
(declare-fun *@slen987 () String )
(declare-fun *@slen988 () String )
(declare-fun *@slen989 () String )
(declare-fun *@slen670 () String )
(declare-fun *@slen671 () String )
(declare-fun *@slen672 () String )
(declare-fun *@slen673 () String )
(declare-fun *@slen674 () String )
(declare-fun *@slen675 () String )
(declare-fun *@slen676 () String )
(declare-fun *@slen677 () String )
(declare-fun *@sstring186 () String )
(assert (not (= (str.len *ip_str) 0)  ) )
(assert (not (str.contains *@ss1862 ".")  ) )
(assert (= (str.len *@ss1863) 0)  )
(assert (= *ip_str (str.++  *@ss1860 ":"  *@ss1861 ":"  *@ss1862 ":"  *@ss1863 *@sstring186 )))
(assert (not (str.contains *@slen450 ":")))
(assert (not (str.contains *@slen451 ":")))
(assert (not (str.contains *@slen452 ":")))
(assert (or (= *@ss186 (str.++  *@slen450  ""))(or (= *@ss186 (str.++  *@slen450  ":" *@slen451  ""))(or (= *@ss186 (str.++  *@slen450  ":" *@slen451  ":" *@slen452  "")) false ))))
(assert (= *ip_str *@ss186)) 
(assert (= *@ss186 (str.++ *@slen980  ":" *@slen981  ":" *@slen982  ":" *@slen983  ":" *@slen984  ":" *@slen985  ":" *@slen986  ":" *@slen987  ":" *@slen988  ":"  *@slen989 *@sstring98  )))
(assert (= *ip_str *@ss186)) 
(assert (= *@ss186 (str.++ *@slen670  ":" *@slen671  ":" *@slen672  ":" *@slen673  ":" *@slen674  ":" *@slen675  ":" *@slen676  ":"  *@slen677  "")))
(assert (= *ip_str *@ss186)) 
(check-sat)
 (get-model)