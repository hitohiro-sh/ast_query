(define (get-var binding)
    (if (null? binding) 
        binding
        (car binding)))

(define (get-val binding)
    (if (null? binding)
        binding
        (cdr binding)))

(define (get-binding var theta)
    (let ((result (assoc var theta)))
        (if result 
            result
            '())))

(define (make-binding var val)
    (cons var val))

(define (occur-check? var exp)
    (cond 
        ((const? exp) #t)
        ((var? exp)
            (if (equal? var exp) #f #t))
        ((occur-check? var (car exp))
        (occur-check? var (cdr exp)))
        (else #f)))

(define (var? pattern)
    (if (symbol? pattern)
        (eq? #\? (string-ref (symbol->string pattern) 0))
        #f))

(define (const? x)
    (and (not (pair? x)) (not (var? x))))


;(define (instantiate exp subst)
;    (cond
;        ((const? exp) exp)
;        ((var? exp)
;            (let* ((bind (get-binding exp subst))
;                    (result (get-val bind)))
;                    (if (null? bind)
;                        exp
;                        result)))
;        (else (cons (instantiate (car exp) subst) 
;                    (instantiate (cdr exp) subst))
;                    )))

(define (instantiate exp subst)
    (letrec ((inst (lambda (exp subst)
        (cond
            ((const? exp) exp)
            ((var? exp)
                (let* ((bind (get-binding exp subst))
                        (result (get-val bind)))
                        (if (null? bind)
                            exp
                            result)))
            (else 
                (cons (inst (car exp) subst) 
                    (inst (cdr exp) subst)))))))
        (inst exp subst)))

(define (subst-compose theta eta)
    (letrec
        ((rho '())
        (compose-a (lambda (var val)
            (let ((new (instantiate val eta)))
                (if (not (equal? var new))
                    (set! rho
                        (cons (make-binding var new) rho))
                    #f))))
        (compose-b (lambda (var val)
            (let ((foo (get-binding var theta)))
                (if (null? foo)
                    (set! rho
                        (cons (make-binding var val) rho))
                    #f)))))
        (for-each
            (lambda (x) (compose-a (get-var x) (get-val x)))
            theta)
        (for-each
            (lambda (x) (compose-b (get-var x) (get-val x)))
            eta)
        rho))

(define (unify p q)
    (letrec 
        ((theta '())
        (unify-aux (lambda (p q theta)
            (cond
                ((eq? theta 'failed) 'failed)
                ((and (var? p) (occur-check? p q))
                    (subst-compose theta (list (make-binding p q))))
                ((and (var? q) (occur-check? q p))
                    (subst-compose theta (list (make-binding q p))))
                ((const? p)
                    (if (const? q)
                        (if (equal? p q)
                            theta
                            'failed)
                        'failed))
                ((const? q) 'failed)
                (else (unify-aux (cdr p) 
                                (cdr q)
                                (unify-aux (instantiate (car p) theta)
                                            (instantiate (car q) theta)
                                            theta)))))))
        (unify-aux p q theta)))
