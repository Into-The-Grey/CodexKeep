-- Sample Data

-- Insert into Games
INSERT INTO Games (Name, Description) VALUES
('Destiny2', 'Loot-based shooter game by Bungie'),
('Diablo', 'Action RPG by Blizzard'),
('WoW', 'MMORPG by Blizzard');

-- Insert sample items
INSERT INTO Items (GameID, Name, Category, Subcategory, Rarity, Description)
VALUES
(1, 'Gjallarhorn', 'Weapons', 'PowerWeapons', 'Exotic', 'Powerful rocket launcher.'),
(1, 'Ace of Spades', 'Weapons', 'KineticWeapons', 'Exotic', 'Cayde-6’s trusty hand cannon.');
