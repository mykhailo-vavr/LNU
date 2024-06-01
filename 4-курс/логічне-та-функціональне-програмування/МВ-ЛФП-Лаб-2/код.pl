first_element([X|_], X).

last_element([X], X).
last_element([_|Tail], X) :- last_element(Tail, X).

prefix(_, []).
prefix([Head|Tail], [Head|X]):- prefix(Tail, X).

n_element(1, [Element | _], Element).
n_element(N, [_|Tail], Element) :-
    N > 1, NewN is N - 1,
    n_element(NewN, Tail, Element).

sum([], 0).
sum([Head|Tail], Sum) :-
    sum(Tail, TailSum),
    Sum is Head + TailSum.

multiply([], 1).
multiply([Head|Tail], Mult) :-
    multiply(Tail, TailMult),
    Mult is Head * TailMult.

max_element([X], X).
max_element([Head|Tail], Max) :-
    max_element(Tail, TailMax),
    (Head >= TailMax -> Max = Head ; Max = TailMax).

min_element([X], X).
min_element([Head|Tail], Min) :-
    min_element(Tail, TailMin),
    (Head =< TailMin -> Min = Head ; Min = TailMin).

is_in_list(X, [ X | _]).
is_in_list(X, [ _ | Tail]) :- is_in_list(X, Tail).