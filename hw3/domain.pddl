(define (domain puzzles)
    (:requirements
        :strips
        :typing
    )
    (:types
        cell ; 16 cells we have
        puzzle ; 15 puzzles we have
    )    
    (:predicates 
        (near ?c1 ?c2 - cell) ; showing where to move kinda
        (empty ?c - cell) ; if there's a puzzle on the cell
        (at ?c - cell ?p - puzzle) ; at which cell puzzle is, or which cell has this puzzle
    )
    (:action move
        :parameters (?p - puzzle ?from ?to - cell) 
        :precondition 
            (and
                (near ?from ?to)
                (at ?from ?p)
                (empty ?to)
            )
        
        :effect
            (and
                (at ?to ?p)
                (empty ?from)
                (not (empty ?to))
                (not (at ?from ?p))
            )
        
    )
)