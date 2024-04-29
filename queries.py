import mysql.connector
import random
from enum import Enum

db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password = "root",
    database = "test5"
)

mycursor = db.cursor()

#Login function
def start():
    choice = input("Please choose login(1) or sign-up(2) or quit(0):")
    if choice == '0':
        quit()
    elif choice == '1':
        login()
    elif choice == '2':
        signup()
    else:
        print("Error, invalid input. Try again.")
        start()

def login():
    found = 0
    attempts = 0
    while found == 0:
        id = input("Please enter your User ID (enter 0 to quit): ")
        if id == '0':
            quit()
        mycursor.execute("SELECT * FROM Users WHERE USER_ID = (%s)", (id,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("Error, That User ID does not exist.")
    
    correct = 0
    while correct == 0 and attempts < 3:
        pswd = input("Please enter your password (enter 0 to quit): ")
        if pswd == '0':
            quit()
        mycursor.execute("SELECT * FROM Users WHERE USER_ID = (%s) AND password = (%s)", (id, pswd))
        for x in mycursor:
            correct += 1
        if correct == 0:
            attempts += 1
            print(f"Error, password incorrect. {3 - attempts} Attempts left.")
    if attempts >= 3:
        print("Account locked due to too many failed attempts.")
        quit()
    

def signup():
    new = 0
    while new == 0:
        email = input("Enter your email (enter 0 to quit): ")
        if email == '0':
            quit()
        mycursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        if mycursor.fetchone():
            print(f"Error, email already exists. Please use a different email.")
        else:
            new += 1
            phone_number = input("Enter your phone number: ")
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            password = input("Enter your password: ")
            authorization = 'default'
            default_language = input("Enter your default language: ")
            language_id = 1  # Example: Defaulting to English with language_id = 1

            mycursor.execute("""
                INSERT INTO Users (phone_number, email, first_name, last_name, password, authorization, default_language, language_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (phone_number, email, first_name, last_name, password, authorization, default_language, language_id))
            db.commit()
            print("User registered successfully!")
            return

def Show_Chompskis():
    print("age, name, height, weight, no. of teeth, swarm_id")
    mycursor.execute("SELECT * FROM Gnome_Chompskis")
    for x in mycursor:
        print(x)
   
def Add_Chompski(age : int, name : str, height : float, weight : float, no_teeth : int, swarm_id : int):
    try: 
        mycursor.execute("INSERT Gnome_Chompskis(age, name, height, weight, no_teeth, swarm_id)VALUES(%s,%s,%s,%s,%s,%s)", (age, name, height, weight, no_teeth, swarm_id))
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
        return err
    
    mycursor.execute("SELECT * FROM Gnome_Chompskis")
    for x in mycursor:
        print(x)
    choice = input("Database Updated [press ENTER]")
    if choice == 1:
       db.commit()

def Create_Tables():
    mycursor.execute("CREATE TABLE Employee (employee_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,fname VARCHAR(50) NOT NULL, mname VARCHAR(50),lname VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, authorization ENUM('Intern','Employee', 'Supervisor', 'Bossman'))")
    mycursor.execute("CREATE TABLE Swarm (swarm_id int PRIMARY KEY AUTO_INCREMENT, name varchar(45) NOT NULL, latitude double(9, 5), longitude double (9,5))")
    mycursor.execute("CREATE TABLE Oversees (employee_id int, swarm_id int, FOREIGN KEY(employee_id) REFERENCES Employee(employee_id),  FOREIGN KEY(swarm_id) REFERENCES Swarm(swarm_id))")
    mycursor.execute("CREATE TABLE Gnome_Chompskis (chompskis_id int PRIMARY KEY AUTO_INCREMENT,name varchar(45) NOT NULL,  age smallint, height double(10,2), weight double (10,2), no_teeth int UNSIGNED, swarm_id int, FOREIGN KEY(swarm_id) REFERENCES Swarm(swarm_id))")
    print("Tables created")

def Add_Definition():
    word_name = input("Enter the word: ")
    mycursor.execute("SELECT Word_ID FROM Word WHERE Text=word_name")
    word_id = mycursor.fetchone()
    word_id = word_id[0]
    definition = input("Enter the definition: ")
    mycursor.execute("INSERT INTO Word_Definition (definition, word_id)")
    db.commit()
    print("Definition entered successfully!")
    return