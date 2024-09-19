import random
import sqlite3
import getpass
import datetime
import os


# using now() to get current time
current_time = datetime.datetime.now()
date = f"{current_time.day}/{current_time.month}/{current_time.year}"
time = f"{current_time.hour}:{current_time.minute}:{current_time.second}"
date_and_time = f"{date} {time}"


# getting user computer name
current_user = getpass.getuser()
print(f"\nHello, your computer's username is: {current_user}\n\n")
print("Have you read the ReadMe.md file ?.\n\n")
print("\nKindly ensure you have installed sqlite3 on your computer before running this programme\n\n")
input("I hope you saved the projects folder in your 'Desktop' folder on your computer, if not, kindly ensure you have done that for this app to work effectively.\n\nPress Enter to proceed\n\n")

# database file path
# dataBaseFilePath = f"C:/Users/{current_user}/Desktop/wave_bank/waveBankAccountDataBase.db"


# Database initialization and connection
def get_dynamic_db_filepath():
    path = os.path.dirname(os.path.realpath(__file__))
    toDB = os.path.join(path, "waveBankAccountDataBase.db")
    return toDB


"""
Write a python program named BankAccount.py that a bank might use to represent customers bank accounts.  
Include a data member of type int to represent the account balance.

Provide a fuction that receives an initial balance and uses it to initialize the data member. 
The fuction should validate the initial balance to ensure that it's greater than or equal to 0. 
If not, set the balance to 0 and display an error message indicating that the initial balance was invalid. 

Provide three member functions. Member functions creditAmount should add an amount to the current balance. 
Member function debit amount should withdraw money from the account and ensure that the debit amount does 
not exceed the Account's balance. 
If it does, the balance should be left unchanged and the function should print a message 
indicating "Debit amount exceed account balance." 

Member function getBalance should return the current balance. 

Create a program that test the member functions of the class Account.

Necessary tables like Transaction history, User details... should be stored be persistent in the db With your SQLite

Sign up and login should functionality
should be available
And must have a user login and logout log 
(time and date stamp of every login 
Example:12/05/05  12:08:09  username logged in.)
And the logout (when the program ends(done with all transactions)
time and date stamp of every logout
Example:12/05/05  12:08:09  username logged out.)
stored in the database named users_log and on a txt either the same name

Show the output
"""        


def creditAmount1(amount, curBal):
    if amount < 0:
        print("\nYou can't input a negative value\n")
        return "You can't input a negative value"
    elif amount < 10 or amount > 100000:
        print("\nAmount must be between 10 and 100,000 naira\n")
        return "Amount must be between 10 and 100,000 naira"
    else:
        curBal += amount
        return curBal
        
        
def debitAmount1(amount, curBal):
    if amount < 0:
        print("\nYou can't input a negative value\n")
        return "You can't input a negative value"
    elif curBal < amount:
        print("\n\nDebit amount exceed account balance\n\n")
        return "Debit amount exceed account balance"
    else:
        curBal -= amount
        return curBal


def getBalance1(curBal):
    return curBal



# def logOut():
#     print("register user log out")
    
    
    
