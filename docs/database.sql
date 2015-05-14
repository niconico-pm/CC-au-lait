Create Database BST_ScoreTool;
Grant Select, Insert, Update on BST_ScoreTool.* to httpd@localhost;

Use BST_ScoreTool;

Create Table
user(
	UID		serial,
	UserName	varchar(32) Unique NOT NULL,
	NickName	char(32) NULL,
	Comment		char(64) NULL,
	IsPublic	boolean NOT NULL default False,
	PassHash	char(128) NOT NULL,
	PassSalt	char(32) NOT NULL,
	LastUpdate	timestamp NOT NULL default '0000-00-00 00:00:00',

	Primary Key(UID),
	Index (UserName)
) ENGINE=InnoDB;

Create Table
music(
	MusicID		int unsigned,
	Name		varchar(64) NOT NULL,

	Primary Key(MusicID)
) ENGINE=InnoDB;

Create Table
tracks(
	MusicID		int unsigned,
	Difficulty	int,
	Level		int NOT NULL,
	Notes		int unsigned NULL,

	Primary Key(MusicID, Difficulty),
	Foreign Key(MusicID) References music(MusicID)
) ENGINE=InnoDB;

Create Table
updation(
	Count		int,
	UID		bigint unsigned,
	Date		timestamp NOT NULL Default CURRENT_TIMESTAMP,

	Primary Key(Count, UID),
	Foreign Key(UID) References user(UID)
) ENGINE=InnoDB;

Create Table
score(
	UID		bigint unsigned,
	MusicID		int unsigned,
	Difficulty	int,
	UpCount		int,
	Score		int unsigned,
	Medal		int,

	Primary Key(UID, MusicID, Difficulty, UpCount),
	Foreign Key(UID, UpCount) References updation(UID, Count),
	Foreign Key(MusicID) References music(MusicID)
) ENGINE=InnoDB;

Create Trigger
update_user_timestamp
After Insert On updation For Each Row
Update user Set LastUpdate = New.Date Where user.UID = New.UID;
