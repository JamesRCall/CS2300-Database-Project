import mysql.connector
from enum import Enum

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password = "mysql",
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
        2. Add New Language
        3. Learn a New Language
        4. Delete a Language
        5. Edit a Language
        6. Search for a Language                
        7. Go Back
        Choose an option""")
        if choice == '1':
            show_languages()
        elif choice == '2':
            Add_language()
        elif choice == '3':
            Choose_Language(User_ID)
        elif choice == '4':
            language = Sinput("Enter the language to delete:")
            # TODO: delete_language(language)
        elif choice == '5':
            language = Sinput("Enter the language to edit:")
            # TODO: edit_language(language)
        elif choice == '6':
            print("")
            # TODO: Language_Search()
        elif choice == '7':
            break
        else:
            print("Invalid input. Please try again.")


def Word_Hub(User_ID):
    while True:
        choice = Sinput("""
        Word & Definition Options:
        1. Add New Word
        2. Add Definition to a Word
        3. Delete a Word
        4. Delete a Definition
        5. Edit a Word
        6. Edit a Definition
        7. Search for a Word
        8. Go Back
        Choose an option""")
        if choice == '1':
            Add_word()
        elif choice == '2':
            word_id = Sinput("Enter the ID of the word to add a definition:")
            Add_definition(int(word_id))
        elif choice == '3':
            word = Sinput("Enter the word to delete:")
            # TODO: delete_word(word)
        elif choice == '4':
            word = Sinput("Enter the word to delete its definition:")
            # TODO: delete_word_definition(word)
        elif choice == '5':
            word = Sinput("Enter the word to edit:")
            # TODO: edit_word(word)
        elif choice == '6':
            word = Sinput("Enter the word to edit its definition:")
            # TODO: edit_word_definition(word) 
        elif choice == '7':
            print('')
            # TODO: Word_Search()
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
            # TODO: add_translation(word)
        elif choice == '2':
            word = Sinput("Enter the word to delete its translation:")
            # TODO: delete_translation(word)
        elif choice == '3':
            word = Sinput("Enter the word to edit its translation:")
            # TODO: edit_translation(word) 
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
        4. Remove a Language I'm Learning
        5. Search for a User
        6. Go Back
        Choose an option""")
        if choice == '1':
            print("Function to display user profile needs to be implemented")
        elif choice == '2':
            print("")
            # TODO: edit_user_settings(User_ID)
        elif choice == '3':
            print("")
            # TODO: show_user_languages(User_ID)
        elif choice == '4':
            language = Sinput("Enter the language to remove from your learning list:")
            # TODO: remove_user_language(User_ID, language)
        elif choice == '5':
            print('')
            # TODO: User_Search()
        elif choice == '6':
            break
        else:
            print("Invalid input. Please try again.")

def Learn_Hub(User_ID):
    while True:
        choice = Sinput("""
        Learn Hub:
        1. Review Learned Words # TODO
        2. Practice Vocabulary # TODO
        3. Track Learning Progress # TODO
        4. Go Back
        Choose an option""")
        if choice == '1':
            print("")
            # TODO: review_learned_words(User_ID)
        elif choice == '2':
            print("")
            # TODO: practice_vocabulary(User_ID)
        elif choice == '3':
            print("")
            # TODO: track_learning_progress(User_ID)
        elif choice == '4':
            break
        else:
            print("Invalid input. Please try again.")

def Admin_Panel(User_ID):
    while True:
        choice = Sinput("""
        Admin Panel:
        1. Manage Users # TODO
        2. Manage Languages # TODO
        3. View System Reports # TODO
        4. Go Back
        Choose an option""")
        if choice == '1':
            print("")
            # TODO: manage_users()
        elif choice == '2':
            print("")
            # TODO: manage_languages()
        elif choice == '3':
            print("")
            # TODO: view_system_reports() 
        elif choice == '4':
            break
        else:
            print("Invalid input. Please try again.")



#Login function
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

            User_ID = Add_User(phone_number, email, first_name, last_name, password, authorization, default_language, language_id)
    choice = input("Would you like to add a new language to learn? (1 yes 0 no): ")
    if choice == '1':
        Choose_Language(User_ID)
    return User_ID

def Add_User(phone_number: str, email: str, first_name: str, last_name: str, password: str, authorization: str, default_language: str, language_id: str): 
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

def Show_Users():
    print("age, name, height, weight, no. of teeth, swarm_id")
    mycursor.execute("SELECT * FROM Users")
    for x in mycursor:
        print(x)

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

def show_languages():
    print("language ID, Word Count, Language Name")
    mycursor.execute("SELECT * FROM Languages")
    for x in mycursor:
        print(x)

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

def Modify_Definition():
    word_definition = input("Enter the definition completely: ")
    # NOTE: Might want to change logic to list defintions of a word and choose based on definition id?
    mycursor.execute("SELECT Definition_id FROM Word_definition WHERE text=%s", (word_definition,))
    definition_id = mycursor.fetchone()
    if definition_id is not None:
      definition_id = definition_id[0]
      new_definition = input("Enter the new definition: ")
      mycursor.execute("UPDATE Word_Definition SET text=%s WHERE Definition_id=%s", (new_definition,definition_id))
      db.commit()
      print("Definition changed successfully")
    else:
      print("Entered definition does not exist")
    return

def Delete_Definition():
    word_name = input("Enter the word: ")
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=%s", (word_name,))
    word_id = mycursor.fetchone()
    if word_id is not None:
      word_id = word_id[0]
      word_definition = input("Enter the definition completely: ")
      # NOTE: Might want to change logic to list defintions of a word and choose based on definition id?
      mycursor.execute("SELECT Definition_id FROM Word_definition WHERE text=%s AND Word_ID=%s", (word_definition,word_id))
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
