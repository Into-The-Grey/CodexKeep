-- Create Main Games Table
CREATE TABLE Games(
    GameID serial PRIMARY KEY,
    Name varchar(255) NOT NULL,
    Description text
);

-- Placeholder Tables for DiabloDB and WoWDB
CREATE TABLE DiabloDB(
    PlaceholderID serial PRIMARY KEY,
    Name varchar(255) DEFAULT 'Diablo Placeholder'
);

CREATE TABLE WoWDB(
    PlaceholderID serial PRIMARY KEY,
    Name varchar(255) DEFAULT 'WoW Placeholder'
);

-- Full Schema for Destiny2DB
-- 1. Items Table
CREATE TABLE Items(
    ItemID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    Description text,
    Category varchar(50),
    Subcategory varchar(50),
    Rarity varchar(50),
    ImageURL text
);

-- 2. Activities Table
CREATE TABLE Activities(
    ActivityID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    Type VARCHAR(50),
    RecommendedPower int,
    Modifiers jsonb,
    Rewards int REFERENCES Items(ItemID)
);

-- 3. Vendors Table
CREATE TABLE Vendors(
    VendorID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    Type VARCHAR(50),
    LocationID int REFERENCES Locations(LocationID)
);

-- 4. Locations Table
CREATE TABLE Locations(
    LocationID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    Type VARCHAR(50),
    ParentLocation int REFERENCES Locations(LocationID)
);

-- 5. Quests Table
CREATE TABLE Quests(
    QuestID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    Type VARCHAR(50),
    Description text,
    RewardID int REFERENCES Items(ItemID)
);

-- 6. Collectibles Tables
CREATE TABLE LoreBooks(
    BookID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Title varchar(255) NOT NULL,
    Description text
);

CREATE TABLE LoreEntries(
    EntryID serial PRIMARY KEY,
    BookID int REFERENCES LoreBooks(BookID),
    Title varchar(255) NOT NULL,
    Content text
);

-- 7. Enemies Tables
CREATE TABLE EnemyTypes(
    TypeID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    TypeName varchar(255) NOT NULL
);

CREATE TABLE Enemies(
    EnemyID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    TypeID int REFERENCES EnemyTypes(TypeID),
    ZoneID int REFERENCES Locations(LocationID),
    Health int,
    DamageType varchar(50)
);

-- 8. ItemDrops Tables
CREATE TABLE EnemyDrops(
    EnemyDropID serial PRIMARY KEY,
    EnemyID int REFERENCES Enemies(EnemyID),
    ItemID int REFERENCES Items(ItemID),
    DropRate float
);

CREATE TABLE ActivityDrops(
    ActivityDropID serial PRIMARY KEY,
    ActivityID int REFERENCES Activities(ActivityID),
    ItemID int REFERENCES Items(ItemID),
    DropRate float
);

-- 9. Currencies Table
CREATE TABLE Currencies(
    CurrencyID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    Description text,
    Source text
);

-- 10. Events Tables
CREATE TABLE Events(
    EventID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    StartDate date,
    EndDate date,
    Description text
);

CREATE TABLE EventRewards(
    EventRewardID serial PRIMARY KEY,
    EventID int REFERENCES Events(EventID),
    ItemID int REFERENCES Items(ItemID),
    Description text
);

-- 11. Seasons Tables
CREATE TABLE Seasons(
    SeasonID serial PRIMARY KEY,
    GameID int REFERENCES Games(GameID),
    Name varchar(255) NOT NULL,
    StartDate date,
    EndDate date,
    Description text
);

CREATE TABLE SeasonalItems(
    SeasonalItemID serial PRIMARY KEY,
    SeasonID int REFERENCES Seasons(SeasonID),
    ItemID int REFERENCES Items(ItemID),
    Availability text
);

CREATE TABLE SeasonalActivities(
    SeasonalActivityID serial PRIMARY KEY,
    SeasonID int REFERENCES Seasons(SeasonID),
    ActivityID int REFERENCES Activities(ActivityID),
    Description text
);

