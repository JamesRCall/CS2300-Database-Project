import mysql.connector
from enum import Enum
import random

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password = "mysql",
    database = "language_database"
)

mycursor = db.cursor()

def Sinput(text: str):
    x = input(f'{text} (press 0 to quit): ')
    if x == '0':
        quit()
    return x

def menu(User_ID = None): 
    if not hasattr(menu, "counter"):
        menu.counter = 0 
    menu.counter += 1
    if menu.counter == 1:
        User_ID = start()
        menu.User_ID = User_ID
    else:
        User_ID = menu.User_ID
    mycursor.execute("SELECT authorization FROM Users WHERE User_ID = %s", (User_ID,))
    user = mycursor.fetchone()
    authorization, = user
    super_user = False
    print("""1 Language Options
2 Word & Definition Options
3 Translation Options
4 User Hub
5 Learn Hub
6 Log Out""")
    if authorization == 'admin' or authorization == 'CEO':
        print("""7 Admin Panel""")
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
    elif choice == '6':
        menu.counter = 0
        menu()
    elif choice == '7' and super_user == True:
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
            Language_Search()
        elif choice == '3':
            menu()
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
            Delete_word()
        elif choice == '3':
            Edit_word()
        elif choice == '4':
            Word_Search()
        elif choice == '5':
            Add_definition()
        elif choice == '6':
            Delete_Definition()
        elif choice == '7':
            Modify_Definition()
        elif choice == '8':
            menu()
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
            menu()
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
            View_Profile(User_ID)
        elif choice == '2':
            edit_user_settings(User_ID)
        elif choice == '3':
            show_user_languages(User_ID)
        elif choice == '4':
            Choose_Language(User_ID)
        elif choice == '5':
            language = Sinput("Enter the language to remove from your learning list:")
            remove_user_language(User_ID, language)
        elif choice == '6':
            menu()
        else:
            print("Invalid input. Please try again.")

def Learn_Hub(User_ID):
    while True:
        choice = Sinput("""
Learn Hub:
1. Review Learned Words
2. Practice New Vocabulary
3. Track Learning Progress
4. Make a Word List
5. Add words to Word List
6. Remove words from Word List
7. Delete a Word List
8. Edit a Word List
9. Go Back
Choose an option""")
        if choice == '1':
            review_learned_words(User_ID)
        elif choice == '2':
            practice_new_vocabulary(User_ID)
        elif choice == '3':
            track_learning_progress(User_ID)
        elif choice == '4':
            make_wordList(User_ID)
        elif choice == '5':
            add_word_to_list(User_ID)
        elif choice == '6':
            remove_word_from_list(User_ID)
        elif choice == '7':
            delete_wordList(User_ID)
        elif choice == '8':
            edit_wordList(User_ID)
        elif choice == '9':
            menu()
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
            delete_language(language)
        elif choice == '3':
            language = Sinput("Enter the language to edit:")
            Edit_Language(language)
        elif choice == '4':
            Show_Users()
        elif choice == '5':
            Add_User(True)
        elif choice == '6':
            Delete_User()
        elif choice == '7':
            Edit_User()
        elif choice == '8':
            User_Search()
        elif choice == '9':
            menu()

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
        choice = input("Please choose login(1) or sign-up(2) or quit(0): ")
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
Language_Search(): searches for languages based on id or text

"""
def show_languages():
    print("language ID, Word Count, Language Name")
    mycursor.execute("SELECT * FROM Languages")
    for x in mycursor:
        print(x)

def Language_Search():
    print("Choose the search type:")
    print("1. Search by Language ID")
    print("2. Search by  Text")
    choice = Sinput("Enter your choice (1 or 2)")

    if choice == '1':
        # Search by language ID
        lang_id = Sinput("Enter the Language ID")
        try:
            lang_id = int(lang_id)  # Ensuring the input is an integer
            mycursor.execute("SELECT * FROM Languages WHERE language_id = %s", (lang_id,))
            result = mycursor.fetchone()
            if result:
                print("Language Found: ID:", result[0], "Name:", result[2])
            else:
                print("No Language found with ID:", lang_id)
        except ValueError:
            print("Invalid input! Please enter a valid integer for lang ID.")
        except mysql.connector.Error as err:
            print("Error: ", err)
    elif choice == '2':
        # Search by Language name
        lang_text = Sinput("Enter part of the language name to search")
        mycursor.execute("SELECT * FROM Languages WHERE language_name LIKE %s", ('%' + lang_text + '%',))
        results = mycursor.fetchall()
        if results:
            print("Language(s) found:")
            for language in results:
                print("ID:", language[0], "Language:", language[2])
        else:
            print("No Language found containing:", lang_text)
    else:
        print("Invalid choice. Please select either 1 or 2.")

"""_____________________________WORD & DEFINITION FUNCTIONS___________________________________
Add_word(): adds a new word
Delete_word(): deletes an existing word
Edit_word(): edits an existing word
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

def Delete_word():
    while True:
        text = Sinput("Enter the word you want to delete")
        mycursor.execute("SELECT Word_ID FROM Word WHERE Text = %s", (text,))
        word = mycursor.fetchone()
        if word:
            word_id = word[0]
            try:
                # Delete from Translation where the word is used
                mycursor.execute("DELETE FROM Translation WHERE Word_ID = %s", (word_id,))
                
                # Delete from Words_In_List where the word is used
                mycursor.execute("DELETE FROM Words_In_List WHERE Word_ID = %s", (word_id,))
                
                # Delete from Word_Definition where the word is defined
                mycursor.execute("DELETE FROM Word_Definition WHERE Word_ID = %s", (word_id,))
                
                # Delete from User_Learned_Words where the word is learned
                mycursor.execute("DELETE FROM User_Learned_Words WHERE Word_ID = %s", (word_id,))
                
                # Finally, delete the word itself
                mycursor.execute("DELETE FROM Word WHERE Word_ID = %s", (word_id,))
                
                db.commit()
                print("Word deleted successfully!")
                break
            except mysql.connector.Error as err:
                print("Error deleting word:", err)
                db.rollback()
        else:
            print("Word not found. Please enter a valid word.")

