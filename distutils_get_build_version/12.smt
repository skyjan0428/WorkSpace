(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *version () String)
(declare-fun *@sp422 () String )
(declare-fun *@sp228 () String )
(define-fun isdigit ((a String)) Bool
 (str.in_re a (re.++ (re.* (str.to_re "0")) (re.* (str.to_re "1")) (re.* (str.to_re "2")) (re.* (str.to_re "3")) (re.* (str.to_re "4")) (re.* (str.to_re "5")) (re.* (str.to_re "6")) (re.* (str.to_re "7")) (re.* (str.to_re "8")) (re.* (str.to_re "9")))))
(assert (not (= (str.indexof *version "MSC v." 0) (- 0 1))  ) )
(assert (= (str.substr *version (+ (str.indexof *version "MSC v." 0) 6) (str.len *version) ) (str.++  *@sp422 " "  *@sp228))  )
(assert (not (not (isdigit (str.substr *@sp422 0 (- (str.len *@sp422) 2)))  ) ) )
(assert (>= (str.len *@sp422) 3)  )
(assert (not (not (isdigit (str.substr *@sp422 2 3 ))  ) ) )
(assert (>= (- (str.to_int (str.substr *@sp422 0 (- (str.len *@sp422) 2))) 6) 13)  )
(assert (>= (str.len *@sp422) 3)  )
(assert (not (= (+ (- (str.to_int (str.substr *@sp422 0 (- (str.len *@sp422) 2))) 6) 1) 6)  ) )
(assert (not (< (+ (- (str.to_int (str.substr *@sp422 0 (- (str.len *@sp422) 2))) 6) 1) 6)  ) )
(assert (> (+ (- (str.to_int (str.substr *@sp422 0 (- (str.len *@sp422) 2))) 6) 1) 7)  )
(assert (not (>= (+ (- (str.to_int (str.substr *@sp422 0 (- (str.len *@sp422) 2))) 6) 1) 8)  ) )
(check-sat)
 (get-model)
