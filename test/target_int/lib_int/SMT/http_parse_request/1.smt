(set-option :produce-models true)
(set-logic ALL)
(define-fun min ((a Int) (b Int)) Int
    (ite (<= a b) a b))
(define-fun max ((a Int) (b Int)) Int
    (ite (>= a b) a b))

(define-fun split ((a String) (b String) (c Int)) String
	(ite (< c 1)
    	(str.substr a 0 (str.indexof a b 1))
    	(str.substr a (+ (str.indexof a b c) 1) (str.indexof a b (+ c 1)))))

(declare-fun version () String)
(assert (not (str.prefixof "HTTP/" version)))
(check-sat)
(get-model)
