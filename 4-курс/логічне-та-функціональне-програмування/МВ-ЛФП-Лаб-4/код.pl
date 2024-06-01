% Структура для опису книги
% book_info_structure(рік_випуску, рейтинг, жанр).

% Автор (ім'я, прізвище, список написаних ним книг)
author('Дж. Р. Р. Толкін', 'Толкін', [
    book('Володар перснів', book_info_structure(1954, 1, фентезі)),
    book('Хобіт, або Туди і знову назад', book_info_structure(1937, 3, фентезі)),
    book('Сильмарілліон', book_info_structure(1977, 2, фентезі)),
    book('Некрономікон', book_info_structure(1938, 4, жахи)),
    book('Фармер Джайлз з Гему', book_info_structure(1943, 5, гумор)),
    book('Розповідь про Кутулу', book_info_structure(1928, 2, жахи)),
    book('Багаття світлофорів', book_info_structure(1964, 3, гумор)),
    book('Том Бомбаділ', book_info_structure(1962, 4, фентезі)),
    book('Фермір в Бірчовому лісі', book_info_structure(1969, 3, фентезі))
]).

author('Джоан Роулінг', 'Роулінг', [
    book('Гаррі Поттер і філософський камінь', book_info_structure(1997, 4, фентезі)),
    book('Гаррі Поттер і Келих вогню', book_info_structure(2000, 5, фентезі)),
    book('Гаррі Поттер і вязень Азкабану', book_info_structure(1999, 3, фентезі)),
    book('Гаррі Поттер і келих вогню 2', book_info_structure(2000, 4, фентезі)),
    book('Гаррі Поттер і Орден Фенікса', book_info_structure(2003, 5, фентезі)),
    book('Гаррі Поттер і напівкровний принц', book_info_structure(2005, 4, фентезі)),
    book('Гаррі Поттер і смертельні реліквії', book_info_structure(2007, 5, фентезі)),
    book('Квіддич через віки', book_info_structure(2001, 3, фентезі)),
    book('Чудовиська Гаррі Поттера', book_info_structure(2001, 2, фентезі)),
    book('Синдзо Халловен', book_info_structure(1986, 1, детектив))
]).

author('Ернест Хемінгуей', 'Хемінгуей', [
    book('Старий і море', book_info_structure(1952, 4, драма)),
    book('Прощай, зброє!', book_info_structure(1929, 5, роман)),
    book('По ком звонить дзвін', book_info_structure(1940, 3, військовий)),
    book('По той бік раю', book_info_structure(1950, 4, роман)),
    book('На свій манер', book_info_structure(1927, 5, роман)),
    book('Після снігу', book_info_structure(1923, 3, роман)),
    book('Фієста', book_info_structure(1926, 4, роман)),
    book('Зелені холми Африки', book_info_structure(1935, 5, подорож)),
    book('По бік ріки, що несе течію', book_info_structure(1970, 4, подорож)),
    book('До нового світу', book_info_structure(1932, 3, подорож))
]).

% Селектор для отримання року випуску книги
% Отримує об'єкт book із вкладеною структурою book_info_structure та витягує рік випуску книги.
get_book_year(book(_, book_info_structure(Year, _)), Year).

% Селектор для отримання рейтингу книги
get_book_rating(book(_, book_info_structure(_, Rating, _)), Rating).

% Запит для знаходження всіх назв книг, випущених у заданому діапазоні років
find_books_in_year_range(StartYear, EndYear, BookTitles) :-
    % Визначаємо автора та його книги ігноруючи ім'я та прізвище автора
    author(_, _, Books),
    % це вбудований предикат, який знаходить усі можливі значення Title, 
    % що задовольняють умову, описану всередині дужок.
    findall(Title, (
        % перебираємо всі книги автора та витягуємо назву книги та інші дані.
        member(book(Title, Info), Books),
        % Отримуємо рік книги 
        get_book_year(book(_, Info), Year),
        % перевіряємо чи знаходиться він в межах StartYear та EndYear
        between(StartYear, EndYear, Year)
    ), BookTitles).

% Запит для знаходження всіх назв книг з заданим рейтингом
find_books_by_rating(Rating, BookTitles) :-
    % визначаємо автора та його книги 
    author(_, _, Books),
    % Знаходимо усі можливі значення Title, що задовольняють умову, 
    % описану всередині дужок.
    findall(Title, 
            % перебираємо всі книги автора та витягуємо назву книги та інші дані.
            (member(book(Title, Info), Books), 
            % Отримуємо рейтинг книги 
            get_book_rating(book(_, Info), Rating)),
            BookTitles).

% Запит для знаходження всіх книг заданого жанру (рекурсивний)
find_books_by_genre(Genre) :-
    % визначаємо автора та його книги 
    author(Author, _, Books),
    print_books_by_genre(Author, Books, Genre),
    % примушуємо Prolog перейти до наступного варіанту визначення предиката
    % після того, як відбудеться вивід всіх книг поточного автора.
    fail.

% Базовий випадок для рекурсії, який завершує роботу, коли список книг порожній.
print_books_by_genre(_, [], _).
print_books_by_genre(Author, [book(Title, book_info_structure(_, _, Genre)) | Rest], TargetGenre) :-
    (Genre = TargetGenre ->
        writeln(Title)
    % виводимо назву книги, а в іншому випадку продовжується рекурсія.
    ; true),
    print_books_by_genre(Author, Rest, TargetGenre).


% базовий випадок, коли список книг порожній. 
sum_ratings([], 0, 0).
sum_ratings([book(_, book_info_structure(_, Rating, _)) | Tail], Sum, Len) :-
    sum_ratings(Tail, RestSum, RestLen),
    % Рейтинг кожної книги додається до суми 
    Sum is Rating + RestSum,
    % До кількості книг додається 1 
    Len is 1 + RestLen.

average_rating(AuthorName, Average):-
    author(AuthorName, _, Books),
    sum_ratings(Books, Sum, Len),
    Average is Sum / Len.


% Запит для знаходження книги з найвищим рейтингом
find_highest_rated_book(HighestRatedBook) :-
    author(_, _, Books),
    findall(Rating, (
        member(book(_, Info), Books),
        get_book_rating(book(_, Info), Rating)
    ), Ratings),
    max_list(Ratings, MaxRating),
    member(book(HighestRatedBook, book_info_structure(_, MaxRating, _)), Books).