def Edit_word():
    while True:
        old_text = Sinput("Enter the word you want to edit")
        mycursor.execute("SELECT Word_ID FROM Word WHERE Text = %s", (old_text,))
        word = mycursor.fetchone()
        if word:
            word_id = word[0]  # Assuming the correct column index for Word_ID
            new_text = Sinput("Enter the new text for the word")
            try:
                # Ensure the column name in SQL is correct as per your schema; it should likely be `Word_ID`, not `WordID`
                mycursor.execute("UPDATE Word SET Text = %s WHERE Word_ID = %s", (new_text, word_id))
                db.commit()
                print("Word edited successfully!")
                return  # Use return instead of break to exit the function after successful operation
            except mysql.connector.Error as err:
                print("Error editing word:", err)
                db.rollback()  # Roll back the transaction on error
        else:
            print("Word not found. Please enter a valid word.")

def Word_Search():
    print("Choose the search type:")
    print("1. Search by Word ID")
    print("2. Search by Word Text")
    choice = Sinput("Enter your choice (1 or 2),")

    if choice == '1':
        # Search by Word ID
        word_id = Sinput("Enter the Word ID")
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
        word_text = Sinput("Enter part of the word text to search")
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
    while word_id is None:
        word = Sinput("Enter the word you'd like to add a definition to")
        mycursor.execute("SELECT Word_ID FROM Word WHERE Text = (%s)", (word,))
        word_id_result = mycursor.fetchone()
        if word_id_result is None:
            print("Error, that word does not exist.")
            continue
        word_id = word_id_result[0]  # Correct extraction of word_id

    definition_added = False
    while not definition_added:
        definition = Sinput("Enter your word's definition")
        if definition.lower() == 'quit':
            return  # Exit the function

        mycursor.execute("SELECT * FROM Word_Definition WHERE text = %s AND Word_ID = %s", (definition, word_id))
        if mycursor.fetchone():
            print("Error, definition already exists. Try again.")
        else:
            definition_added = True

    try:
        mycursor.execute("""
            INSERT INTO Word_Definition (text, Word_ID)
            VALUES (%s, %s)
            """, (definition, word_id))
        db.commit()
        print("Definition added successfully!")
    except mysql.connector.IntegrityError as err:
        print(f"Error: {err}")
        return err


