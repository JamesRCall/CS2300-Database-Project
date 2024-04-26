CREATE TABLE User (
    USER_ID INTEGER PRIMARY KEY,
    phone_number VARCHAR(16),
    email VARCHAR(64) NOT NULL,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    default_language VARCHAR(64),
    language_id INTEGER,
    FOREIGN KEY (language_id) REFERENCES Language(language_id)
);

CREATE TABLE User_Selected_Languages (
    USER_ID INTEGER,
    Selected_Languages VARCHAR(64) NOT NULL,
    FOREIGN KEY (USER_ID) REFERENCES User(USER_ID)
);

CREATE TABLE Language (
    language_id INTEGER PRIMARY KEY,
    word_count INTEGER CHECK (word_count >= 0),
    language_name VARCHAR(64) NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(USER_ID)
);

CREATE TABLE Word (
    Word_ID INTEGER PRIMARY KEY,
    Text TEXT NOT NULL,
    language_id INTEGER,
    FOREIGN KEY (language_id) REFERENCES Language(language_id)
);

CREATE TABLE Definition (
    Definition_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    Word_ID INTEGER,
    FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID)
);

CREATE TABLE Word_List (
    List_ID INTEGER PRIMARY KEY,
    Word_Count INTEGER CHECK (Word_Count >= 0),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(USER_ID)
);

INSERT INTO User VALUES (1,'111-222-3333','john_appleseed@gmail.com','John','Appleseed','English',1);
--to test run $ sqlite3 test.db < src.sql
--            $ sqlite3 test.db
--            sqlite> SELECT * FROM User;
--to quit     sqlite> .quit
--you can change the name of "test.db" 
