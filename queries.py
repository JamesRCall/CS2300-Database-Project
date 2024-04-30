import mysql.connector
from enum import Enum

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password = "root",
    database = "test5"
)

mycursor = db.cursor()

def Sinput(text: str):
    x = input(f'{text} (press 0 to quit): ')
    if x == '0':
        quit()
    return x

def menu():
    User_ID = start()
    mycursor.execute("SELECT authorization FROM Users WHERE User_ID = %s", (User_ID,))
    user = mycursor.fetchone()
    authorization, = user
    super_user = False
    print("""
           1 Language Options
           2 Word & Definition Options
           3 Translation Options
           4 User Hub
           5 Learn Hub""")
    if authorization == 'admin' or authorization == 'CEO':
        print("\n6 Admin Panel")
        super_user = True
    choice = Sinput("Please select an option")
    if choice == '1':
        Language_Hub(User_ID)
    elif choice == '2':
        Word_Hub(User_ID)
    elif choice == '3':
        Translation_Hub(User_ID)
    elif choice == '4':
        User_Hub(User_ID)
    elif choice == '5':
        Learn_Hub(User_ID)
    elif choice == '6' and super_user == True:
        Admin_Panel(User_ID)
    else:
        print("Invalid input. Please try again.")


def Language_Hub(User_ID):
    while True:
        choice = Sinput("""
        Language Options:
        1. Show All Languages
        2. Search for a Language                
        3. Go Back
        Choose an option""")
        if choice == '1':
            show_languages()
        elif choice == '2':
            print("")
            # TODO: Language_Search()
        elif choice == '3':
            break
        else:
            print("Invalid input. Please try again.")


def Word_Hub(User_ID):
    while True:
        choice = Sinput("""
        Word & Definition Options:
        1. Add New Word
        2. Delete a Word
        3. Edit a Word  
        4. Search for a Word
        5. Add Definition to a Word                              
        6. Delete a Definition
        7. Edit a Definition
        8. Go Back
        Choose an option""")
        if choice == '1':
            Add_word()
        elif choice == '2':
            word = Sinput("Enter the word to delete:")
            # TODO: delete_word(word)
        elif choice == '3':
            word = Sinput("Enter the word to edit:")
            # TODO: edit_word(word)
        elif choice == '4':
            Add_definition()
        elif choice == '5':
            Delete_Definition()
        elif choice == '6':
            Modify_Definition()
        elif choice == '7':
            print('')
            Word_Search()
        elif choice == '8':
            break
        else:
            print("Invalid input. Please try again.")


def Translation_Hub(User_ID):
    while True:
        choice = Sinput("""
        Translation Options:
        1. Add Translation for a Word
        2. Delete Translation for a Word
        3. Edit Translation for a Word
        4. Go Back
        Choose an option""")
        if choice == '1':
            word = Sinput("Enter the word to translate:")
            add_translation(word)
        elif choice == '2':
            word = Sinput("Enter the word to delete its translation:")
            delete_translation(word)
        elif choice == '3':
            word = Sinput("Enter the word to edit its translation:")
            edit_translation(word) 
        elif choice == '4':
            break
        else:
            print("Invalid input. Please try again.")

def User_Hub(User_ID):
    while True:
        choice = Sinput("""
        User Hub:
        1. View My Profile
        2. Edit My Settings
        3. Show My Learning Languages
        4. Learn a New Language
        5. Remove a Language I'm Learning
        6. Go Back
        Choose an option""")
        if choice == '1':
            print("")
            # TODO: View_Profile(User_ID)
        elif choice == '2':
            print("")
            # TODO: edit_user_settings(User_ID)
        elif choice == '3':
            print("")
            # TODO: show_user_languages(User_ID)
        elif choice == '4':
            Choose_Language(User_ID)
        elif choice == '5':
            language = Sinput("Enter the language to remove from your learning list:")
            # TODO: remove_user_language(User_ID, language)
        elif choice == '6':
            break
        else:
            print("Invalid input. Please try again.")