def Modify_Definition():
    # CHANGE: User enters a word. The word's definition and definition id's are printed. User chooses the definition id
    #         to modify
    word_name = Sinput("Enter the word that you want to modify its definition")
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=%s", (word_name,))
    word_id = mycursor.fetchone()
    if word_id is not None:
      word_id = word_id[0]
      print("Definition ID, Definition")
      mycursor.execute("SELECT Definition_id, text FROM Word_Definition WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      definition_id = Sinput("Enter the definition id to modify")
      mycursor.execute("SELECT Definition_id FROM Word_Definition WHERE Definition_id=%s", (definition_id,))
      definition_id = mycursor.fetchone()
      if definition_id is not None:
        definition_id = definition_id[0]
        new_definition = Sinput("Enter the new definition")
        mycursor.execute("UPDATE Word_Definition SET text=%s WHERE Text=%s", (new_definition,definition_id))
        db.commit()
        print("Definition changed successfully!")
      else:
        print("Definition id does not exist")
    else:
      print("Word does not exist")
    return

def Delete_Definition():
    word_name = Sinput("Enter the word")
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=%s", (word_name,))
    word_id = mycursor.fetchone()
    if word_id is not None:
      word_id = word_id[0]
      print("Definition ID, Definition")
      mycursor.execute("SELECT Definition_id, text FROM Word_Definition WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      definition_id = Sinput("Enter the definition id to delete")
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
get_word_id(word): finds a words id given the text
get_language_id(language_name): find language id given its name
add_translation(word): adds a translation to a word given the words text
delete_translation(word): deletes a word's translation given a words text
edit_translation(word): edits a word's translation

"""
def get_word_id(word):
    mycursor.execute("SELECT Word_ID, language_id FROM Word WHERE Text = %s", (word,))
    result = mycursor.fetchone()
    if result is not None:
        word_id, language_id = result
        return word_id, language_id
    else:
        return None, None

def get_language_id(language_name):
    mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (language_name,))
    result = mycursor.fetchone()
    if result is not None:
        return result[0]
    else:
        print("Language not found. Please enter a valid language name.")
        return None

def add_translation(word):
    word_id, word_language_id = get_word_id(word)
    if word_id is not None:
        translated_text = Sinput("Enter the translation")
        language_name = Sinput("Enter the translation's language name")
        language_id = get_language_id(language_name)
        if language_id is not None:
            mycursor.execute("INSERT INTO Translation (Word_ID, Word_Language, Language_ID, Translated_Text) VALUES (%s, %s, %s, %s)", (word_id, word_language_id, language_id, translated_text))
            db.commit()
            print("Translation added successfully!")
        else:
            print("Failed to add translation. Invalid language name.")
    else:
        print("Word does not exist.")

def delete_translation(word): 
    word_id, _ = get_word_id(word)
    if word_id != None:
      print("Translation ID, Translated Text")
      mycursor.execute("SELECT Translation_ID, Translated_Text FROM Translation WHERE Word_ID=%s", (word_id,))
      for x in mycursor:
        print(x)
      translation_id = Sinput("Enter the translation id to delete")
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
    word_id, _ = get_word_id(word)  # We do not need the language_id for this function
    if word_id is not None:
        print("Translation ID, Translated Text")
        mycursor.execute("SELECT Translation_ID, Translated_Text FROM Translation WHERE Word_ID=%s", (word_id,))
        translations = mycursor.fetchall()

        if translations:
            for x in translations:
                print(x)
            translation_id = Sinput("Enter the translation id to edit")
            mycursor.execute("SELECT Translation_ID FROM Translation WHERE Translation_ID=%s AND Word_ID=%s", (translation_id, word_id))
            translation_check = mycursor.fetchone()
            if translation_check is not None:
                new_translation = Sinput("Enter the new translation")
                mycursor.execute("UPDATE Translation SET Translated_Text=%s WHERE Translation_ID=%s", (new_translation, translation_id))
                db.commit()
                print("Translation edited successfully!")
            else:
                print("Translation ID does not exist.")
        else:
            print("No translations found for this word.")
    else:
        print("Word does not exist.")

"""_______________________________USER FUNCTIONS_________________________________
View_Profile(User_ID): views users profile
edit_user_settings(User_ID): edits users settings
show_user_languages(User_ID): shows all languages user is learning
Choose_Language(User_ID): assigns a new language to user to learn
remove_user_language(User_ID, language): removes a language from users list being learned

"""

def View_Profile(User_ID):
    # Fetch user details
    mycursor.execute("SELECT first_name, last_name, default_language FROM Users WHERE User_ID = %s", (User_ID,))
    user_details = mycursor.fetchone()
    if not user_details:
        print("User not found.")
        return

    first_name, last_name, default_language = user_details

    # Calculate total XP based on correct answers
    mycursor.execute("SELECT SUM(Correct_Amount) FROM User_Learned_Words WHERE User_ID = %s", (User_ID,))
    total_xp = mycursor.fetchone()[0] or 0

    # Define levels based on XP thresholds
    levels = [5, 10, 20, 50, 100, 200, 400, 800, 1600, 3200]
    user_level = 0
    for i, threshold in enumerate(levels):
        if total_xp >= threshold:
            user_level = i + 1
        else:
            break

    # Determine the top learning language based on the highest number of learned words
    mycursor.execute("""
        SELECT Languages.language_name FROM Languages
        JOIN Word ON Languages.language_id = Word.language_id
        JOIN User_Learned_Words ON Word.Word_ID = User_Learned_Words.Word_ID
        WHERE User_Learned_Words.User_ID = %s
        GROUP BY Languages.language_id
        ORDER BY COUNT(User_Learned_Words.Word_ID) DESC
        LIMIT 1
    """, (User_ID,))
    top_language = mycursor.fetchone()
    top_language_name = top_language[0] if top_language else "No language data"

    # Display the profile details
    print("Profile Details")
    print(f"Name: {first_name} {last_name}")
    print(f"Default Language: {default_language}")
    print(f"Top Learning Language: {top_language_name}")
    print(f"Total XP: {total_xp}")
    print(f"Level: {user_level}")

def edit_user_settings(user_id):
    # Fetch and display current settings
    mycursor.execute("SELECT email, phone_number, default_language FROM Users WHERE User_ID = %s", (user_id,))
    user_data = mycursor.fetchone()
    if not user_data:
        print("User not found.")
        return

    email, phone_number, default_language = user_data
    print(f"Current settings:\nEmail: {email}\nPhone Number: {phone_number}\nDefault Language: {default_language}")

    # Provide options for what to edit
    print("Choose the setting you want to edit:\n1. Email\n2. Phone Number\n3. Default Language")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        new_email = input("Enter your new email: ")
        mycursor.execute("UPDATE Users SET email = %s WHERE User_ID = %s", (new_email, user_id))
    elif choice == '2':
        new_phone = input("Enter your new phone number: ")
        mycursor.execute("UPDATE Users SET phone_number = %s WHERE User_ID = %s", (new_phone, user_id))
    elif choice == '3':
        print("Available languages:")
        mycursor.execute("SELECT language_name FROM Languages")
        languages = mycursor.fetchall()
        for idx, (language,) in enumerate(languages, start=1):
            print(f"{idx}. {language}")
        lang_choice = int(input("Select your new default language: ")) - 1
        new_language_id = languages[lang_choice][0]
        mycursor.execute("UPDATE Users SET default_language = %s WHERE User_ID = %s", (new_language_id, user_id))
    else:
        print("Invalid choice")
        return

    db.commit()
    print("Settings updated successfully.")

def show_user_languages(User_ID):
    # Fetch the default language using the language_id foreign key in Users table
    mycursor.execute("SELECT language_name FROM Languages JOIN Users ON Languages.language_id = Users.language_id WHERE Users.User_ID = %s", (User_ID,))
    default_language = mycursor.fetchone()
    if default_language:
        print(f"Default Language for User ID {User_ID}: {default_language[0]}")
    else:
        print("Default language not found for this user.")
    
    # Fetch selected languages from User_Selected_Languages table
    mycursor.execute("SELECT Selected_Languages FROM User_Selected_Languages WHERE User_ID = %s", (User_ID,))
    selected_languages = mycursor.fetchall()
    if selected_languages:
        print(f"Selected Languages for User ID {User_ID}:")
        for language in selected_languages:
            print(language[0])
    else:
        print("No additional selected languages found for this user.")

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

def remove_user_language(User_ID, language):
    try:
        # First, check if the language is actually selected by the user
        mycursor.execute("SELECT * FROM User_Selected_Languages WHERE User_ID = %s AND Selected_Languages = %s", (User_ID, language))
        if not mycursor.fetchone():
            print(f"The language '{language}' is not selected by User ID {User_ID}.")
            return

        # Remove the language from the User_Selected_Languages table
        mycursor.execute("DELETE FROM User_Selected_Languages WHERE User_ID = %s AND Selected_Languages = %s", (User_ID, language))
        db.commit()
        print(f"The language '{language}' has been successfully removed from User ID {User_ID}'s selected languages.")

    except mysql.connector.Error as err:
        print(f"Error removing the language: {err}")
        db.rollback()

"""________________________LEARN FUNCTIONS_____________________________
generate_language_questions(user_id, list_id): creates a question dictionary of sorted questions for review
format_written_question(question): formats all written questions for review
format_multiple_choice_question(question): formats all multiple choice questions for review
review_learned_words(User_ID): lets user practice words already learned 
practice_new_vocabulary(User_ID): lets user practice new words (first shows translation then same as review_learned_words)
track_learning_progress(User_ID): shows user percentage of a language complete (can be for word list or whole language)
make_wordList(User_ID): makes a new word list for user to learn words from
add_word_to_list(User_ID, Word_list): adds words to existing word list
remove_word_from_list(User_ID, Word_list): removes words from existing word list
delete_wordList(User_ID): deletes an existing word list
edit_wordList(User_ID): edits an existing word list

"""
def generate_language_questions(user_id, list_id):
    # This query fetches translations that are specific to the word list's target language
    mycursor.execute("""
        SELECT t.Word_ID, t.Translated_Text, t.Language_ID, t.Word_Language, w.Text AS Original_Text
        FROM Translation t
        JOIN Words_In_List wil ON t.Word_ID = wil.Word_ID
        JOIN Word_List wl ON wil.List_ID = wl.List_ID
        JOIN Word w ON w.Word_ID = t.Word_ID
        WHERE wl.List_ID = %s AND t.Language_ID = wl.translated_language
        ORDER BY RAND() LIMIT 10
    """, (list_id,))
    translations = mycursor.fetchall()

    # Fetching language settings including names for better clarity in question prompts
    mycursor.execute("""
        SELECT wl.primary_language, wl.translated_language, pl.language_name AS primary_language_name, tl.language_name AS translated_language_name
        FROM Word_List wl
        JOIN Languages pl ON wl.primary_language = pl.language_id
        JOIN Languages tl ON wl.translated_language = tl.language_id
        WHERE wl.List_ID = %s AND wl.User_ID = %s
    """, (list_id, user_id))
    language_settings = mycursor.fetchone()
    known_language = language_settings[0]
    learning_language = language_settings[1]
    known_language_name = language_settings[2]
    translated_language_name = language_settings[3]

    questions = []
    for translation in translations:
        question_type = 'multiple choice' if random.choice([True, False]) else 'written'
        question_language_choice = random.choice([True, False])  # Randomly choose the question language

        # Constructing each question's details
        questions.append({
            'word_id': translation[0],
            'original_text': translation[4],  # The text in its original language
            'translated_text': translation[1],  # The translated text
            'language_id': translation[2],
            'word_language_id': translation[3],
            'type': question_type,
            'question_language': known_language if question_language_choice else learning_language,
            'answer_language': learning_language if question_language_choice else known_language,
            'known_language': known_language,
            'translated_language': learning_language,
            'known_language_name': known_language_name,
            'translated_language_name': translated_language_name
        })

    return questions

def format_written_question(question):
    # Determine the text for the question based on the current question language
    mycursor.execute("SELECT Text FROM Word WHERE Word_ID = %s", (question['word_id'],))
    original_text = mycursor.fetchone()[0]

    if question['question_language'] == question['known_language']:
        prompt = f"What is the translation for '{original_text}' in {question['translated_language_name']}?"
        correct_answer = question['translated_text']  # This should be fetched correctly aligned with the 'translated_language'
    else:
        prompt = f"What is the translation for '{question['translated_text']}' in {question['known_language_name']}?"
        correct_answer = original_text

    return {
        'type': 'written',
        'prompt': prompt,
        'correct_answer': correct_answer
    }

def format_multiple_choice_question(question):
    original_text = question['original_text']

    # Determine target language ID for fetching incorrect translations
    target_language_id = question['translated_language'] if question['question_language'] == question['known_language'] else question['known_language']

    if question['question_language'] == question['known_language']:
        # Fetch incorrect answers that are also translated texts from known to learning language
        mycursor.execute("""
            SELECT DISTINCT Translated_Text FROM Translation
            WHERE Word_ID != %s AND Language_ID = %s AND Translated_Text != %s
            ORDER BY RAND() LIMIT 10
        """, (question['word_id'], question['translated_language'], question['translated_text']))
    else:
        # Fetch incorrect answers that are original texts in the known language
        mycursor.execute("""
            SELECT DISTINCT Text FROM Word
            WHERE Word_ID != %s AND language_id = %s AND Text != %s
            ORDER BY RAND() LIMIT 10
        """, (question['word_id'], question['known_language'], original_text))

    all_possible_incorrects = [row[0] for row in mycursor.fetchall()]

    # Ensure there are enough unique incorrect answers
    incorrect_answers = list(set(all_possible_incorrects))[:3]
    if len(incorrect_answers) < 3:
        incorrect_answers += ["Incorrect 1", "Incorrect 2", "Incorrect 3"][:3 - len(incorrect_answers)]

    correct_answer = question['translated_text'] if question['question_language'] == question['known_language'] else original_text
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    # Create a prompt based on the question's language direction
    prompt = f"What is the correct translation for '{original_text}' in the {question['translated_language_name']}?" if question['question_language'] == question['known_language'] else f"What is the correct translation for '{question['translated_text']}' in the {question['known_language_name']}?"

    return {
        'type': 'multiple choice',
        'prompt': prompt,
        'options': options,
        'correct_answer': correct_answer
    }

def review_learned_words(user_id):
    # Step 1: Fetch user's word lists and let them choose one
    mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
    word_lists = mycursor.fetchall()
    if not word_lists:
        print("No word lists found for this user.")
        return

    # Display word lists to the user
    print("Please select a word list to review:")
    for i, (list_id, list_name) in enumerate(word_lists, start=1):
        print(f"{i}. {list_name}")
    choice = int(Sinput("Enter your choice"))
    selected_list_id = word_lists[choice - 1][0]

    # Step 2: Generate questions for the selected list
    questions = generate_language_questions(user_id, selected_list_id)

    # Step 3: Present questions to the user and check answers
    for question in questions:
        if question['type'] == 'written':
            formatted_question = format_written_question(question)
        else:
            formatted_question = format_multiple_choice_question(question)

        print(formatted_question['prompt'])
        if 'options' in formatted_question:
            for idx, option in enumerate(formatted_question['options'], start=1):
                print(f"{idx}. {option}")
            user_answer = int(Sinput("Choose the correct answer (number)")) - 1
            user_answer = formatted_question['options'][user_answer]
        else:
            user_answer = Sinput("Your answer")

        if user_answer.lower() == formatted_question['correct_answer'].lower():
            print("Correct!")
            correct_answer_increment = 1
        else:
            print("Incorrect. The correct answer was:", formatted_question['correct_answer'])
            correct_answer_increment = 0

        # Step 4: Update the Correct_Amount in the database
        mycursor.execute("""
            INSERT INTO User_Learned_Words (User_ID, Word_ID, Correct_Amount)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE Correct_Amount = Correct_Amount + %s
        """, (user_id, question['word_id'], correct_answer_increment, correct_answer_increment))

    print(f"Review session completed.")

def practice_new_vocabulary(user_id):
    # Step 1: Fetch user's word lists and let them choose one
    mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
    word_lists = mycursor.fetchall()
    if not word_lists:
        print("No word lists found for this user.")
        return

    print("Please select a word list to practice new vocabulary:")
    for index, (list_id, list_name) in enumerate(word_lists, start=1):
        print(f"{index}. {list_name}")

    list_choice = int(Sinput("Enter your choice"))
    selected_list_id = word_lists[list_choice - 1][0]

    # Get the language settings for the chosen word list
    mycursor.execute("SELECT primary_language, translated_language FROM Word_List WHERE List_ID = %s", (selected_list_id,))
    language_settings = mycursor.fetchone()
    primary_language, translated_language = language_settings

    # Step 2: Find words not in the list but with valid translations in the learning language
    mycursor.execute("""
        SELECT w.Word_ID, w.Text, t.Translated_Text
        FROM Word w
        JOIN Translation t ON w.Word_ID = t.Word_ID
        WHERE t.Language_ID = %s AND w.language_id = %s AND w.Word_ID NOT IN (SELECT Word_ID FROM Words_In_List WHERE List_ID = %s)
    """, (translated_language, primary_language, selected_list_id))

    new_words = mycursor.fetchall()
    if not new_words:
        print("No new words to practice.")
        return

    print("New vocabulary to learn:")
    for word_id, original_text, translated_text in new_words:
        print(f"Word: {original_text} - Translation: {translated_text}")

    # Step 3: Practice these new words similarly to review_learned_words
    for word_id, original_text, translated_text in new_words:
        print(f"\nPractice Translation for '{original_text}'")
        user_answer = Sinput(f"What is the translation of '{original_text}' in the learning language?")

        if user_answer.lower() == translated_text.lower():
            print("Correct!")
        else:
            print(f"Incorrect. The correct translation is: {translated_text}")

        # Optionally, add the practiced words to the word list and/or user learned words
        # Confirm if the user wants to add this word to their list
        add_word = Sinput("Would you like to add this word to your list? (yes/no)")
        if add_word.lower() == 'yes':
            mycursor.execute("INSERT INTO Words_In_List (List_ID, Word_ID) VALUES (%s, %s)", (selected_list_id, word_id))
            db.commit()
            print("Word added to your list!")

    print("Vocabulary practice session completed.")

def track_learning_progress(user_id):
    print("Choose the tracking mode:")
    print("1. Track by specific word list")
    print("2. Track by language")
    
    choice = int(Sinput("Enter your choice (1 or 2)"))

    if choice == 1:
        # Fetch and let user select a word list
        mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
        word_lists = mycursor.fetchall()
        if not word_lists:
            print("No word lists found for this user.")
            return

        print("Select a word list:")
        for index, (list_id, list_name) in enumerate(word_lists, start=1):
            print(f"{index}. {list_name}")

        list_choice = int(Sinput("Enter your choice"))
        selected_list_id = word_lists[list_choice - 1][0]

        # Calculate learning progress for the selected word list
        mycursor.execute("""
            SELECT COUNT(*) FROM Words_In_List WHERE List_ID = %s
        """, (selected_list_id,))
        total_words = mycursor.fetchone()[0]

        mycursor.execute("""
            SELECT COUNT(DISTINCT Word_ID) FROM User_Learned_Words
            WHERE User_ID = %s AND Word_ID IN (SELECT Word_ID FROM Words_In_List WHERE List_ID = %s)
        """, (user_id, selected_list_id))
        learned_words = mycursor.fetchone()[0]

    elif choice == 2:
        # Fetch and let user select a language
        mycursor.execute("SELECT language_id, language_name FROM Languages")
        languages = mycursor.fetchall()
        for lang in languages:
            print(f"{lang[0]}. {lang[1]}")

        lang_choice = int(Sinput("Enter the language ID to track"))

        # Calculate learning progress for the selected language
        mycursor.execute("""
            SELECT COUNT(*) FROM Word WHERE language_id = %s
        """, (lang_choice,))
        total_words = mycursor.fetchone()[0]

        mycursor.execute("""
            SELECT COUNT(DISTINCT Word_ID) FROM User_Learned_Words
            WHERE User_ID = %s AND Word_ID IN (SELECT Word_ID FROM Word WHERE language_id = %s)
        """, (user_id, lang_choice))
        learned_words = mycursor.fetchone()[0]

    else:
        print("Invalid choice.")
        return

    if total_words > 0:
        progress = (learned_words / total_words) * 100
        print(f"Learning progress: {progress:.2f}%")
    else:
        print("No words found for the selected criteria.")

def make_wordList(User_ID):
    list_title = input("Enter title for new word list: ")

    # Check if the word list title already exists for the user
    while True:
        mycursor.execute("SELECT * FROM Word_List WHERE List_Name = %s AND User_ID = %s", (list_title, User_ID))
        if mycursor.fetchone():
            print("Error, list title is already in use! Please use a different title.")
            list_title = input("Enter title for new word list: ")
        else:
            break

    # Fetch user's default language ID
    mycursor.execute("SELECT language_id FROM Users WHERE User_ID = %s", (User_ID,))
    default_language_id = mycursor.fetchone()[0]

    # Function to display available languages and get the language ID
    def get_language_id(prompt):
        print(prompt)
        mycursor.execute("SELECT language_id, language_name FROM Languages")
        languages = mycursor.fetchall()
        for id, name in languages:
            print(f"{id}. {name}")
        lang_choice = int(input("Enter the language id: "))
        return lang_choice

    # Choose the language to learn
    while True:
        language_id = get_language_id("Choose a language to learn (Enter the language ID):")

        # Check if the selected language is the user's default language
        if language_id == default_language_id:
            print("Error: this is your default language.")
        else:
            Word_Count = 0  # Initial word count set to zero
            try:
                mycursor.execute("""
                INSERT INTO Word_List (List_Name, User_ID, primary_language, translated_language, Word_Count)
                VALUES (%s, %s, %s, %s, %s)
                """, (list_title, User_ID, default_language_id, language_id, Word_Count))
                db.commit()
                print("List added successfully!")
                break
            except mysql.connector.IntegrityError as err:
                print("Error creating word list:", err)

def add_word_to_list(user_id):
    # Step 1: Fetch user's word lists and let them choose one
    mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
    word_lists = mycursor.fetchall()
    if not word_lists:
        print("No word lists found for this user.")
        return

    print("Please select a word list to add words to:")
    for index, (list_id, list_name) in enumerate(word_lists, start=1):
        print(f"{index}. {list_name} (ID: {list_id})")

    list_choice = int(Sinput("Enter your choice (number)"))
    word_list_id = word_lists[list_choice - 1][0]  # Get the List_ID from the selected choice

    # Get the translated language of the selected word list
    mycursor.execute("SELECT translated_language FROM Word_List WHERE List_ID = %s", (word_list_id,))
    translated_language_id = mycursor.fetchone()[0]

    # Step 2: Prompt for the word to add by name
    while True:
        word_name = Sinput("Enter the name of the word you want to add")
        mycursor.execute("SELECT Word_ID, language_id FROM Word WHERE Text = %s", (word_name,))
        word_result = mycursor.fetchone()

        if not word_result:
            print("Word not found. Please enter a valid word name.")
            continue

        word_id, word_language_id = word_result

        # Step 3: Check if the word has a valid translation for the word list's language
        mycursor.execute("SELECT * FROM Translation WHERE Word_ID = %s AND Language_ID = %s", (word_id, translated_language_id))
        if not mycursor.fetchone():
            print(f"This word does not have a valid translation in the target language of the word list (Language ID: {translated_language_id}).")
            continue

        # Step 4: Check if the word already exists in the list
        mycursor.execute("SELECT * FROM Words_In_List WHERE List_ID = %s AND Word_ID = %s", (word_list_id, word_id))
        if mycursor.fetchone():
            print("This word is already in the list.")
            continue

        # Step 5: Add the word to the list
        try:
            mycursor.execute("INSERT INTO Words_In_List (List_ID, Word_ID) VALUES (%s, %s)", (word_list_id, word_id))
            db.commit()
            print("Word added to the word list successfully!")
            break
        except mysql.connector.Error as err:
            print("Error adding word to word list:", err)
            db.rollback()

def remove_word_from_list(user_id):
    # Step 1: Fetch user's word lists and let them choose one
    mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
    word_lists = mycursor.fetchall()
    if not word_lists:
        print("No word lists found for this user.")
        return

    print("Please select a word list to remove words from:")
    for index, (list_id, list_name) in enumerate(word_lists, start=1):
        print(f"{index}. {list_name} (ID: {list_id})")

    list_choice = int(Sinput("Enter your choice (number)"))
    word_list_id = word_lists[list_choice - 1][0]  # Get the List_ID from the selected choice

    # Step 2: Display all words in the selected list
    mycursor.execute("SELECT wl.Word_ID, w.Text FROM Words_In_List wl JOIN Word w ON wl.Word_ID = w.Word_ID WHERE wl.List_ID = %s", (word_list_id,))
    words_in_list = mycursor.fetchall()
    if not words_in_list:
        print("No words found in the selected word list.")
        return

    print("Please select a word to remove:")
    for index, (word_id, word_text) in enumerate(words_in_list, start=1):
        print(f"{index}. {word_text} (ID: {word_id})")

    word_choice = int(Sinput("Enter your choice (number)"))
    word_id_to_remove = words_in_list[word_choice - 1][0]  # Get the Word_ID from the selected choice

    # Step 3: Remove the word from the list
    try:
        mycursor.execute("DELETE FROM Words_In_List WHERE List_ID = %s AND Word_ID = %s", (word_list_id, word_id_to_remove))
        db.commit()
        print("Word removed from the list successfully!")
    except mysql.connector.Error as err:
        print("Error removing word from list:", err)
        db.rollback()


def delete_wordList(user_id):
    # Step 1: Fetch user's word lists and let them choose one to delete
    mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
    word_lists = mycursor.fetchall()
    if not word_lists:
        print("No word lists found for this user.")
        return

    print("Please select a word list to delete:")
    for index, (list_id, list_name) in enumerate(word_lists, start=1):
        print(f"{index}. {list_name} (ID: {list_id})")

    list_choice = int(Sinput("Enter your choice (number)"))
    word_list_id = word_lists[list_choice - 1][0]  # Get the List_ID from the selected choice

    # Confirm deletion
    confirmation = input(f"Are you sure you want to delete the word list '{word_lists[list_choice - 1][1]}'? This cannot be undone. Type 'yes' to confirm: ")
    if confirmation.lower() == 'yes':
        # Step 2: Begin transaction to delete the word list and all related entries
        try:
            # Delete all associated words from Words_In_List
            mycursor.execute("DELETE FROM Words_In_List WHERE List_ID = %s", (word_list_id,))
            
            # Delete the word list itself
            mycursor.execute("DELETE FROM Word_List WHERE List_ID = %s", (word_list_id,))
            
            db.commit()
            print("Word list deleted successfully!")
        except mysql.connector.Error as err:
            print("Error deleting word list:", err)
            db.rollback()
    else:
        print("Deletion cancelled.")

def edit_wordList(user_id):
    # Step 1: Fetch user's word lists and let them choose one to edit
    mycursor.execute("SELECT List_ID, List_Name FROM Word_List WHERE User_ID = %s", (user_id,))
    word_lists = mycursor.fetchall()
    if not word_lists:
        print("No word lists found for this user.")
        return

    print("Please select a word list to edit:")
    for index, (list_id, list_name) in enumerate(word_lists, start=1):
        print(f"{index}. {list_name} (ID: {list_id})")

    list_choice = int(Sinput("Enter your choice (number)"))
    word_list_id = word_lists[list_choice - 1][0]  # Get the List_ID from the selected choice

    # Step 2: Ask the user what they want to edit
    print("What would you like to edit?")
    print("1. List Name")
    print("2. Translated Language")
    edit_choice = int(Sinput("Enter your choice (number)"))

    if edit_choice == 1:
        # Edit the list name
        new_name = Sinput("Enter the new name for the word list")
        mycursor.execute("UPDATE Word_List SET List_Name = %s WHERE List_ID = %s", (new_name, word_list_id))
        db.commit()
        print("Word list name updated successfully!")
    elif edit_choice == 2:
        # Edit the translated language
        print("Available languages:")
        mycursor.execute("SELECT language_id, language_name FROM Languages")
        languages = mycursor.fetchall()
        for lang in languages:
            print(f"{lang[0]}: {lang[1]}")

        new_lang_id = int(Sinput("Enter the new language ID for translation"))
        # Confirm before changing language and deleting words
        confirmation = input("Changing the language will remove all words from this list. Are you sure you want to continue? (yes/no): ")
        if confirmation.lower() == 'yes':
            mycursor.execute("UPDATE Word_List SET translated_language = %s WHERE List_ID = %s", (new_lang_id, word_list_id))
            # Remove all words from the list
            mycursor.execute("DELETE FROM Words_In_List WHERE List_ID = %s", (word_list_id,))
            db.commit()
            print("Translated language updated and all words removed successfully!")
        else:
            print("Operation cancelled.")
    else:
        print("Invalid choice.")

"""________________________ADMIN FUNCTIONS_________________________________
Add_language(): adds a new language to sql database
delete_Language(language): deletes an existing language will need to also delete all words in that language, and the words translations and definitions
Edit_Language(language): edits an existing language
Show_Users(): shows a list of all users in database
Add_User(admin,...): adds a new user to the sql database
Delete_User(): deletes an existing user from sql database, will also have to delete all the users word list
Edit_User(): given a valid user id, allows user to edit any value of a user (other than User_ID)
User_Search(): searches for user by id, name, or email

"""
def Add_language():
    language_name = Sinput("Input language name")
    word_count = 0
    
    # Check if the language already exists
    mycursor.execute("SELECT * FROM Languages WHERE language_name = %s", (language_name,))
    if mycursor.fetchone():
        print("Error, language name already exists. Please use a different name.")
    else:
        try:
            mycursor.execute("""
                INSERT INTO Languages (word_count, language_name)
                VALUES (%s, %s)
                """, (word_count, language_name))
            db.commit()
            print(f"Language '{language_name}' added successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)
            return err

def delete_language(language):
    try:
        # Check if the language exists and get its ID
        mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (language,))
        result = mycursor.fetchone()
        if not result:
            print(f"No such language: {language}")
            return

        language_id = result[0]  # Extracting the integer ID from the tuple

        # Get all words in this language
        mycursor.execute("SELECT Word_ID FROM Word WHERE language_id = %s", (language_id,))
        words = mycursor.fetchall()

        # Delete related entries from dependent tables
        for (word_id,) in words:  # Extracting Word_ID from the tuple
            mycursor.execute("DELETE FROM Translation WHERE Word_ID = %s", (word_id,))
            mycursor.execute("DELETE FROM Word_Definition WHERE Word_ID = %s", (word_id,))
            mycursor.execute("DELETE FROM Words_In_List WHERE Word_ID = %s", (word_id,))
            mycursor.execute("DELETE FROM Word WHERE Word_ID = %s", (word_id,))

        # Finally, delete the language
        mycursor.execute("DELETE FROM Languages WHERE language_id = %s", (language_id,))
        
        # Commit the transaction
        db.commit()
        print(f"Language '{language}' and all associated data have been deleted.")

    except Exception as e:
        # Rollback in case of any error
        db.rollback()
        print(f"Failed to delete language {language}: {e}")

def Edit_Language(language):
    try:
        # Check if the language exists
        mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (language,))
        result = mycursor.fetchone()
        if not result:
            print(f"No such language: {language}")
            return

        # Input new language name
        new_language_name = Sinput("Enter the new name for the language:")

        # Update the language name
        mycursor.execute("UPDATE Languages SET language_name = %s WHERE language_id = %s", (new_language_name, result[0]))
        db.commit()
        print(f"Language name updated from {language} to {new_language_name}")

    except Exception as e:
        db.rollback()
        print(f"Failed to update language {language}: {e}")


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
                while True:
                    authorization = str(Sinput("Enter their authorization level"))
                    if authorization != 'default' and authorization != 'admin' and authorization != 'CEO':
                        print("Error, not supported authorization level.")
                    else:
                        break
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

def Delete_User():
    user_id = Sinput("Enter the User ID of the user you want to edit")
    
    # Fetch and display current user details for reference
    mycursor.execute("SELECT * FROM Users WHERE User_ID = %s", (user_id,))
    user_details = mycursor.fetchone()
    if not user_details:
        print("User not found.")
        return

    try:
        # Delete entries from Words_In_List using Word_List linked to the User
        mycursor.execute("DELETE Words_In_List FROM Words_In_List JOIN Word_List ON Words_In_List.List_ID = Word_List.List_ID WHERE Word_List.User_ID = %s", (user_id,))

        # Delete Word_List entries
        mycursor.execute("DELETE FROM Word_List WHERE User_ID = %s", (user_id,))

        # Finally, delete the user
        mycursor.execute("DELETE FROM Users WHERE User_ID = %s", (user_id,))
        
        # Commit the transaction
        db.commit()
        print(f"User and all associated data have been deleted successfully.")

    except Exception as e:
        # Rollback in case of error
        db.rollback()
        print(f"Failed to delete user: {e}")


def Edit_User():
    user_id = Sinput("Enter the User ID of the user you want to edit")
    
    # Fetch and display current user details for reference
    mycursor.execute("SELECT * FROM Users WHERE User_ID = %s", (user_id,))
    user_details = mycursor.fetchone()
    if not user_details:
        print("User not found.")
        return

    print(f"Current details of User ID {user_id}: {user_details}")
    
    print("Select the attribute you want to edit:")
    print("1: Phone Number")
    print("2: Email")
    print("3: First Name")
    print("4: Last Name")
    print("5: Password")
    print("6: Authorization")
    print("7: Default Language")
    print("8: Language ID")
    
    choice = int(Sinput("Enter your choice (1-8)"))
    if choice not in range(1, 9):
        print("Invalid choice. Please enter a number between 1 and 8.")
        return

    new_value = Sinput("Enter the new value for the selected attribute")

    # Define SQL based on the choice
    attributes = {
        1: "phone_number",
        2: "email",
        3: "first_name",
        4: "last_name",
        5: "password",
        6: "authorization",
        7: "default_language",
        8: "language_id"
    }
    attribute = attributes[choice]

    # Update user details in the Users table
    sql_update = f"UPDATE Users SET {attribute} = %s WHERE User_ID = %s"
    mycursor.execute(sql_update, (new_value, user_id))
    
    # If the user changes the language_id, update the foreign key reference
    if attribute == "language_id":
        # Update any other tables that reference language_id as a foreign key
        mycursor.execute("UPDATE Word_List SET primary_language = %s WHERE User_ID = %s", (new_value, user_id))

    db.commit()
    print(f"User ID {user_id} updated: {attribute} set to {new_value}.")

def User_Search():
    print("""Select the search criterion:)
    1: Search by User ID
    2: Search by Name
    3: Search by Email""")
    
    try:
        choice = int(Sinput("Enter your choice (1, 2, or 3)"))
        if choice not in [1, 2, 3]:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return

        search_term = Sinput("Enter the search term")

        if choice == 1:
            # Search by User ID
            mycursor.execute("SELECT User_ID, first_name, last_name, email FROM Users WHERE User_ID = %s", (search_term,))
        elif choice == 2:
            # Search by Name
            mycursor.execute("""
                SELECT User_ID, first_name, last_name, email FROM Users
                WHERE first_name LIKE %s OR last_name LIKE %s
            """, ('%' + search_term + '%', '%' + search_term + '%'))
        elif choice == 3:
            # Search by Email
            mycursor.execute("SELECT User_ID, first_name, last_name, email FROM Users WHERE email LIKE %s", ('%' + search_term + '%',))

        results = mycursor.fetchall()
        if results:
            for user in results:
                print(f"ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}")
        else:
            print("No users found matching the search criteria.")

    except ValueError:
        print("Please enter a valid number for your choice.")
    except mysql.connector.Error as err:
        print(f"Error searching for users: {err}")


"""_____________________________________________SQL FUNCTIONS__________________________________________
Create_Tables(): creates the database pretty much

"""
def Create_Tables():
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            User_ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
            phone_number VARCHAR(16),
            email VARCHAR(64) NOT NULL,
            first_name VARCHAR(64) NOT NULL,
            last_name VARCHAR(64) NOT NULL,
            password VARCHAR(50) NOT NULL,
            authorization ENUM('default', 'admin', 'CEO'),
            default_language VARCHAR(64),
            language_id int NOT NULL,
            FOREIGN KEY (language_id) REFERENCES Languages(language_id)
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Languages (
            language_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            word_count INTEGER DEFAULT 0,
            language_name VARCHAR(64) NOT NULL
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS User_Selected_Languages (
            User_ID int,
            Selected_Languages VARCHAR(64) NOT NULL,
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Word (
            Word_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
            Text TEXT NOT NULL,
            language_id INTEGER,
            FOREIGN KEY (language_id) REFERENCES Languages(language_id)
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Word_Definition (
            Definition_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            text TEXT NOT NULL,
            Word_ID INTEGER,
            FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID)
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Word_List (
            List_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
            List_Name VARCHAR(64) NOT NULL,
            User_ID INTEGER NOT NULL,
            word_count INTEGER DEFAULT 0,
            Difficulty VARCHAR(64) DEFAULT 'Medium',
            primary_language int NOT NULL,
            translated_language int NOT NULL,
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
            FOREIGN KEY (primary_language) REFERENCES Languages(language_id),
            FOREIGN KEY (translated_language) REFERENCES Languages(language_id)
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Words_In_List (
            List_ID INTEGER,
            Word_ID INTEGER,
            FOREIGN KEY (List_ID) REFERENCES Word_List(List_ID),
            FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID),
            PRIMARY KEY (List_ID, Word_ID)
        );
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Translation (
            Translation_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
            Word_ID INTEGER NOT NULL,
            Translated_Text VARCHAR(255) NOT NULL,
            FOREIGN KEY (Word_ID) REFERENCES Word(Word_ID)
        );
    """)
    print("Tables created")

