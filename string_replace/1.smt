(set-option :produce-models true)
 (set-logic ALL)
 (declare-fun *a () String)
  (declare-fun *b () String)
(assert (not (str.contains (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace (str.replace *a "A,"  "!" ) "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "A," "!") "ABC")  ))
(assert (not (str.contains (str.replace *b " "  "" ) " ")  ) )
(check-sat)
 (get-model)