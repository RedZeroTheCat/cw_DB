INSERT INTO Users (fullname, social_media_link, age, role, playing_since, password_hash) VALUES
('Некрасов Константин', 'https://t.me/Red_The_Cat', 20, 'master', '2020-09-01', '$2b$12$04pPFKKQGYB.QiChKJwfveYz6G4CQlzM2tlHydg655AKTeA6ejIkW'),
('Иван Петров', 'https://vk.com/ivan', 28, 'master', '2015-06-12', 'hashed_password_1'),
('Мария Смирнова', 'https://vk.com/maria', 25, 'user', '2018-04-23', 'hashed_password_2'),
('Алексей Иванов', 'https://vk.com/alex', 30, 'user', '2016-09-18', 'hashed_password_3'),
('Екатерина Соколова', 'https://vk.com/kate', 27, 'user', '2019-01-05', 'hashed_password_4');

INSERT INTO Groups (master_id, group_name, type) VALUES
(1, 'Отряд искателей приключений', 'offline'),
(1, 'Темный культ', 'online');

INSERT INTO GroupMembers (group_id, user_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 4);

INSERT INTO Modules (module_name, system_name, description, group_size) VALUES
('Проклятие древнего храма', 'D&D 5E', 'Исследование заброшенного храма, полное ловушек и загадок.', 4),
('Восстание киборгов', 'Cyberpunk Red', 'Восстание против корпорации в киберпанковом мире.', 5);

INSERT INTO Campaigns (group_id, module_id, duration, status, name) VALUES
(1, 1, 10, 'active', 'Поход в храм'),
(2, 2, 8, 'paused', 'Хакеры против корпорации');

INSERT INTO Sessions (campaign_id, session_date, duration, notes) VALUES
(1, '2024-02-10', 4, 'Первая сессия: Вход в храм и первая ловушка.'),
(1, '2024-02-17', 5, 'Игроки нашли тайную комнату.'),
(2, '2024-02-20', 3, 'Планирование атаки на сервер корпорации.');

INSERT INTO CharacterSheets (user_id, character_name, attributes, background) VALUES
(2, 'Эллиан', 'Сила: 12, Ловкость: 14, Интеллект: 16', 'Маг из королевской академии.'),
(3, 'Торгрим', 'Сила: 18, Ловкость: 10, Интеллект: 8', 'Гном-варвар с темным прошлым.'),
(4, 'Рин', 'Сила: 10, Ловкость: 18, Интеллект: 12', 'Хакер, бывший наемник.');

INSERT INTO Achievements (campaign_id, user_id, name, description, date_awarded) VALUES
(1, 2, 'Первый шаг', 'Первая успешно завершенная сессия.', '2024-02-10'),
(1, 3, 'Охотник за сокровищами', 'Нашел редкий артефакт.', '2024-02-17'),
(2, 4, 'Кибер-революционер', 'Провел успешную атаку на сервер.', '2024-02-20');
