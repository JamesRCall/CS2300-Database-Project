import mysql.connector
from enum import Enum
import random

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
    print("""
    1 Language Options
    2 Word & Definition Options
    3 Translation Options
    4 User Hub
    5 Learn Hub
    6 Log Out""")
    if authorization == 'admin' or authorization == 'CEO':
        print("""    7 Admin Panel""")
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
            word = Sinput("Enter the word to delete:")
            Delete_word(word)
        elif choice == '3':
            word = Sinput("Enter the word to edit:")
            Edit_word(word)
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
            print("")
            # TODO: add_word_to_list(User_ID, Word_List)
        elif choice == '6':
            print("")
            # TODO: remove_word_from_list(User_ID, Word_List)
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
            delete_Language(language)
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
    print("Choose the search type:")
    print("1. Search by Language ID")
    print("2. Search by  Text")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # Search by language ID
        lang_id = input("Enter the Word ID: ")
        try:
            lang_id = int(lang_id)  # Ensuring the input is an integer
            mycursor.execute("SELECT * FROM Languages WHERE language_id = %s", (lang_id,))
            result = mycursor.fetchone()
            if result:
                print("Language Found: ID:", result[0], "Name:", result[2])
            else:
                print("No word found with ID:", lang_id)
        except ValueError:
            print("Invalid input! Please enter a valid integer for lang ID.")
        except mysql.connector.Error as err:
            print("Error: ", err)
    elif choice == '2':
        # Search by Language name
        lang_text = input("Enter part of the language name to search: ")
        mycursor.execute("SELECT * FROM Languages WHERE language_name LIKE %s", ('%' + lang_text + '%',))
        results = mycursor.fetchall()
        if results:
            print("Words found:")
            for language in results:
                print("ID:", language[0], "Language:", language[2])
        else:
            print("No words found containing:", lang_text)
    else:
        print("Invalid choice. Please select either 1 or 2.")

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
add_translation(word): adds a translation to a word given the words text
delete_translation(word): deletes a word's translation given a words text
edit_translation(word): edits a word's translation

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
show_user_languages(User_ID): shows all languages user is learning
Choose_Language(User_ID): assigns a new language to user to learn
remove_user_language(User_ID, language): removes a language from users list being learned

"""

def View_Profile(User_ID): # TODO
    print("Not implemented yet.")
    return

def edit_user_settings(User_ID): # TODO
    print("Not implemented yet.")
    return

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
TODO review_learned_words(User_ID): lets user practice words already learned (should give user the word in their language and ask them for the translated word, have them try again till they get it right or press show answer)
TODO practice_new_vocabulary(User_ID): lets user practice new words (first shows translation then same as review_learned_words)
TODO track_learning_progress(User_ID): shows user percentage of a language complete (can be for word list or whole language)
make_wordList(User_ID): makes a new word list for user to learn words from
TODO add_word_to_list(User_ID, Word_list): adds words to existing word list
TODO remove_word_from_list(User_ID, Word_list): removes words from existing word list
TODO delete_wordList(User_ID): deletes an existing word list
TODO edit_wordList(User_ID): edits an existing word list

"""
def generate_language_questions(user_id, list_id):
    # Step 1: Fetch 10 random translations related to the user's selected word list
    mycursor.execute("""
        SELECT t.Word_ID, t.Translated_Text, t.Language_ID, t.Word_Language
        FROM Translation t
        JOIN Words_In_List wil ON t.Word_ID = wil.Word_ID
        WHERE wil.List_ID = %s
        ORDER BY RAND() LIMIT 10
    """, (list_id,))
    translations = mycursor.fetchall()

    # Step 2: Fetch the user's known and learning languages
    mycursor.execute("""
        SELECT primary_language, translated_language
        FROM Word_List
        WHERE List_ID = %s AND User_ID = %s
    """, (list_id, user_id))
    language_settings = mycursor.fetchone()
    known_language = language_settings[0]
    learning_language = language_settings[1]

    # Step 3: Decide the question type and language for each translation
    questions = []
    for translation in translations:
        question_type = 'multiple choice' if random.choice([True, False]) else 'written'
        question_language_choice = random.choice([True, False])  # True for known language, False for learning language

        # Generate the question and answer setup
        questions.append({
            'word_id': translation[0],
            'text': translation[1],
            'language_id': translation[2],
            'word_language_id': translation[3],
            'type': question_type,
            'question_language': known_language if question_language_choice else learning_language,
            'answer_language': learning_language if question_language_choice else known_language
        })

    return questions

