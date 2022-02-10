; '(and a b)  -> '(a b)
; 'a          -> '((and a x))
; 'b          -> '((and x b))
; '(or a b)   -> '(a)
; '(or a b)   -> '(b)
; 'c          -> '((or x y) (leaf x c) (leaf y c))
; '(then a b) -> '((leaf a b))
; 'b          -> '((then x b) x)
; '(not a)    -> '((leaf a #f))
; #f          -> '((not x) x)
; a           -> '((leaf (not a) #f))
; a           -> #f

; tree: ('tree exp childs)
; childs: (tag (tree...))
(define (tree? tree) (and (pair? tree) (eq? 'tree (car tree))))
(define (tree-val tree) 
  (if (tree? tree)
      (car (cdr tree))
      tree))
(define (tree-has-child? tree)
  (if (tree? tree)
      (not (null? (cdr (cdr tree))))
      #f))
(define (tree-childs tree) (car (cdr (cdr tree))))
(define (tree-childs-tag tree) (car (tree-childs tree)))
(define (tree-childs-trees tree) (car (cdr (tree-childs tree))))
(define (tree-leafs tree func)
  (if (tree-has-child? tree)
      ( (lambda (exp) (tree-leafs exp
                                     (lambda (x) (func (tree-val x))))) 
           (tree-childs-trees tree))
      (func (tree-val tree))))
(define (tree-make exp childs) (list 'tree exp childs))
(define (tree-make-1 exp) (list 'tree exp))


; '(and a b)  -> '(a b)
(define (match-and-i exp) 
  (if (and (pair? exp) (eq? 'and (car exp)))
      (list 'and-i (list (car (cdr exp)) (car (cdr (cdr exp)))))
      '()))

; 'a          -> '((and a x))
(define (match-and-e-1 exp)
  (list 'and-e (list (list 'and exp '?x)))
)

; 'b          -> '((and x b))
(define (match-and-e-2 exp)
  (list 'and-e (list (list 'and '?x exp)))
)

; '(or a b)   -> '(a)
(define (match-or-i-1 exp)
  (if (and (pair? exp) (eq? 'or (car exp)))
      (list 'or-i (list (car (cdr exp))))
      '()))

; '(or a b)   -> '(b)
(define (match-or-i-2 exp)
  (if (and (pair? exp) (eq? 'or (car exp)))
      (list 'or-i (list (car (cdr (cdr exp)))))
      '()))

; 'c          -> '((or x y) (leaf x c) (leaf y c))
(define (match-or-e exp)
  (list 'or-e (list '(or ?x ?y) (list 'leaf '?x exp) (list 'leaf '?y exp))))

; '(then a b) -> '((leaf a b))
(define (match-then-i exp)
  (if (and (pair? exp) (eq? 'then (car exp)))
      (list 'then-i (list (list 'leaf (car (cdr exp)) (car (cdr (cdr exp))))))
      '()))

; 'b          -> '((then x b) x)
(define (match-then-e exp)
  (list 'then-e (list (list 'then '?x exp) '?x)))

; '(not a)    -> '((leaf a #f))
(define (match-not-i exp)
  (if (and (pair? exp) (eq? 'not (car exp)))
      (list 'not-i (list 'leaf (car (cdr exp)) #f))
      '()))

; #f          -> '((not x) x)
(define (match-not-e exp)
  (if (eq? #f exp)
      (list 'not-e (list (list '(not ?x) '?x)))
      '()))

; a           -> '((leaf (not a) #f))
(define (match-negation exp)
  (list 'negation (list (list 'leaf (list 'not exp) #f))))

; a           -> #f
(define (match-falsehood exp)
  (list 'falsehood (list #f)))

(define (atom? exp)
  (not (pair? exp)))

(define (choose-list exp)
  (if (atom? exp) 
    (list exp)
    (append 
      (list exp)
      (if (and (pair? exp) (> (length exp) 1))
        (choose-list (car (cdr exp))) '())
      (if (and (pair? exp) (> (length exp) 2))
          (choose-list (car (cdr (cdr exp)))) '()))))


(define (deduction-1 exp)
  (remove
    null?
    (list 
      (match-and-i exp) 
      (match-and-e-1 exp)
      (match-and-e-2 exp)
      (match-or-i-1 exp)
      (match-or-i-2 exp)
      (match-or-e exp)
      (match-then-i exp)
      (match-then-e exp)
      (match-not-i exp)
      (match-not-e exp)
      (match-negation exp)
      (match-falsehood exp))))

(define (deduction-tree tree)
  (if (tree-has-child? tree)
      '(TODO)
      (let ((exps-with-tag (deduction-1 (tree-val tree))))
        (map (lambda (exp) (tree-make (tree-val tree) exp)) exps-with-tag))))

; exp: conclution
; ass: assumptions
(define (deduction exp ass)
    '(TODO))

(for-each print (choose-list '(or (and (not a) b) (not c))))

(for-each print (deduction-1 '(and a b)))
(for-each print (deduction-1 '(or a b)))
(for-each print (deduction-tree '(or a b)))
;(print (map tree-val (deduction-tree '(or a b))))
;(for-each print (map tree-childs-trees (deduction-tree '(or a b))))
(for-each print (map (lambda (tree) (tree-leafs tree (lambda (x) x))) (deduction-tree '(or a b))))
;(for-each print (map (lambda (tree) (tree-leafs tree (lambda (x) (deduction-tree x)))) (deduction-tree '(or a b))))