def Learn_Hub(User_ID):
    while True:
        choice = Sinput("""
        Learn Hub:
        1. Review Learned Words # TODO
        2. Practice New Vocabulary # TODO
        3. Track Learning Progress # TODO
        4. Make a Word List
        5. Add words to Word List
        6. Remove words from Word List
        7. Delete a Word List
        8. Edit a Word List
        9. Go Back
        Choose an option""")
        if choice == '1':
            print("")
            # TODO: review_learned_words(User_ID)
        elif choice == '2':
            print("")
            # TODO: practice_new_vocabulary(User_ID)
        elif choice == '3':
            print("")
            # TODO: track_learning_progress(User_ID)
        elif choice == '4':
            make_wordList(User_ID)
        elif choice == '5':
            print("")
            # TODO: add_word_to_list(User_ID, Word_List)
        elif choice == '6':
            print("")
            # TODO: remove_word_from_list(User_ID, Word_List)
        elif choice == '7':
            print("")
            # TODO: delete_wordList(User_ID)
        elif choice == '8':
            print("")
            # TODO: edit_wordList(User_ID)
        elif choice == '9':
            break
        else:
            print("Invalid input. Please try again.")

def Admin_Panel(User_ID):
    while True:
        choice = Sinput("""
        Admin Panel:
        1. Add New Language
        2. Delete a Language
        3. Edit a Language
        4. Show Users
        5. Add_User
        6. Delete Users
        7. Edit Users
        8. User Search
        9. Go Back
        Choose an option""")
        if choice == '1':
            Add_language()
        elif choice == '2':
            language = Sinput("Enter the language to delete:")
            # TODO: delete_language(language)
        elif choice == '3':
            language = Sinput("Enter the language to edit:")
            # TODO: edit_language(language)
        elif choice == '4':
            Show_Users()
        elif choice == '5':
            Add_User(True)
        elif choice == '6':
            print('')
            # TODO: Delete_User()
        elif choice == '7':
            print('')
            # TODO: Edit_User()
        elif choice == '8':
            print('')
            # TODO: User_Search()
        elif choice == '9':
            break

        else:
            print("Invalid input. Please try again.")


"""______________________LOGIN FUNCTIONS________________________
start(): prompts user for logging in or signing up
login(): logs an existing user in
signup(): creates a new user

"""
def start():
    User_ID = None
    while User_ID == None:
        choice = input("Please choose login(1) or sign-up(2) or quit(0):")
        if choice == '0':
            quit()
        elif choice == '1':
            User_ID = login()
            if User_ID == None:
                print("Error logging in, try again.")
        elif choice == '2':
            User_ID = signup()
            if User_ID == None:
                print("Error logging in, try again.")
        else:
            print("Error, invalid input. Try again.")
    return User_ID

def login():
    while True:
        email = Sinput("Please enter your email")

        # Fetch user by email
        mycursor.execute("SELECT User_ID, password FROM Users WHERE email = %s", (email,))
        user = mycursor.fetchone()
        if user is None:
            print("Error, that email does not exist.")
            continue

        User_ID, correct_password = user

        # Check password
        attempts = 0
        while attempts < 3:
            pswd = Sinput("Please enter your password")

            if pswd == correct_password:
                print("Login successful!")
                return User_ID  # Successfully logged in, return the User_ID

            attempts += 1
            print(f"Error, password incorrect. {3 - attempts} Attempts left.")

        if attempts >= 3:
            print("Account locked due to too many failed attempts.")
            quit()
    
def signup():
    new = 0
    while new == 0:
        email = Sinput("Enter your email")
        mycursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        if mycursor.fetchone():
            print(f"Error, email already exists. Please use a different email.")
        else:
            new += 1
            phone_number = Sinput("Enter your phone number")
            first_name = Sinput("Enter your first name")
            last_name = Sinput("Enter your last name")
            password = Sinput("Enter your password")
            authorization = 'default'
            valid = 0
            while valid == 0:
                default_language = Sinput("Enter your default language")
                mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (default_language,))
                language_id = mycursor.fetchone()
                if language_id != None:
                    language_id = language_id[0]
                    valid += 1
                else:
                    print("Error, Invalid language here are the current supported languages: ")
                    show_languages()

            User_ID = Add_User(False, phone_number, email, first_name, last_name, password, authorization, default_language, language_id)
    choice = input("Would you like to add a new language to learn? (1 yes 0 no): ")
    if choice == '1':
        Choose_Language(User_ID)
    return User_ID

