(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *ip_str () String)
(declare-fun *@ss023 () String )
(declare-fun *@ss0232 () String )
(declare-fun *@ss0233 () String )
(declare-fun *@ss0230 () String )
(declare-fun *@ss0231 () String )
(declare-fun *@slen510 () String )
(declare-fun *@slen511 () String )
(declare-fun *@slen512 () String )
(declare-fun *@sstring04 () String )
(declare-fun *@slen040 () String )
(declare-fun *@slen041 () String )
(declare-fun *@slen042 () String )
(declare-fun *@slen043 () String )
(declare-fun *@slen044 () String )
(declare-fun *@slen045 () String )
(declare-fun *@slen046 () String )
(declare-fun *@slen047 () String )
(declare-fun *@slen048 () String )
(declare-fun *@slen049 () String )
(declare-fun *@slen110 () String )
(declare-fun *@slen111 () String )
(declare-fun *@slen112 () String )
(declare-fun *@slen113 () String )
(declare-fun *@slen114 () String )
(declare-fun *@slen115 () String )
(declare-fun *@slen116 () String )
(declare-fun *@slen117 () String )
(declare-fun *@sstring023 () String )
(assert (not (= (str.len *ip_str) 0)  ) )
(assert (not (str.contains *@ss0232 ".")  ) )
(assert (not (= (str.len *@ss0233) 0)  ) )
(assert (not (= (str.len *@ss0232) 0)  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss0233 0 )))  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss0233 1 )))  ) )
(assert (not (not (str.contains "0123456789ABCDEFabcdef" (str.at *@ss0233 2 )))  ) )
(assert (not (> (str.len *@ss0233) 4)  ) )
(assert (not (= (str.at *@ss0233 0 ) "a")  ) )
(assert (not (= (str.at *@ss0233 0 ) "A")  ) )
(assert (= (str.at *@ss0233 0 ) "b")  )
(assert (= *ip_str (str.++  *@ss0230 ":"  *@ss0231 ":"  *@ss0232 ":"  *@ss0233 *@sstring023 )))
(assert (not (str.contains *@slen510 ":")))
(assert (not (str.contains *@slen511 ":")))
(assert (not (str.contains *@slen512 ":")))
(assert (or (= *@ss023 (str.++  *@slen510  ""))(or (= *@ss023 (str.++  *@slen510  ":" *@slen511  ""))(or (= *@ss023 (str.++  *@slen510  ":" *@slen511  ":" *@slen512  "")) false ))))
(assert (= *ip_str *@ss023)) 
(assert (= *@ss023 (str.++ *@slen040  ":" *@slen041  ":" *@slen042  ":" *@slen043  ":" *@slen044  ":" *@slen045  ":" *@slen046  ":" *@slen047  ":" *@slen048  ":"  *@slen049 *@sstring04  )))
(assert (= *ip_str *@ss023)) 
(assert (= *@ss023 (str.++ *@slen110  ":" *@slen111  ":" *@slen112  ":" *@slen113  ":" *@slen114  ":" *@slen115  ":" *@slen116  ":"  *@slen117  "")))
(assert (= *ip_str *@ss023)) 
(check-sat)
 (get-model)
