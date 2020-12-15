(define-fun-rec  split ((a String) (b String) (c Int)) String
	(ite (= c 0)
		(ite (< (str.indexof a b c) 0) a (str.substr a 0 (str.indexof a b c)))
    	(split (str.substr a (+ (str.indexof a b 0) 1) (str.len a)) b (- c 1))))