"""_________________________LANGUAGE FUNCTIONS__________________________
show_languages(): Shows all Languages
# TODO: Language_Search(): searches for languages based on id or text

"""
def show_languages():
    print("language ID, Word Count, Language Name")
    mycursor.execute("SELECT * FROM Languages")
    for x in mycursor:
        print(x)

def Language_Search(): # TODO
    print("Not implemented yet.")
    return

"""_____________________________WORD & DEFINITION FUNCTIONS___________________________________
Add_word(): adds a new word
TODO Delete_word(): deletes an existing word
TODO Edit_word(): edits an existing word
Word_Search(): searches for a word (either using id or text)
Add_definition(): adds a new definition
Delete_Definition(): deletes an existing definition
Modify_Definition(): edits an existing definition

"""
def Add_word():
    found = 0
    while found == 0:
        language = Sinput("Choose a language for your word")
        mycursor.execute("SELECT language_id FROM Languages WHERE language_name = (%s)", (language,))
        for x in mycursor:
            found += 1
            language_id = x[0]
        if found == 0:
            print("Error, that language does not exist.")
    new = 0
    while new == 0:
        text = Sinput("Type your word")      
        mycursor.execute("SELECT * FROM Word WHERE Text = %s", (text,))
        if mycursor.fetchone():
            print(f"Error, Word already exist. Try again.")
        else:
            new += 1
    try: 
        mycursor.execute("""
            INSERT INTO Word (text, language_id)
            VALUES (%s, %s)
            """, (text, language_id))
        mycursor.execute("UPDATE Languages SET word_count = word_count + 1 WHERE language_id = %s", (language_id,))
        word_id = mycursor.lastrowid
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
        return err

    choice = input("word added successfully! would you like to add a definition? (1 for yes 0 for no): ")
    if choice == 0:
       db.commit()
    else: 
        Add_definition(word_id)

def Delete_word(): # TODO
    print("Not implemented yet.")
    return

def Edit_word(): # TODO
    print("Not implemented yet.")
    return

def Word_Search():
    print("Choose the search type:")
    print("1. Search by Word ID")
    print("2. Search by Word Text")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # Search by Word ID
        word_id = input("Enter the Word ID: ")
        try:
            word_id = int(word_id)  # Ensuring the input is an integer
            mycursor.execute("SELECT * FROM Word WHERE Word_ID = %s", (word_id,))
            result = mycursor.fetchone()
            if result:
                print("Word Found: ID:", result[0], "Text:", result[1])
            else:
                print("No word found with ID:", word_id)
        except ValueError:
            print("Invalid input! Please enter a valid integer for Word ID.")
        except mysql.connector.Error as err:
            print("Error: ", err)
    elif choice == '2':
        # Search by Word Text
        word_text = input("Enter part of the word text to search: ")
        mycursor.execute("SELECT * FROM Word WHERE Text LIKE %s", ('%' + word_text + '%',))
        results = mycursor.fetchall()
        if results:
            print("Words found:")
            for word in results:
                print("ID:", word[0], "Text:", word[1])
        else:
            print("No words found containing:", word_text)
    else:
        print("Invalid choice. Please select either 1 or 2.")

