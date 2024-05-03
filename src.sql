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
INSERT INTO Languages (word_count, language_name) VALUES (0, 'French');
INSERT INTO Languages (word_count, language_name) VALUES (0, 'Spanish');
INSERT INTO Languages (word_count, language_name) VALUES (0, 'German');
INSERT INTO Languages (word_count, language_name) VALUES (0, 'Japanese');

INSERT INTO Users VALUES (1, '111-222-3333', 'john_appleseed@gmail.com', 'John', 'Appleseed', 'no', 'default', 'English', 1);
INSERT INTO Users (phone_number, email, first_name, last_name, password, authorization, default_language, language_id) 
VALUES ('222-333-4444', 'alice_wonderland@example.com', 'Alice', 'Wonderland', 'secret', 'user', 'French', 2);

INSERT INTO Users (phone_number, email, first_name, last_name, password, authorization, default_language, language_id) 
VALUES ('333-444-5555', 'admin', 'Bob', 'Builder', 'root', 'admin', 'Spanish', 3);

INSERT INTO User_Selected_Languages (User_ID, Selected_Languages) VALUES (1, 'French');
INSERT INTO User_Selected_Languages (User_ID, Selected_Languages) VALUES (2, 'English');

INSERT INTO Word (Text, language_id) VALUES ('Hello', 1);
INSERT INTO Word (Text, language_id) VALUES ('Bonjour', 2);
INSERT INTO Word (Text, language_id) VALUES ('Hola', 3);

INSERT INTO Word_Definition (text, Word_ID) VALUES ('A greeting', 1);
INSERT INTO Word_Definition (text, Word_ID) VALUES ('Salutation en français', 2);

INSERT INTO Word_List (List_Name, Word_Count, User_ID, primary_language, translated_language) VALUES ('Daily Words', 2, 1, 1, 2);
INSERT INTO Word_List (List_Name, Word_Count, User_ID, primary_language, translated_language) VALUES ('Construction Terms', 1, 2, 3, 1);

INSERT INTO Words_In_List (List_ID, Word_ID) VALUES (1, 1);
INSERT INTO Words_In_List (List_ID, Word_ID) VALUES (1, 2);
INSERT INTO Words_In_List (List_ID, Word_ID) VALUES (2, 3);

INSERT INTO Translation (Word_ID, Translated_Text) VALUES (1, 'Bonjour');
INSERT INTO Translation (Word_ID, Translated_Text) VALUES (2, 'Hello');

