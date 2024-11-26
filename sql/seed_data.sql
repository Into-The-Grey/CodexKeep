-- Seed data for Games Table
INSERT INTO Games (Name, Description) VALUES
('Destiny 2', 'A first-person shooter game developed by Bungie.'),
('Diablo', 'An action role-playing hack and slash video game series developed by Blizzard Entertainment.'),
('World of Warcraft', 'A massively multiplayer online role-playing game (MMORPG) released in 2004 by Blizzard Entertainment.');

-- Seed data for Items Table
INSERT INTO Items (GameID, Name, Description, Category, Subcategory, Rarity, ImageURL) VALUES
(1, 'Gjallarhorn', 'A powerful rocket launcher.', 'Weapon', 'Rocket Launcher', 'Exotic', 'https://example.com/gjallarhorn.png'),
(1, 'Ace of Spades', 'A hand cannon.', 'Weapon', 'Hand Cannon', 'Exotic', 'https://example.com/ace_of_spades.png'),
(1, 'Cloak of the Hidden', 'A cloak for hunters.', 'Armor', 'Class Item', 'Legendary', 'https://example.com/cloak_of_the_hidden.png');

-- Seed data for Activities Table
INSERT INTO Activities (GameID, Name, Type, RecommendedPower, Modifiers, Rewards) VALUES
(1, 'Nightfall: The Ordeal', 'Strike', 1050, '{"modifier1": "Match Game", "modifier2": "Champions: Barrier"}', 1),
(1, 'Crucible', 'PvP', 0, '{"modifier1": "Mayhem"}', 2);

-- Seed data for Vendors Table
INSERT INTO Vendors (GameID, Name, Type, LocationID) VALUES
(1, 'Xur', 'NPC', 1),
(1, 'Banshee-44', 'NPC', 2);

-- Seed data for Locations Table
INSERT INTO Locations (GameID, Name, Type, ParentLocation) VALUES
(1, 'The Tower', 'Social', NULL),
(1, 'The Farm', 'Social', NULL);

-- Seed data for Quests Table
INSERT INTO Quests (GameID, Name, Type, Description, RewardID) VALUES
(1, 'The Whisper', 'Exotic Quest', 'Complete the mission to earn the Whisper of the Worm.', 1);

-- Seed data for LoreBooks Table
INSERT INTO LoreBooks (GameID, Title, Description) VALUES
(1, 'The Last Word', 'A book about the legendary weapon.');

-- Seed data for LoreEntries Table
INSERT INTO LoreEntries (BookID, Title, Content) VALUES
(1, 'The Last Word - Chapter 1', 'Excerpt about The Last Word.');

-- Seed data for EnemyTypes Table
INSERT INTO EnemyTypes (GameID, TypeName) VALUES
(1, 'Fallen'),
(1, 'Hive');

-- Seed data for Enemies Table
INSERT INTO Enemies (GameID, Name, TypeID, ZoneID, Health, DamageType) VALUES
(1, 'Dreg', 1, 1, 100, 'Kinetic'),
(1, 'Thrall', 2, 2, 150, 'Arc');

-- Seed data for EnemyDrops Table
INSERT INTO EnemyDrops (EnemyID, ItemID, DropRate) VALUES
(1, 1, 0.05),
(2, 2, 0.10);

-- Seed data for ActivityDrops Table
INSERT INTO ActivityDrops (ActivityID, ItemID, DropRate) VALUES
(1, 1, 0.15),
(2, 2, 0.20);

-- Seed data for Currencies Table
INSERT INTO Currencies (GameID, Name, Description, Source) VALUES
(1, 'Glimmer', 'A form of currency in Destiny 2.', 'General'),
(1, 'Legendary Shards', 'Used to infuse and masterwork gear.', 'General');

-- Seed data for Events Table
INSERT INTO Events (GameID, Name, StartDate, EndDate, Description) VALUES
(1, 'Festival of the Lost', '2023-10-01', '2023-11-01', 'A Halloween-themed event.');

-- Seed data for EventRewards Table
INSERT INTO EventRewards (EventID, ItemID, Description) VALUES
(1, 1, 'Earned during the Festival of the Lost.');

-- Seed data for Seasons Table
INSERT INTO Seasons (GameID, Name, StartDate, EndDate, Description) VALUES
(1, 'Season of the Chosen', '2023-02-01', '2023-05-01', 'A season focused on the Cabal.');

-- Seed data for SeasonalItems Table
INSERT INTO SeasonalItems (SeasonID, ItemID, Availability) VALUES
(1, 1, 'Available during Season of the Chosen.');

-- Seed data for SeasonalActivities Table
INSERT INTO SeasonalActivities (SeasonID, ActivityID, Description) VALUES
(1, 1, 'Nightfall: The Ordeal available during Season of the Chosen.');