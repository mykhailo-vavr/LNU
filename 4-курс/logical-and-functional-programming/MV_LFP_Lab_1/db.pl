% unary facts

male(yevgen).
male(ivan).
male(igor).
male(svyatoslav).
male(volodymyr).
male(mykhailo).
male(andriy).
male(taras).

female(nadya).
female(kateryna).
female(olga).
female(galyna).
female(natalya).
female(olena).
female(svitlana).
female(julia).
female(karolina).
female(tetyana).
female(anastasya).

% binary facts

parent(yevgen, olga).
parent(nadya, olga).
parent(ivan, igor).
parent(kateryna, igor).
parent(ivan, svyatoslav).
parent(kateryna, svyatoslav).

parent(igor, volodymyr).
parent(olga, volodymyr).
parent(igor, natalya).
parent(olga, natalya).
parent(igor, mykhailo).
parent(olga, mykhailo).
parent(svyatoslav, andriy).
parent(galyna, andriy).

parent(taras, julia).
parent(natalya, julia).
parent(volodymyr, tetyana).
parent(svitlana, tetyana).
parent(volodymyr, anastasya).
parent(svitlana, anastasya).
parent(andriy, karolina).
parent(olena, karolina).

% rules

child(X, Y) :-
    parent(Y, X).

sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y).

sister(X, Y) :-
    female(X),
    sibling(X, Y).

uncle(X, Y) :-
    male(X),
    parent(Z, Y),
    sibling(X, Z).

cousin(X, Y) :-
    parent(Z, X),
    parent(W, Y),
    sibling(Z, W).

grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

% recurscive rules

ancestor(X, Y) :-
    parent(X, Y).
ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).

descendant(X, Y) :-
    parent(Y, X).
descendant(X, Y) :-
    parent(Y, Z),
    descendant(X, Z).







