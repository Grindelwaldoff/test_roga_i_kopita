PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS corporation_activity_link;
DROP TABLE IF EXISTS corporation_phones;
DROP TABLE IF EXISTS corporation;
DROP TABLE IF EXISTS building;
DROP TABLE IF EXISTS activity;

CREATE TABLE activity (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES activity (id) ON DELETE RESTRICT
);

CREATE TABLE building (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL UNIQUE,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    CHECK (-90 <= latitude AND latitude <= 90),
    CHECK (-180 <= longitude AND longitude <= 180)
);

CREATE TABLE corporation (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    building_id INTEGER NOT NULL,
    FOREIGN KEY (building_id) REFERENCES building (id) ON DELETE RESTRICT
);

CREATE INDEX ix_corporation_name ON corporation (name);
CREATE INDEX ix_corporation_building_id ON corporation (building_id);

CREATE TABLE corporation_phones (
    id INTEGER PRIMARY KEY,
    corporation_id INTEGER NOT NULL,
    phone_number TEXT NOT NULL,
    CONSTRAINT uq_phone_per_corporation UNIQUE (corporation_id, phone_number),
    FOREIGN KEY (corporation_id)
        REFERENCES corporation (id)
        ON DELETE CASCADE
);

CREATE TABLE corporation_activity_link (
    corporation_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    PRIMARY KEY (corporation_id, activity_id),
    FOREIGN KEY (corporation_id)
        REFERENCES corporation (id)
        ON DELETE CASCADE,
    FOREIGN KEY (activity_id)
        REFERENCES activity (id)
        ON DELETE CASCADE
);

INSERT INTO activity (id, name, parent_id) VALUES
    (1, 'Еда', NULL),
    (2, 'Мясная продукция', 1),
    (3, 'Молочная продукция', 1),
    (4, 'Автомобили', NULL),
    (5, 'Грузовые', 4),
    (6, 'Легковые', 4),
    (7, 'Запчасти', 6),
    (8, 'Аксессуары', 6);

INSERT INTO building (id, address, latitude, longitude) VALUES
    (1, 'г. Москва, ул. Ленина 1, офис 3', 55.751244, 37.618423),
    (2, 'г. Москва, ул. Тверская 10', 55.757394, 37.604188),
    (3, 'г. Санкт-Петербург, Невский пр., 50', 59.935000, 30.327000);

INSERT INTO corporation (id, name, building_id) VALUES
    (1, 'ООО "Рога и Копыта"', 1),
    (2, 'АО "Мясной мир"', 2),
    (3, 'ИП Иванова "Молочная лавка"', 1),
    (4, 'ООО "АвтоПлюс"', 3),
    (5, 'ООО "АвтоСервис"', 3);

INSERT INTO corporation_phones (id, corporation_id, phone_number) VALUES
    (1, 1, '2-222-222'),
    (2, 1, '8-800-100-00-01'),
    (3, 2, '3-333-333'),
    (4, 2, '8-923-666-13-13'),
    (5, 3, '8-495-123-45-67'),
    (6, 4, '8-800-200-30-40'),
    (7, 4, '8-800-200-30-41'),
    (8, 5, '8-812-555-44-33');

INSERT INTO corporation_activity_link (corporation_id, activity_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 2),
    (3, 3),
    (4, 4),
    (4, 6),
    (4, 7),
    (4, 8),
    (5, 4),
    (5, 5);

COMMIT;
PRAGMA foreign_keys = ON;
