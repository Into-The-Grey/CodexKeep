-- Indexes for Items Table
CREATE INDEX idx_items_name ON Items(Name);

CREATE INDEX idx_items_rarity ON Items(Rarity);

CREATE INDEX idx_items_category_subcategory ON Items(Category, Subcategory);

-- Indexes for Activities Table
CREATE INDEX idx_activities_name ON Activities(Name);

CREATE INDEX idx_activities_type ON Activities(Type);

-- Indexes for Vendors Table
CREATE INDEX idx_vendors_name ON Vendors(Name);

CREATE INDEX idx_vendors_type ON Vendors(Type);

-- Indexes for Locations Table
CREATE INDEX idx_locations_name ON Locations(Name);

CREATE INDEX idx_locations_type ON Locations(Type);

-- Indexes for Quests Table
CREATE INDEX idx_quests_name ON Quests(Name);

CREATE INDEX idx_quests_type ON Quests(Type);

-- Indexes for Collectibles
CREATE INDEX idx_lorebooks_title ON LoreBooks(Title);

CREATE INDEX idx_loreentries_title_content ON LoreEntries USING gin(to_tsvector('english', Title || ' ' || Content));

-- Indexes for Enemies
CREATE INDEX idx_enemies_name ON Enemies(Name);

CREATE INDEX idx_enemies_typeid_zoneid ON Enemies(TypeID, ZoneID);

-- Indexes for Drops
CREATE INDEX idx_enemydrops_enemyid_itemid ON EnemyDrops(EnemyID, ItemID);

CREATE INDEX idx_activitydrops_activityid_itemid ON ActivityDrops(ActivityID, ItemID);

-- Index for Currencies
CREATE INDEX idx_currencies_name ON Currencies(Name);

-- Indexes for Events
CREATE INDEX idx_events_name ON Events(Name);

CREATE INDEX idx_events_dates ON Events(StartDate, EndDate);

-- Indexes for Seasons
CREATE INDEX idx_seasons_name ON Seasons(Name);

CREATE INDEX idx_seasonalitems_seasonid_itemid ON SeasonalItems(SeasonID, ItemID);

CREATE INDEX idx_seasonalactivities_seasonid_activityid ON SeasonalActivities(SeasonID, ActivityID);

