-- This file adds test data for the database

-- Use the appropriate database
USE language_database;

-- Inserting data into Languages
INSERT INTO Languages (language_name) VALUES ('English'), ('French'), ('Spanish'), ('German'), ('Japanese');

-- Inserting data into Users
INSERT INTO Users (phone_number, email, first_name, last_name, password, authorization, default_language, language_id) VALUES
('123-456-7890', 'john.doe@example.com', 'John', 'Doe', 'pass123', 'default', 'French', 2),
('234-567-8901', 'admin', 'Jane', 'Smith', 'root', 'admin', 'English', 1),
('345-678-9012', 'emily.jones@example.com', 'Emily', 'Jones', 'hello789', 'CEO', 'Spanish', 3);

-- Inserting data into User_Selected_Languages
INSERT INTO User_Selected_Languages (User_ID, Selected_Languages) VALUES
(1, 'French'),
(2, 'Spanish'),
(3, 'German');

-- Inserting data into Word
INSERT INTO Word (Text, language_id) VALUES
('Hello', 1), ('Bonjour', 2), ('Hola', 3), ('Hallo', 4), ('こんにちは', 5);

-- Adding more English words to the Word table
INSERT INTO Word (Text, language_id) VALUES
('Thank you', 1),    -- Assuming language_id 1 is English
('Goodbye', 1),
('Yes', 1),
('No', 1),
('Good morning', 1);


-- Inserting data into Word_Definition
INSERT INTO Word_Definition (text, Word_ID) VALUES
('A greeting in English', 1),
('A greeting in French', 2),
('A greeting in Spanish', 3),
('A greeting in German', 4),
('A greeting in Japanese', 5);

-- Inserting new word lists
INSERT INTO Word_List (List_Name, User_ID, primary_language, translated_language) VALUES
('English to Spanish', 1, 1, 3),    -- Assuming User 1, English ID is 1, Spanish ID is 3
('English to Japanese', 2, 1, 5);   -- Assuming User 2, English ID is 1, Japanese ID is 5

INSERT INTO Translation (Word_ID, Word_Language, Translated_Text, Language_ID) VALUES
(1, 1, 'Bonjour', 2), -- English to French
(2, 2, 'Hello', 1),   -- French to English
(3, 3, 'Hello', 1),   -- Spanish to English
(4, 4, 'Hello', 1),   -- German to English
(5, 5, 'Hello', 1),   -- Japanese to English
(1, 1, 'Hola', 3),    -- English to Spanish
(1, 1, 'Hallo', 4),   -- English to German
(1, 1, 'こんにちは', 5), -- English to Japanese
(2, 2, 'Hola', 3),    -- French to Spanish
(3, 3, 'Bonjour', 2); -- Spanish to French

-- Inserting translations for the new English words into the Translation table
INSERT INTO Translation (Word_ID, Word_Language, Translated_Text, Language_ID) VALUES
-- English to Japanese translations
(6, 1, 'ありがとう', 5),        -- Thank you
(7, 1, 'さようなら', 5),         -- Goodbye
(8, 1, 'はい', 5),             -- Yes
(9, 1, 'いいえ', 5),            -- No
(10, 1, 'おはよう', 5),         -- Good morning

-- English to Spanish translations
(6, 1, 'Gracias', 3),           -- Thank you
(7, 1, 'Adiós', 3),             -- Goodbye
(8, 1, 'Sí', 3),                -- Yes
(9, 1, 'No', 3),                -- No
(10, 1, 'Buenos días', 3);      -- Good morning

-- Inserting words into the English to Spanish word list
-- Selecting words that are originally in English and have Spanish translations
INSERT INTO Words_In_List (List_ID, Word_ID) SELECT 1, Word_ID FROM Translation WHERE Language_ID = 3 AND Word_Language = 1;

-- Inserting words into the English to Japanese word list
-- Selecting words that are originally in English and have Japanese translations
INSERT INTO Words_In_List (List_ID, Word_ID) SELECT 2, Word_ID FROM Translation WHERE Language_ID = 5 AND Word_Language = 1;

-- Inserting data into User_Learned_Words
INSERT INTO User_Learned_Words (User_ID, Word_ID, Correct_Amount) VALUES
(1, 1, 10),
(1, 2, 8),
(2, 3, 15);

-- Ensure to commit the transaction if required depending on your SQL environment settings
COMMIT;
