# This is just a snippet of the real code base. It will not run as is.
import Queries as sq
import time
import os


def Add_Tuples():
    clear()
    sq.Show_Database()
    table = int(input("Which table # would you like to add to? [0 to exit]: "))
    
    while table < 0 or table > 4:
        print("Please choose from the available table #")
        sq.Show_Database()
        table = int(input("Which table # would you like to see?: "))
    match table:
        case 0:
            return
        case 1:
            fname = input("Please enter a first name: ")
            mname = input("Please enter a middle name: ")
            lname = input("Please enter a last name: ")
            password = input("Plase enter a password: ")
            if password != 0:
                authorization_no = 5
                count = 0
                for i in authorization_lists:
                    count +=1
                    print( "{}. ".format(count) + i)
                while authorization_no not in range(0,4):
                    authorization_no = int(input("Please enter authorization number:"))
                
                sq.Add_Employees(fname, mname, lname, password, authorization_no)

def Show_Tables():
    clear()
    sq.Show_Database()
    table = int(input("Which table # would you like to see? (enter 0 to quit): "))

    while table < 0 or table > 4:
        print("Please choose from the available table #")
        sq.Show_Database()
        table = int(input("Which table # would you like to see? (enter 0 to quit): "))
    match table:
        case 0:
            clear(  )
            return
        case 1:
            sq.Show_Employees()
            okay = input("press ENTER")
            Show_Tables()
        case 2:
            sq.Show_Chompskis()
            okay = input("press ENTER")
            Show_Tables()
        case 3:
            sq.Show_Oversees()
            okay = input("press ENTER")
            Show_Tables()
        case 4:
            sq.Show_Swarms()
            okay = input("press ENTER")
            Show_Tables()
        case 0:
            return 0
    # Add if else statements for choices
    
        
def main():
    menu()

if __name__ == "__main__":
    main()