def Add_definition(word_id: int = None):
    while word_id == None:
        word = Sinput("Enter the word you'd like to add a definition to")
        mycursor.execute("SELECT Word_ID FROM Languages WHERE language_name = (%s)", (word,))
        word_id = mycursor.fetchone()
        if word_id == None:
            print("Error, that word does not exist.")
    new = 0
    while new == 0:
        definition = Sinput("Enter your word's definition")      
        if definition == '0':
            quit()
        mycursor.execute("SELECT * FROM Word_Definition WHERE text = %s AND Word_ID = %s", (definition, word_id))
        if mycursor.fetchone():
            print(f"Error, definition already exist. Try again.")
        else:
            new += 1
    try: 
        mycursor.execute("""
            INSERT INTO Word_Definition (text, Word_ID)
            VALUES (%s, %s)
            """, (definition, word_id))
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
        return err
    
    choice = input("Definition added successfully! [press ENTER]")
    if choice == 1:
       db.commit()

def Modify_Definition():
    # CHANGE: User enters a word. The word's definition and definition id's are printed. User chooses the definition id
    #         to modify
    word_name = input("Enter the word that you want to modify its definition: ")
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=%s", (word_name,))
    word_id = mycursor.fetchone()
    if word_id is not None:
      word_id = word_id[0]
      print("Definition ID, Definition")
      mycursor.execute("SELECT Definition_id, text FROM Word_Definition WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      definition_id = input("Enter the definition id to modify: ")
      # NOTE: Might want to change logic to list defintions of a word and choose based on definition id?
      mycursor.execute("SELECT Definition_id FROM Word_Definition WHERE text=%s", (definition_id,))
      definition_id = mycursor.fetchone()
      if definition_id is not None:
        definition_id = definition_id[0]
        new_definition = input("Enter the new definition: ")
        mycursor.execute("UPDATE Word_Definition SET text=%s WHERE Definition_id=%s", (new_definition,definition_id))
        db.commit()
        print("Definition changed successfully!")
      else:
        print("Definition id does not exist")
    else:
      print("Word does not exist")
    return

def Delete_Definition():
    word_name = input("Enter the word: ")
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=%s", (word_name,))
    word_id = mycursor.fetchone()
    if word_id is not None:
      word_id = word_id[0]
      print("Definition ID, Definition")
      mycursor.execute("SELECT Definition_id, text FROM Word_Definition WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      definition_id = input("Enter the definition id to delete: ")
      # NOTE: Might want to change logic to list defintions of a word and choose based on definition id?
      mycursor.execute("SELECT Definition_id FROM Word_definition WHERE Definition_id=%s AND Word_ID=%s", (definition_id,word_id))
      definition_id = mycursor.fetchone()
      if definition_id is not None:
        definition_id = definition_id[0]
        mycursor.execute("DELETE FROM Word_Definition WHERE Definition_id=%s", (definition_id,))
        db.commit()
        print("Definition deleted successfully!")
      else:
        print("Definition does not exist")
    else:
      print("Word does not exist")
    return
"""______________________________TRANSLATION FUNCTIONS___________________________
TODO add_translation(word)
TODO delete_translation(word)
TODO edit_translation(word)

"""

def get_word_id(word):
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=%s", (word,))
    word_id = mycursor.fetchone()
    if word_id is not None:
      return word_id[0]
    else:
      return None
    
def add_translation(word):
    word_id = get_word_id(word)
    if word_id != None:
      translated_text = input("Enter the translation: ")
      mycursor.execute("INSERT INTO Translation (Word_ID, Translated_Text) VALUES (%s,%s)", (word_id,translated_text))
      db.commit()
      print("Translation added successfully!")
    else:
      print("Word does not exist")
    return

def delete_translation(word): 
    word_id = get_word_id(word)
    if word_id != None:
      print("Translation ID, Translated Text")
      mycursor.execute("SELECT Translation_ID, Translated_Text FROM Translation WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      translation_id = input("Enter the translation id to delete: ")
      mycursor.execute("SELECT Translation_ID FROM Translation WHERE Translation_ID=%s AND Word_ID=%s", (translation_id,word_id))
      translation_id = mycursor.fetchone()
      if translation_id is not None:
        translation_id = translation_id[0]
        mycursor.execute("DELETE FROM Translation WHERE Translation_ID=%s", (translation_id,))
        db.commit()
        print("Translation deleted successfully!")
      else:
        print("Translation ID does not exist")
    else:
      print("Word does not exist")
    return

def edit_translation(word):
    word_id = get_word_id(word)
    if word_id != None:
      print("Translation ID, Translated Text")
      mycursor.execute("SELECT Translation_ID, Translated_Text FROM Translation WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      translation_id = input("Enter the translation id to edit: ")
      mycursor.execute("SELECT Translation_ID FROM Translation WHERE Translation_ID=%s AND Word_ID=%s", (translation_id,word_id))
      translation_id = mycursor.fetchone()
      if translation_id is not None:
        translation_id = translation_id[0]
        new_translation = input("Enter the new translation: ")
        mycursor.execute("UPDATE Translation SET Translated_Text=%s WHERE Translation_ID=%s", (new_translation,translation_id,))
        db.commit()
        print("Translation edited successfully!")
      else:
        print("Translation ID does not exist")
    else:
      print("Word does not exist")
    return

"""_______________________________USER FUNCTIONS_________________________________
TODO View_Profile(User_ID): views users profile
TODO edit_user_settings(User_ID): edits users settings
TODO show_user_languages(User_ID): shows all languages user is learning
Choose_Language(User_ID): assigns a new language to user to learn
TODO remove_user_language(User_ID, language): removes a language from users list being learned

"""

def View_Profile(User_ID): # TODO
    print("Not implemented yet.")
    return

def edit_user_settings(User_ID): # TODO
    print("Not implemented yet.")
    return

def show_user_languages(User_ID): # TODO
    print("Not implemented yet.")
    return

def Choose_Language(User_ID: int):
    while True:  # Use 'while True' for clearer looping intent
        language = Sinput("Choose a language to learn (press 1 for a list),")
        if language == '1':
            show_languages()
            continue  # Immediately continue to the next iteration of the loop

        # Fetch the default language once at the start of the function to avoid repeated calls
        mycursor.execute("SELECT default_language FROM Users WHERE USER_ID = %s", (User_ID,))
        default_language = mycursor.fetchone()[0]

        if language == default_language:
            print("Error: This is your default language.")
            continue  # Prompt the user again since they chose their default language

        # Check if the language has already been selected
        mycursor.execute("SELECT * FROM User_Selected_Languages WHERE USER_ID = %s AND Selected_Languages = %s", (User_ID, language))
        if mycursor.fetchone():
            print("Error: You've already selected this language. Try again.")
            continue  # Prompt the user again since they chose a previously selected language

        # If the language is neither the default nor already selected, proceed to add it
        try:
            mycursor.execute("""
                INSERT INTO User_Selected_Languages (USER_ID, Selected_Languages)
                VALUES (%s, %s)
                """, (User_ID, language))
            db.commit()
            print("Language added successfully.")
            break  # Exit the loop after successfully adding the language
        except mysql.connector.IntegrityError as err:
            print("Error:", err)
            continue  # In case of an SQL error, prompt the user again

    return

def remove_user_language(User_ID, language): # TODO
    print("Not implemented yet.")
    return

"""________________________LEARN FUNCTIONS_____________________________
TODO review_learned_words(User_ID): lets user practice words already learned (should give user the word in their language and ask them for the translated word, have them try again till they get it right or press show answer)
TODO practice_new_vocabulary(User_ID): lets user practice new words (first shows translation then same as review_learned_words)
TODO track_learning_progress(User_ID): shows user percentage of a language complete (can be for word list or whole language)
make_wordList(User_ID): makes a new word list for user to learn words from
TODO add_word_to_list(User_ID, Word_list): adds words to existing word list
TODO remove_word_from_list(User_ID, Word_list): removes words from existing word list
TODO delete_wordList(User_ID): deletes an existing word list
TODO edit_wordList(User_ID): edits an existing word list

"""
def review_learned_words(User_ID): # TODO
    print("Not implemented yet.")
    return

def practice_new_vocabulary(User_ID): # TODO
    print("Not implemented yet.")
    return

def track_learning_progress(User_ID):  # TODO
    print("Not implemented yet.")
    return

def make_wordList(User_ID):
    list_title = Sinput("Enter title for new word list:")
    valid = 0
    new = 0
    while valid == 0:
        mycursor.execute("SELECT * FROM Word_List WHERE List_Name = %s AND User_ID = %s", (list_title))
        if mycursor.fetchone():
            print(f"Error, list title is already in use! Please use a different title.")
        else:
            valid += 1
    mycursor.execute("SELECT default_language FROM Users WHERE User_ID = %s", (User_ID,))
    default_language = mycursor.fetchone()
    default_language = default_language[0]
    while new == 0:
        language = Sinput("Choose a language to learn (press 1 for a list),")      
        if language == '1':
            show_languages()
        if language == default_language:
            print("Error this is your default Language")
        else:
            new += 1
            try:
                Word_Count = 0
                mycursor.execute("""
                INSERT INTO Word_List (List_Name, Word_Count User_ID, primary_language, translated_language)
                VALUES (%s, %s, %s, %s, %s)
                """, (list_title, Word_Count, User_ID, default_language, language))
                db.commit()
            except mysql.connector.IntegrityError as err:
                print("Error: {}".format(err))
                return err
    choice = input("List added successfully! [press ENTER]")
    if choice == 1:
       db.commit()

def add_word_to_list(User_ID, Word_list):  # TODO
    print("Not implemented yet.")
    return

def remove_word_from_list(User_ID, Word_list):  # TODO
    print("Not implemented yet.")
    return

def delete_wordList(User_ID):  # TODO
    print("Not implemented yet.")
    return

def edit_wordList(User_ID):  # TODO
    print("Not implemented yet.")
    return

"""________________________ADMIN FUNCTIONS_________________________________
Add_language(): adds a new language to sql database
TODO delete_Language(language): deletes an existing language will need to also delete all words in that language, and the words translations and definitions
TODO Edit_Language(language): edits an existing language
Show_Users(): shows a list of all users in database
Add_User(admin,...): adds a new user to the sql database
TODO Delete_User(): deletes an existing user from sql database, will also have to delete all the users word list
TODO Edit_User(): edits an existing user
TODO User_Search(): searches for user by id, name, or email

"""
def Add_language():
    language_name = Sinput("Input language name")
    word_count = 0
    mycursor.execute("SELECT * FROM Languages WHERE language_name = %s", (language_name))
    if mycursor.fetchone():
        print(f"Error, language name already exists. Please use a different name.")
    else: 
        try: 
            mycursor.execute("""
                INSERT INTO Languages (word_count, languague_name)
                VALUES (%s, %s)
                """, (word_count, language_name))
            db.commit()
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
            return err

def delete_Language(language):  # TODO
    print("Not implemented yet.")
    return

def Edit_Language(language):  # TODO
    print("Not implemented yet.")
    return

def Show_Users():
    mycursor.execute("SELECT * FROM Users")
    for x in mycursor:
        print(x)
       
def Add_User(admin: bool, phone_number: str = None, email: str = None, first_name: str = None, last_name: str = None, password: str = None, authorization: str = None, default_language: str = None, language_id: str = None): 
    if admin == True:
        new = 0
        while new == 0:
            email = Sinput("Enter their email")
            mycursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            if mycursor.fetchone():
                print(f"Error, email already exists. Please use a different email.")
            else:
                new += 1
                phone_number = Sinput("Enter their phone number")
                first_name = Sinput("Enter their first name")
                last_name = Sinput("Enter their last name")
                password = Sinput("Enter their password")
                level = 0
                while level == 0:
                    authorization = Sinput("Enter their authorization level")
                    if authorization != 'default' or authorization != 'admin' or authorization != 'CEO':
                        print("Error, not supported authorization level.")
                    else:
                        level +=1
                valid = 0
                while valid == 0:
                    default_language = Sinput("Enter your default language")
                    mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (default_language,))
                    language_id = mycursor.fetchone()
                    if language_id != None:
                        language_id = language_id[0]
                        valid += 1
                    else:
                        print("Error, Invalid language here are the current supported languages: ")
                        show_languages()
    try: 
        
        mycursor.execute("""
            INSERT INTO Users (phone_number, email, first_name, last_name, password, authorization, default_language, language_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (phone_number, email, first_name, last_name, password, authorization, default_language, language_id))
        User_ID = mycursor.lastrowid
        print("User registered successfully! User ID:", User_ID)
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
        return err

    choice = input("User registered successfully! [press ENTER]")
    if choice == 1:
       db.commit()
    return User_ID

def Delete_User():  # TODO
    print("Not implemented yet.")
    return

def Edit_User():  # TODO
    print("Not implemented yet.")
    return

def User_Search():  # TODO
    print("Not implemented yet.")
    return

"""_____________________________________________SQL FUNCTIONS__________________________________________
Create_Tables(): creates the database pretty much

"""
def Create_Tables():
    mycursor.execute("CREATE TABLE Users (User_ID int PRIMARY KEY NOT NULL AUTO_INCREMENT, phone_number VARCHAR(16), email VARCHAR(64) NOT NULL, first_name VARCHAR(64) NOT NULL, last_name VARCHAR(64) NOT NULL, password VARCHAR(50) NOT NULL, authorization ENUM('default', 'admin', 'CEO'), default_language VARCHAR(64), language_id int NOT NULL)")
    mycursor.execute("CREATE TABLE Languages (language_id INTEGER PRIMARY KEY AUTO_INCREMENT, word_count INTEGER CHECK (word_count >= 0),language_name VARCHAR(64) NOT NULL)")
    mycursor.execute("CREATE TABLE User_Selected_Languages (User_ID int, Selected_Languages VARCHAR(64) NOT NULL)")
    mycursor.execute("CREATE TABLE Word (Word_ID INTEGER PRIMARY KEY AUTO_INCREMENT, Text TEXT NOT NULL, language_id INTEGER)")
    mycursor.execute("CREATE TABLE Word_Definition (Definition_id INTEGER PRIMARY KEY AUTO_INCREMENT, text TEXT NOT NULL, Word_ID INTEGER)")
    mycursor.execute("CREATE TABLE Word_List (List_ID INTEGER PRIMARY KEY AUTO_INCREMENT, Word_Count INTEGER CHECK (Word_Count >= 0), User_ID INTEGER, primary_language int NOT NULL, translated_language int NOT NULL")
    mycursor.execute("CREATE TABLE Words_In_List(List_ID INTEGER, Word_ID INTEGER)")
    mycursor.execute("CREATE TABLE Translation(Translation_ID INTEGER PRIMARY KEY AUTO_INCREMENT, Word_ID INTEGER NOT NULL, Translated_Text VARCHAR(255) NOT NULL, FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID))")

    mycursor.execute("ALTER TABLE Users ADD CONSTRAINT FK_User_Language FOREIGN KEY (language_id) REFERENCES Languages(language_id)")
    mycursor.execute("ALTER TABLE Word ADD CONSTRAINT FK_Word_Language FOREIGN KEY (language_id) REFERENCES Languages(language_id)")
    mycursor.execute("ALTER TABLE Word_Definition ADD CONSTRAINT FK_WordDef_Word FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID)")
    mycursor.execute("ALTER TABLE Word_List ADD CONSTRAINT FK_WordList_User FOREIGN KEY (User_ID) REFERENCES Users(User_ID)")
    mycursor.execute("ALTER TABLE Word_List ADD CONSTRAINT FK_WordList_Default FOREIGN KEY (primary_language) REFERENCES Users(language_id)")
    mycursor.execute("ALTER TABLE Words_In_List ADD CONSTRAINT FK_Words_ListID FOREIGN KEY (List_ID) REFERENCES Word_List(List_ID)")
    mycursor.execute("ALTER TABLE Words_In_List ADD CONSTRAINT FK_Words_WordID FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID)")

    print("Tables created")