def deposit(userBio2):
    print(f"\n{userBio2[3]} Deposit into Account....\n\n")
    
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cursor = conn.cursor()

    # SELECT * FROM user_register WHERE account_no = ? AND password = ?
    # locate user transaction data in user_transaction table with account number
    cursor.execute("SELECT * FROM user_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
    userTransactResult = cursor.fetchone()  # returns the user's transaction data bio from the table as a tuple
    # print(userTransactResult)
    usersCurrentBalanceInDataBase = userTransactResult[5]
    
    
    # History
    cursor.execute("SELECT * FROM user_history_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
    userPreviousHistory = cursor.fetchone()  # returns the user's previous History transaction data bio from the table as a tuple
    # print(userPreviousHistory)
    
    

    debitAmount = int(input("Deposit Amount: "))

    # Define the new value
    newBalance = creditAmount1(debitAmount, usersCurrentBalanceInDataBase)
    # print(newBalance)
    
    # new_value = 1003.0
    transaction_type = "deposit"
    
    
    # Checking for Error first before executing
    if newBalance == "You can't input a negative value" or newBalance == "Amount must be between 10 and 100,000 naira":
        return newBalance
    else:
        if newBalance != None:     # None is return as a value if amount to withdraw is more than the current balance, and If stored in db, it will mess with the interactive operation
            cursor.execute("UPDATE user_transaction SET amount = ? WHERE account_no = ?", (newBalance, userBio2[2]))
            
            
        userCurrentTransactionRecord = f"{userBio2[3]}, you {transaction_type} {debitAmount} on {date_and_time}. Your balance is now {newBalance}\n\n"
        # Updated History
        userUpdatedHistory =  f"{userPreviousHistory[3]} {userCurrentTransactionRecord}"
        
        
        # Update the value for the specific ID
        cursor.execute("UPDATE user_transaction SET transaction_type = ? WHERE account_no = ?", (transaction_type, userBio2[2]))
        cursor.execute("UPDATE user_transaction SET timestamp = ? WHERE account_no = ?", (date_and_time, userBio2[2]))
        
        
        #update history
        cursor.execute("UPDATE user_history_transaction SET history = ? WHERE account_no = ?", (userUpdatedHistory, userBio2[2]))


        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()
        print(f"\n\nYou have deposit {newBalance} into your account successfully !!!\n\n")
        # print(userTransactResult)

    
    
def withdraw(userBio2):
    print(f"{userBio2[3]} withdraw from Account....\n\n")
    
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cursor = conn.cursor()

    # locate user transaction data in user_transaction table with account number
    cursor.execute("SELECT * FROM user_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
    userTransactResult = cursor.fetchone()  # returns the user's transaction data bio from the table as a tuple
    # print(userTransactResult)
    usersCurrentBalanceInDataBase = userTransactResult[5]
    
    # History
    cursor.execute("SELECT * FROM user_history_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
    userPreviousHistory = cursor.fetchone()  # returns the user's previous History transaction data bio from the table as a tuple
    # print(userPreviousHistory)
    
    debitAmount = int(input("Withdraw Amount: "))

    # Define the new value
    newBalance = debitAmount1(debitAmount, usersCurrentBalanceInDataBase)
    # print(newBalance)
    
    # new_value = 1003.0
    transaction_type = "withdraw"
    
    
    # Checking for Error first before executing
    if newBalance == "You can't input a negative value" or newBalance == "Debit amount exceed account balance":
        return newBalance
    else:
        # Update the value for the specific ID
        if newBalance != None:     # None is return as a value if amount to withdraw is more than the current balance, and If stored in db, it will mess with the interactive operation
            cursor.execute("UPDATE user_transaction SET amount = ? WHERE account_no = ?", (newBalance, userBio2[2]))
        
        
        userCurrentTransactionRecord = f"{userBio2[3]}, you {transaction_type} {debitAmount} on {date_and_time}. Your balance is now {newBalance}\n\n"
        # Updated History
        userUpdatedHistory =  f"{userPreviousHistory[3]} {userCurrentTransactionRecord}" 

        cursor.execute("UPDATE user_transaction SET transaction_type = ? WHERE account_no = ?", (transaction_type, userBio2[2]))
        cursor.execute("UPDATE user_transaction SET timestamp = ? WHERE account_no = ?", (date_and_time, userBio2[2]))
        
        #update history
        cursor.execute("UPDATE user_history_transaction SET history = ? WHERE account_no = ?", (userUpdatedHistory, userBio2[2]))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()
        print(f"{debitAmount} successfully withdraw !!!\n\n")
        print(f"Current Balance: {newBalance}\n\n")
        # print(userTransactResult)
    
    
    
def checkbalance(userBio2):
    
     # Connect to the SQLite database
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cursor = conn.cursor()

    # locate user transaction data in user_transaction table with account number
    cursor.execute("SELECT * FROM user_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
    userTransactResult = cursor.fetchone()  # returns the user's transaction data bio from the table as a tuple
    # print(userTransactResult)
    
    # Close the connection
    conn.close()
    
    
    current_balance_in_db = getBalance1(userTransactResult[5])
    print(f"{userTransactResult[1]}, your current balance in your bank account is {current_balance_in_db}\n\n")




def sendMoney(userBio2):
    amountToSend = int(input("Amount you want to send: "))
    receiverName = input("Name of receiver: ")
    receiverAccount = int(input("Account number of receiver: "))
    
    # if receiver account is same as senders account, reject the transaction
    if receiverAccount == userBio2[2]:
        print(f"\n\nHi {userBio2[3]}, you can't transfer money to yourself !!!, but you can only deposit.\n\n")
    else:
        # else, proceed with transfer of fund
        import sqlite3
        # Connect to the SQLite database
        conn = sqlite3.connect(get_dynamic_db_filepath())
        cursor = conn.cursor()
        
        def getSenderData():
            # locate sender's transaction data in user_transaction table with sender's name and account number
            cursor.execute("SELECT * FROM user_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
            senderTransactResult = cursor.fetchone()  # returns the user's transaction data bio from the table as a tuple
            return senderTransactResult
        # print(getSenderData())
        senderTransactData = getSenderData()
        sendersPreviousBalance = senderTransactData[5]
        # senderDedubtion = amountToSend

        def getRecieverData():
            # locate receiver's transaction data in user_transaction table with receiver's name and account number
            cursor.execute("SELECT * FROM user_transaction WHERE account_name = ? AND account_no = ?", (receiverName, receiverAccount))
            recieverTransactResult = cursor.fetchone()  # returns the user's transaction data bio from the table as a tuple
            return recieverTransactResult
        # print(getRecieverData())
        recieverTransactData = getRecieverData()
        recieversPreviousBalance = recieverTransactData[5]
        recieversAccountNum = recieverTransactData[2]
        recieversName = recieverTransactData[1]
        
        
        # Define the new value
        # remove money from sender account
        sendersNewBalance = debitAmount1(amountToSend, sendersPreviousBalance)
        # add money to receiver account
        recieversNewBalance = creditAmount1(amountToSend, recieversPreviousBalance)
        # print(sendersNewBalance)
        # print(recieversNewBalance)
        
        
        if sendersNewBalance == "You can't input a negative value" or sendersNewBalance == "Debit amount exceed account balance":
            return sendersNewBalance
        elif recieversNewBalance == "You can't input a negative value" or recieversNewBalance == "Amount must be between 10 and 100,000 naira":
            return recieversNewBalance
        else:
            # Record History Section
            # Senders History
            cursor.execute("SELECT * FROM user_history_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
            sendersPreviousHistory = cursor.fetchone()  # returns the user's previous History transaction data bio from the table as a tuple
            # print(sendersPreviousHistory)
            
            # recievers History
            cursor.execute("SELECT * FROM user_history_transaction WHERE account_name = ? AND account_no = ?", (recieversName, recieversAccountNum))
            receiversPreviousHistory = cursor.fetchone()  # returns the user's previous History transaction data bio from the table as a tuple
            # print(receiversPreviousHistory)
            
            
            transaction_type = "transfer"
            # Update the balance value for the reciever
            if recieversNewBalance != None:     # None is return as a value if amount to withdraw is more than the current balance, and If stored in db, it will mess with the interactive operation
                cursor.execute("UPDATE user_transaction SET amount = ? WHERE account_no = ?", (recieversNewBalance, recieversAccountNum))
            
            
            # Update the balance value for the reciever
            if sendersNewBalance != None:     # None is return as a value if amount to withdraw is more than the current balance, and If stored in db, it will mess with the interactive operation
                cursor.execute("UPDATE user_transaction SET amount = ? WHERE account_no = ?", (sendersNewBalance, userBio2[2]))
            
            # Prepare record
            sendersCurrentTransactionRecord = f"{userBio2[3]}, you {transaction_type}ed {amountToSend} to {recieversName} on {date_and_time}. Your balance is now {sendersNewBalance}\n\n"
            receiversCurrentTransactionRecord = f"{recieversName}, you recieved a fund {transaction_type} of {amountToSend} from {userBio2[3]} on {date_and_time}. Your balance is now {recieversNewBalance}\n\n"
            
            # Bind old and new history together
            sendersUpdatedHistory =  f"{sendersPreviousHistory[3]} {sendersCurrentTransactionRecord}"
            receiversUpdatedHistory = f"{receiversPreviousHistory[3]} {receiversCurrentTransactionRecord}" 

            # Updated last transaction process mode in transaction table 
            cursor.execute("UPDATE user_transaction SET transaction_type = ? WHERE account_no = ?", (transaction_type, userBio2[2]))
            cursor.execute("UPDATE user_transaction SET timestamp = ? WHERE account_no = ?", (date_and_time, userBio2[2]))
            
            if recieversNewBalance != None:
                #update history
                cursor.execute("UPDATE user_history_transaction SET history = ? WHERE account_no = ?", (sendersUpdatedHistory, userBio2[2]))
                cursor.execute("UPDATE user_history_transaction SET history = ? WHERE account_no = ?", (receiversUpdatedHistory, recieversAccountNum))
            # Commit the changes
            conn.commit()

            # Close the connection
            conn.close()
            
            
            
            # Final message on sucessful or failed transaction
            if recieversNewBalance != None:
                successMessage = f"\n\n{userBio2[3]}, your {transaction_type} of {amountToSend} sent to {recieversName} on {date_and_time} was successful. You now have a balance of {sendersNewBalance}\n\n"
                print(successMessage)
            else:
                print(f"Transfer was not successful\n\n")
            # print(userTransactResult)
     
    
    
def transactionHistory(userBio2):
    print("Check transaction history\n\n\n")
   
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cursor = conn.cursor()

    # locate user transaction data in user_transaction table with account number
    cursor.execute("SELECT * FROM user_history_transaction WHERE account_name = ? AND account_no = ?", (userBio2[3], userBio2[2]))
    userTransactResult = cursor.fetchone()  # returns the user's transaction data bio from the table as a tuple
    print(userTransactResult[3])
    
    # Close the connection
    conn.close()
    

# Main app interface after successful login
def mainBankApp(userBio):
    print(f"Hello {userBio[3]}, Select your options below\n\n")
    while True:
        try:
            firstInput = int(input(f"1. Deposit\n2. Withdraw\n3. Send Money\n4. Check Balance\n5. Transaction History\n6. Log Out\n\n {userBio[3]}'s response: "))
            if firstInput == 6:
                print(f"\nHi {userBio[3]}, we hope you had a stress free transaction today ?. Bye !!!\n")
                # logOut(userBio)
                break
            elif firstInput == 1:
                print("\nDeposit.....\n")
                deposit(userBio)
            elif firstInput == 2:
                print("\nWithdraw.....\n")
                withdraw(userBio)
            elif firstInput == 3:
                print("\nSending Money.....\n")
                sendMoney(userBio)
            elif firstInput == 4:
                print("\nChecking Balance......\n")
                checkbalance(userBio)
            elif firstInput == 5:
                print("\nTransaction History.......\n")
                transactionHistory(userBio)
            else:
                print("\nWrong input, kindly input the right option.\n")
                continue
        except ValueError:
            print("\n\nYou have not made any selection yet, kindly do so before pressing 'Enter'.\n\n")
            input("...Press 'Enter' \n\n")
            continue




def validate_password(password):
    # Check if the input is numeric
    if not password.isdigit():
        return False

    # Verify the length (4 digits)
    if len(password) != 4:
        return False

    return True




print("\n\n\n")
print("Welcome to W.A.V.E Bank, how can we help you ?")


#Internal functions here
def register():
    name = input("What is your name: ")
    email = input("Your email: ")
    gender = input("Your gender (male / female): ")
    
    # validate gender
    while True:
        if gender == "male" or gender == "female":
            gender
            break # break out of inner loop and move to next operation
        else:
            print("you inputed the wrong value. Please input the right answer.\n")
            gender = input("Your gender (male / female): ")
            # by default continue
    print(gender)
    
    stateOfOrigin = input("Your state of Origin: ")
    country = input("Your country: ")
    password = input("your password (any 4 digits only): ")
    
    # validate password
    while True:
        if validate_password(password):
            print("\nValid password!")
            break
        else:
            print("\nInvalid password. Please enter a 4-digit numeric password.\n")
            password = input("your password (any 4 digits only): ")
            # by default continue
    
    # clock -> date and time 
    cur_date_and_time = date_and_time
    
    
    print("\n\nRegistration Successful !!!\n")
    # generate unique id number, account number, date and time of registaration
    generate_random_acct_num = int(''.join([str(random.randint(1, 9)) for _ in range(10)])) #generate new account number
    print(f"\nYour Account Number is {generate_random_acct_num}\n")
    generate_unique_id_num = int(''.join([str(random.randint(1, 9)) for _ in range(3)])) #generate new ID number
    print(f"Your unique ID is {generate_unique_id_num}\n\n")
    
    # save or insert items into database customer table
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cur = conn.cursor()
    cur.execute("INSERT INTO user_register VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (cur_date_and_time, generate_unique_id_num, generate_random_acct_num, name, email, gender, stateOfOrigin, country, password))
    
    
    # # create an account for new user in user_transaction table 
    # insert in user_transaction table (unique_id_no INT, account_name TEXT, account_no INT, transaction_id INTEGER PRIMARY KEY, transaction_type TEXT, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("INSERT INTO user_transaction VALUES (?, ?, ?, ?, ?, ?, ?)", (generate_unique_id_num, name, generate_random_acct_num, generate_unique_id_num, "open account", 0, cur_date_and_time))
    cur.execute("INSERT INTO user_history_transaction VALUES (?, ?, ?, ?)", (generate_unique_id_num, name, generate_random_acct_num, f"Open Account on {cur_date_and_time}\n\n"))
    conn.commit()
    conn.close()
    # print("\n\nRegistration Successful !!!\n\n")
    # print("User Account Created !!!")
    
    # output notification to confirm registration successful
    # print(f"Thank you {name}, you have successfully registered your account, kindly remember your account number and password for logging in.")
    input("...press 'Enter' to proceed... ")
    

def deleteAccount():
    accountNumToDelete = int(input("Account to be deleted: "))
    # uniqueID = int(input("input your Unique ID number"))
    import sqlite3

    # Connect to your SQLite database
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cursor = conn.cursor()

    # Suppose you have a table called "people" with columns (name, address, phone)
    # To delete the row with rowid 1000:
    cursor.execute(f"DELETE FROM user_register WHERE account_no = {accountNumToDelete}")
    cursor.execute(f"DELETE FROM user_transaction WHERE account_no = {accountNumToDelete}")
    cursor.execute(f"DELETE FROM user_history_transaction WHERE account_no = {accountNumToDelete}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"\n\nAccount {accountNumToDelete} was successfully deleted !!!\n\n")





    
def logIn():
    acct_no = input("what is your account number: ")
    password = input("password: ")
        
    # # if these above details are in the database, Welcome user, else tell user to confirm if details are correct or ensure registeration of exam
    # # validate password
    while True:
        if validate_password(password):
            print("Valid password!")
            break
        else:
            print("Invalid password. Please enter a 4-digit numeric password.\n")
            password = input("your password (any 4 digits only): ")
            # by default continue
            
    """if details are ok, search the registration database to confirm that it exist, else encourage user 
        to go and register before coming back to log in"""
            
    print(f"\n\nLoggin in account {acct_no}\n\n")
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect(get_dynamic_db_filepath())
    cursor = conn.cursor()


    # Execute a query to check if the account name and password exist in the registration table
    cursor.execute("SELECT * FROM user_register WHERE account_no = ? AND password = ?", (acct_no, password))
    result = cursor.fetchone()  # returns the register user's bio from the table as a tuple

    # print(result)
    # Close the database connection
    conn.close()

    # Check if the result is not None (i.e., account name and password match)
    if result:
        print(f"\nAccess granted. Welcome {result[3]}, you are logged in now !\n")
        mainBankApp(result)
    else:
        print("\nAccess denied. \nIncorrect account name or password. If you don't have an account with us yet, kindly register before loggin in\n")

        


# Main Interface
while True:
    try:
        firstInput = int(input("1. Open an Account\n2. log into my account\n3. Close down my account\n4. Quit\n\n user's response: "))
        if firstInput == 4:
            print("\nThank you for banking with us, We look forward to see you soon. Bye !!!\n")
            break
        elif firstInput == 1:
            print("\nKindly Register your Bio data with us\n")
            register()
        elif firstInput == 2:
            print("\nlog in account info\n")
            logIn()
        elif firstInput == 3:
            print("\nClose down my account info\n")
            deleteAccount()
        else:
            print("\nWrong input, kindly input the right option.\n")
            continue
    except ValueError:
        print("\n\nYou have not made any selection yet, kindly do so before pressing 'Enter'.\n\n")
        input("...Press 'Enter' ")
        continue