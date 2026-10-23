USE library;

INSERT INTO AUTHOR (name, country) VALUES
('AUTHOR 1', 'Egypt'),
('AUTHOR 2', 'Egypt'),
('AUTHOR 3', 'Egypt');

INSERT INTO BOOK (title, price, author_id) VALUES
('BOOK 1', 10.5, 1),
('BOOK 2', 20, 1),
('BOOK 3', 100, 2),
('BOOK 4', 150, 2),
('BOOK 5', 999.99, 3),
('BOOK 6', 111.11, 3);