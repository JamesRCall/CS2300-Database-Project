-- Create the database
DROP DATABASE IF EXISTS test5;
CREATE DATABASE IF NOT EXISTS test5;
USE test5;

-- Create tables without foreign key constraints
CREATE TABLE IF NOT EXISTS Users (
    User_ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    phone_number VARCHAR(16),
    email VARCHAR(64) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    password VARCHAR(50) NOT NULL,
    authorization varchar(50),
    default_language VARCHAR(64),
    language_id INTEGER
);

CREATE TABLE IF NOT EXISTS Languages (
    language_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    word_count INTEGER CHECK (word_count >= 0),
    language_name VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS User_Selected_Languages (
    User_ID int,
    Selected_Languages VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS Word (
    Word_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Text TEXT NOT NULL,
    language_id INTEGER
);

CREATE TABLE IF NOT EXISTS Word_Definition (
    Definition_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    text TEXT NOT NULL,
    Word_ID INTEGER
);

CREATE TABLE IF NOT EXISTS Word_List (
    List_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    List_Name VARCHAR(64) NOT NULL,
    Word_Count INTEGER CHECK (Word_Count >= 0),
    User_ID INTEGER NOT NULL,
    primary_language int NOT NULL,
    translated_language int NOT NULL
);

CREATE TABLE IF NOT EXISTS Words_In_List(
    List_ID INTEGER,
    Word_ID INTEGER
);

-- New table for Translations
CREATE TABLE IF NOT EXISTS Translation (
    Translation_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Word_ID INTEGER NOT NULL,
    Translated_Text VARCHAR(255) NOT NULL,
    FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID)
);

-- Now, add foreign key constraints
ALTER TABLE Users ADD CONSTRAINT FK_User_Language FOREIGN KEY (language_id) REFERENCES Languages(language_id);
ALTER TABLE Word ADD CONSTRAINT FK_Word_Language FOREIGN KEY (language_id) REFERENCES Languages(language_id);
ALTER TABLE Word_Definition ADD CONSTRAINT FK_WordDef_Word FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID);
ALTER TABLE Word_List ADD CONSTRAINT FK_WordList_User FOREIGN KEY (User_ID) REFERENCES Users(User_ID);
ALTER TABLE Word_List ADD CONSTRAINT FK_WordList_Default FOREIGN KEY (primary_language) REFERENCES Users(language_id);
ALTER TABLE Words_In_List ADD CONSTRAINT FK_Words_ListID FOREIGN KEY (List_ID) REFERENCES Word_List(List_ID);
ALTER TABLE Words_In_List ADD CONSTRAINT FK_Words_WordID FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID);

-- Insert initial data (ensure this table name matches your schema)
INSERT INTO Languages VALUES(1, 0, 'English');
INSERT INTO Users VALUES (1, '111-222-3333', 'john_appleseed@gmail.com', 'John', 'Appleseed', 'no', 'default', 'English', 1);