def format_written_question(question):
    mycursor.execute("SELECT Text FROM Word WHERE Word_ID = %s", (question['word_id'],))
    original_text = mycursor.fetchone()[0]

    if question['question_language'] == 'known':
        prompt = f"What is the translation for '{original_text}' in the learning language?"
    else:
        prompt = f"What is the translation for '{question['text']}' in your known language?"

    return {
        'type': 'written',
        'prompt': prompt,
        'correct_answer': question['text']
    }

def format_multiple_choice_question(question):
    # Fetch the original text of the word for the question
    mycursor.execute("SELECT Text FROM Word WHERE Word_ID = %s", (question['word_id'],))
    original_text = mycursor.fetchone()[0]

    # Determine which language ID to exclude in the incorrect options based on question setup
    exclude_language_id = question['word_language_id'] if question['question_language'] == 'known' else question['language_id']

    # Fetch three additional incorrect translations
    mycursor.execute("""
        SELECT Translated_Text FROM Translation
        WHERE Word_ID != %s AND Language_ID = %s AND Word_Language != %s
        ORDER BY RAND() LIMIT 3
    """, (question['word_id'], question['language_id'], exclude_language_id))
    incorrect_answers = [row[0] for row in mycursor.fetchall()]

    # Mix the correct answer with incorrect ones
    correct_answer = question['text'] if question['question_language'] == 'known' else original_text
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)  # Shuffle to mix the correct answer among the incorrect ones

    # Setting up the prompt based on the question language
    prompt = f"What is the correct translation for '{original_text}' in the learning language?" if question['question_language'] == 'known' else f"What is the correct translation for '{question['text']}' in your known language?"

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
    choice = int(input("Enter your choice: "))
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
            user_answer = int(input("Choose the correct answer (number): ")) - 1
            user_answer = formatted_question['options'][user_answer]
        else:
            user_answer = input("Your answer: ")

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

def delete_Language(language):
    # Start the transaction
    db.start_transaction()
    
    try:
        # Check if the language exists and get its ID
        mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (language,))
        language_id = mycursor.fetchone()
        if not language_id:
            print(f"No such language: {language}")
            return

        # Get all words in this language
        mycursor.execute("SELECT Word_ID FROM Word WHERE language_id = %s", (language_id,))
        words = mycursor.fetchall()
        
        # Delete related entries from dependent tables
        for word_id in words:
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


def Edit_Language(old_language_name, new_language_name):
    try:
        # Check if the old language exists
        mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (old_language_name,))
        if not mycursor.fetchone():
            print(f"Language '{old_language_name}' does not exist.")
            return

        # Check if new language name already exists to avoid duplicates
        mycursor.execute("SELECT language_id FROM Languages WHERE language_name = %s", (new_language_name,))
        if mycursor.fetchone():
            print(f"Language name '{new_language_name}' already exists. Please choose another name.")
            return

        # Update the language name
        mycursor.execute("UPDATE Languages SET language_name = %s WHERE language_name = %s", (new_language_name, old_language_name))
        db.commit()
        print(f"Language name updated from '{old_language_name}' to '{new_language_name}'.")

    except mysql.connector.Error as err:
        print("Error: {}".format(err))


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

def Delete_User(user_id):
    # Start transaction
    db.start_transaction()

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
    user_id = input("Enter the User ID of the user you want to edit: ")
    
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
    
    choice = int(input("Enter your choice (1-8): "))
    if choice not in range(1, 9):
        print("Invalid choice. Please enter a number between 1 and 8.")
        return

    new_value = input("Enter the new value for the selected attribute: ")

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
        choice = int(input("Enter your choice (1, 2, or 3): "))
        if choice not in [1, 2, 3]:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return

        search_term = input("Enter the search term: ")

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

