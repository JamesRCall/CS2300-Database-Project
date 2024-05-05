-- Create the database
DROP DATABASE IF EXISTS language_database;
CREATE DATABASE IF NOT EXISTS language_database;
USE language_database;

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
    word_count INTEGER DEFAULT 0,
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
    User_ID INTEGER NOT NULL,
    word_count INTEGER DEFAULT 0,
    Difficulty VARCHAR(64) DEFAULT "Medium",
    primary_language int NOT NULL,
    translated_language int NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (primary_language) REFERENCES Languages(language_id),
    FOREIGN KEY (translated_language) REFERENCES Languages(language_id)
);

CREATE TABLE IF NOT EXISTS Words_In_List (
    List_ID INTEGER,
    Word_ID INTEGER,
    FOREIGN KEY (List_ID) REFERENCES Word_List(List_ID),
    FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID),
    PRIMARY KEY (List_ID, Word_ID)
);

CREATE TABLE User_Learned_Words (
    User_ID int,
    Word_ID int,
    Correct_Amount int DEFAULT 0,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID),
    PRIMARY KEY (User_ID, Word_ID)
);

-- New table for Translations
CREATE TABLE IF NOT EXISTS Translation (
    Translation_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Word_ID INTEGER NOT NULL,
    Word_Language INTEGER NOT NULL,
    Language_ID INTEGER NOT NULL,
    Translated_Text VARCHAR(255) NOT NULL,
    FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID),
    FOREIGN KEY (Word_Language) REFERENCES Languages(language_id),
    FOREIGN KEY (Language_ID) REFERENCES Languages(language_id)
);

-- Now, add foreign key constraints
ALTER TABLE Users ADD CONSTRAINT FK_User_Language FOREIGN KEY (language_id) REFERENCES Languages(language_id);
ALTER TABLE Word ADD CONSTRAINT FK_Word_Language FOREIGN KEY (language_id) REFERENCES Languages(language_id);
ALTER TABLE Word_Definition ADD CONSTRAINT FK_WordDef_Word FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID);

-- Setting up the correct delimiter is crucial in scripts with triggers
DELIMITER //

-- Trigger to increment word_count on new word insertion
CREATE TRIGGER increment_word_count AFTER INSERT ON Word
FOR EACH ROW BEGIN
    UPDATE Languages
    SET word_count = word_count + 1
    WHERE language_id = NEW.language_id;
END;
//

-- Trigger to decrement word_count on word deletion
CREATE TRIGGER decrement_word_count AFTER DELETE ON Word
FOR EACH ROW BEGIN
    UPDATE Languages
    SET word_count = word_count - 1
    WHERE language_id = OLD.language_id;
END;
//

-- Trigger to adjust word_count on updating a word's language_id
CREATE TRIGGER update_word_count AFTER UPDATE ON Word
FOR EACH ROW BEGIN
    IF OLD.language_id != NEW.language_id THEN
        UPDATE Languages SET word_count = word_count - 1 WHERE language_id = OLD.language_id;
        UPDATE Languages SET word_count = word_count + 1 WHERE language_id = NEW.language_id;
    END IF;
END;
//

-- Trigger to update Word_Count on adding a new word to a list
CREATE TRIGGER increment_list_word_count AFTER INSERT ON Words_In_List
FOR EACH ROW BEGIN
    UPDATE Word_List
    SET Word_Count = (SELECT COUNT(*) FROM Words_In_List WHERE List_ID = NEW.List_ID)
    WHERE List_ID = NEW.List_ID;
END;
//

-- Trigger to update Word_Count on deleting a word from a list
CREATE TRIGGER decrement_list_word_count AFTER DELETE ON Words_In_List
FOR EACH ROW BEGIN
    UPDATE Word_List
    SET Word_Count = (SELECT COUNT(*) FROM Words_In_List WHERE List_ID = OLD.List_ID)
    WHERE List_ID = OLD.List_ID;
END;
//

-- Resetting the delimiter to the default
DELIMITER ;