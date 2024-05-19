import json
import pprint
import random
import sys
import time
import base64
import os.path
import getpass
from tabulate import tabulate
import json
import rsa
from InquirerPy import inquirer
import signal


def main():
    try:
        def generateKeys():
            (pubkey, privkey) = rsa.newkeys(512)
            keyData = {
                "public_key": pubkey.save_pkcs1().decode(),
                "private_key": privkey.save_pkcs1().decode()
            }

            with open("keys.json", 'w') as f:
                json.dump(keyData, f)


        def fetchKeys():
            while True:
                try:
                    with open("keys.json", "r") as f:
                        keyData = json.load(f)
                        pubkey = rsa.PublicKey.load_pkcs1(keyData['public_key'].encode())
                        privkey = rsa.PrivateKey.load_pkcs1(keyData['private_key'].encode())
                        return pubkey, privkey
                except FileNotFoundError:
                    print("No Keys Found. Generating Keys. Please wait...")
                    generateKeys()
                
            
        (pubkey, privkey) = fetchKeys()

        def encrypt(data, pubkey):
            return rsa.encrypt(data, pubkey)

        def decrypt(data, privkey):
            try: 
                return rsa.decrypt(data, privkey)
            except rsa.pkcs1.DecryptionError:
                print("Decryption Error. Did you change the keys?")
                return


        def refreshkeys():
            tempAccounts = {}
            (pubkey, privkey) = fetchKeys()
            for k,v in accounts.items():
                account, password = k, decrypt(base64.b64decode(v), privkey).decode("utf-8")
                tempAccounts[account] = password

            generateKeys()
            (pubkey, privkey) = fetchKeys()

            try:
                for account, password in tempAccounts.items():
                    encyrptedPW = encrypt(password.encode("utf-8"), pubkey)
                    tempAccounts[account] = base64.b64encode(encyrptedPW).decode("utf-8")

                with open("accountinfo.json", "w") as f:
                    json.dump(tempAccounts, f)
            except Exception as e:
                print("An error occurred while writing to the file:", e)
                

        def assign_task(command, additional="", additional2="", additonal3=""):
            if command in ["help", "-h"]:
                help()
            elif command in ["add", "-a"]:
                add(additional, additional2)
            elif command in ["show", "-s"]:
                show(additional)
                refreshkeys()
            elif command in ["remove", "-rm"]:
                remove(additional)
            elif command in ["refresh", "-r"]:
                refreshkeys()
            elif command == "keys":
                (pub, priv) = fetchKeys()
                print(pub, priv)
            elif command == "genkeys":
                generateKeys()
            elif command in ["genpass", "-p"]:
                passwordGen()
            elif command in ["usergen", "-cu"]:
                createUser()
            elif command in ["user", "-u"]:
                showUser()

            return

        def add(accountName="", password=""):
            (pubkey, privkey) = fetchKeys()
            if not accountName:
                accountName = input("Enter The Account Name: ")

            if accounts.get(accountName) is not None:
                message = input("Password for this account is already entered. Overrite? This cannot be undone. [Y]/[N]? ")
                if message.upper() == "N":
                    return
                
            if not password:        
                password = getpass.getpass(f"Enter Password for {accountName}: ", stream=sys.stderr).encode("utf-8")
            else:
                password = password.encode("utf-8")

            encyrptedPW = encrypt(password, pubkey)
            accounts[accountName] = base64.b64encode(encyrptedPW).decode("utf-8")
            try:
                with open("accountinfo.json", "w") as f:
                    json.dump(accounts, f)
            except Exception as e:
                print("An error occurred while writing to the file:", e)
            # print(accounts)
            print("Password saved successfully.")
            return

        def show(name=""):
            (pubkey, privkey) = fetchKeys()
            showAccounts = {}
            for k,v in accounts.items():
                try:
                    account, password = k, decrypt(base64.b64decode(v), privkey).decode("utf-8")
                    showAccounts[account] = password
                except Exception as e:
                    print("An error occured. Error:", e, "Have you changed the keys?")
                    return
            
            if name == "all":
                # pprint.pprint(showAccounts)
                table_data = [(key, value) for key, value in showAccounts.items()]
                table = tabulate(table_data, headers=["Account", "Password"], tablefmt="github")
                print(table)
                print(" ")
            elif name == "accounts":
                print("Accounts: ")
                for key, _ in showAccounts.items():
                    print(key)
                print(" ")

            else:
                if not name:
                    chooseIt = []
                    for k, v in accounts.items():
                        chooseIt.append(k)
                    accountName = inquirer.select(
                        message = "Choose the account:",
                        choices = chooseIt
                    ).execute()
                else:
                    accountName = name

                if accountName not in showAccounts:
                    message = input("Account not found. Add a new account with that name? [Y]/[N]? ")
                    if message.upper() == "Y":
                        add(name)
                    return
                else:
                    table_data = [(accountName, showAccounts[accountName])]
                    table = tabulate(table_data, headers=["Account", "Password"], tablefmt="github")
                    print(table)
                    print(" ")

                tableLines = table.count("\n") + 2

            def ignore_ctrl_c(signum, frame):
                print("                             ", end="\r")
                for i in range(tableLines):
                    print("\033[F", end="")  # Move cursor up one line
                    print("\033[K", end="")
                sys.exit(0)
            
            original_handler = signal.getsignal(signal.SIGINT)
            signal.signal(signal.SIGINT, ignore_ctrl_c)
            for i in range(7, 0, -1):
                print(f"clearing screen in {i} seconds.", end="\r")
                time.sleep(1)
            print("                             ", end="\r")
            signal.signal(signal.SIGINT, original_handler)
            
            for i in range(tableLines):
                print("\033[F", end="")  # Move cursor up one line
                print("\033[K", end="")
            
            sys.exit(0)

        def help():
            help_message = """
        Passman - Password Manager

        Usage:
            passman command

        Commands:
            add          Add a new account
            show         Show account information
            refresh      Refresh account information and rsa keys. This will also be done automatically everytime you run "passman show".
            remove       Remove an account
            genpass      Create and generate a strong password of the length of your choice
            keys         View your current RSA encryption keys protecting your passwords
            genkeys      Generate new keys.
            usergen      Creates a new user information overriding the old one. This data is used during passoword generation.
            help         Show this help message

        Alternate Commands for Ease of Use:
            add: -a
            show: -s
            refresh: -r
            remove: -rm
            genpass: -p
            help: -h


        Examples:
            passman add
            passman -a                        
            passman add Google                # Add a new account named "Google"
            passman -a Google
            passman add Facebook password     # Add a new account named "Facebook" with password "password"
            passman -a Facebook password
            passman show                        # Promted to a list to choose your account from
            passman show all                       # Show all accounts
            passman show Google               # Show account password for "Google"
            passman refresh                     # Refresh keys
            passman -r
            passman remove Google               # Removes Google
            passman -rm Google
            passman -u

        For more information and source code, visit: https://github.com/nareshkarthigeyan/passwordManager

        Note:
            - Passwords are encrypted using RSA encryption.
            - Passwords will disappear from the screen after 7 seconds.

        Made with Love by K V Naresh Karthigeyan
        """
            print(help_message)
            return

        def remove(alll=""):
            message = inquirer.select(
                        message = "This process is irreversible. Continue?",
                        choices = ['yes', 'no']
                    ).execute()
            if message == "yes":
                if alll == "all":
                    with open("accountinfo.json", 'w') as json_file:
                        # Write an empty JSON object to the file
                        json.dump({}, json_file)
                else:
                    chooseIt = []
                    for k, v in accounts.items():
                        chooseIt.append(k)
                    alll = inquirer.select(
                        message = "Choose Account:",
                        choices = chooseIt
                    ).execute()

                if alll in accounts:
                    accounts.pop(alll)
                    with open("accountinfo.json", "w") as f:
                        json.dump(accounts, f)
                    print(f"Succesfully removed{alll}")            
            return
        
        def genpass(length, personalized, frequency):
            digits = "0123456789"
            lowercase = "abcdefghijklmnopqrstuvwxyz"
            uppercase = "abcdefghijklmnopqrstuvwxyz".upper()
            special = "!@#$%^&*()_+~|}{:'?><" +'"'
            combinedList = list(digits + lowercase + uppercase + special)
            passwordsFinal = []
            for i in range(frequency):
                userSpecific = ""
                userSpecific2 = ""
                if personalized == "yes":
                    try: 
                        with open("userinfo.json") as f:
                            userinfoDic = json.load(f)
                            userinfoRaw = list(userinfoDic.values())
                            userinfo = [x for x in userinfoRaw if x != ""]
                            random.shuffle(userinfo)
                        ran = random.choice(userinfo).replace(" ", "")

                        if len(ran) < length - 6:
                            randomIndex = random.randint(len(ran)//3, len(ran))
                        else:
                            ran = random.choice([ran[length:], ran[:length]])
                            randomIndex = random.randint(len(ran)//3, len(ran))

                        for i in ran[:randomIndex]:
                            userSpecific += random.choice([i.upper(), i.lower()])
                        for i in ran[randomIndex:]:
                            userSpecific2 += random.choice([i.upper(), i.lower()])

                    except FileNotFoundError:
                        answer = inquirer.select(
                            message = "No user data detected. Add user data now?",
                            choices = ["yes", "no"]
                        ).execute() 
                        if answer == "yes":
                            createUser()
                            print("User info created successfully. Run the command again to generate a personalized password.")
                            sys.exit(0)
                        elif answer == "no":
                            userSpecific = ""
                            userSpecific2 = ""

                passwordList = [random.choice(uppercase)] + [random.choice(lowercase)] + [random.choice(special)] + [random.choice(digits)] + [userSpecific] + [userSpecific2]
                lengthDone = len("".join(passwordList))
                for i in range (length - lengthDone):
                    passwordList.append(random.choice(combinedList))
                random.shuffle(passwordList)
                password = "".join(passwordList)
                passwordsFinal.append(password[0:length])
            return passwordsFinal
        
        def passwordGen():
            frequency = type = inquirer.select(
                        message = "Number of Passwords you want to generate: ",
                        choices = [1, 2, 4, 8, 12, 16]
                    ).execute()
            type = inquirer.select(
                        message = "Do you want to personalize your Password with your info? (may not always work)",
                        choices = ["yes", "no"]
                    ).execute()
            length = inquirer.select(
                        message = "Choose desired characted length of the Password:",
                        choices = [12, 16, 24]
                    ).execute()
            passwordsList = genpass(length=length, personalized=type, frequency=frequency)
            print("Generated Password(s):")
            for passes in passwordsList:
                print("\t", passes)
            savePassword = inquirer.select(
                        message = "Do you want to save any one of these passwords for an account?",
                        choices = ["yes", "no"]
                    ).execute()
            
            if savePassword == "yes":
                choosePassword = inquirer.select(
                            message = "Choose one of the generated passwords: ",
                            choices = passwordsList
                        ).execute()
                print("\t", choosePassword)
                chooseIt = ["Create a New Account"]
                for k, v in accounts.items():
                    chooseIt.append(k)
                accountName = inquirer.select(
                    message = "Choose the account:",
                    choices = chooseIt
                ).execute()

                if accountName == "Create a New Account":
                    add(password=choosePassword)
                else:
                    add(accountName=accountName, password=choosePassword)

        def createUser():
            print("Creating a User Profile for ease of personalized Password generation...")
            time.sleep(0.5)
            print("Proceed below (leave empty for questions you cannot answer): ")
            userinfo = {}
            userinfo["firstName"] = input("First Name: ")
            userinfo["middleName"] = input("Middle Name: ")
            userinfo["lastName"] = input("Last Name: ")
            userinfo["partnerName"] = input("Partner's Name (if any): ")
            userinfo["petName"] = input("Pet's Name (if any): ")
            userinfo["DOB"] = input("Your Date of Birth in DDMMYYY: ")
            userinfo["day"] = userinfo["DOB"][:2]
            userinfo["month"] = userinfo["DOB"][2:4]
            userinfo["year"] = userinfo["DOB"][4:]
            months = {"": "", "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "Novmember", "12": "December"}
            userinfo["monthInWords"] = months[userinfo["month"]]
            userinfo["favourites"] = input("Favourite (word/adjective/thing/person/etc.): ")

            moreInfo = inquirer.select(
                        message = "Do you want to add more info in order to better facilitate password generation?",
                        choices = ["yes", "no"]
                    ).execute()
            
            if moreInfo == "yes":
                userinfo["Occupation"] = input("Occupation: ")
                userinfo["workplace"] = input("Place of Work: ")
                userinfo["School"] = input("School Name: ")
                userinfo["Childhool Crush"] = input("Childhood Crush: ")
                userinfo["Room Number"] = input("Room Number: ")
                userinfo["Book"] = input("Favourite Book: ")
                userinfo["celebrity crush"] = input("Celebrity Crush: ")
                userinfo["color"] = input("Favourite color: ")
                userinfo["Hobby"] = input("Favourite Hobby: ")
                userinfo["LastMovie"] = input("Last Movie Watched: ")
                userinfo["favMovie"] = input("Favourite Movie Watched: ")
                userinfo["ex"] = input("Ex's Name: ")
                userinfo["partnerBday"] = input("Your current parter's Birthday in DDMMYYYY: ")
                userinfo["pday"] = userinfo["DOB"][:2]
                userinfo["pmonth"] = userinfo["DOB"][2:4]
                userinfo["pear"] = userinfo["DOB"][4:]
                userinfo["monthInWords"] = months[userinfo["pmonth"]]
                userinfo["email"] = input("E-mail: ")
                userinfo["memory"] = input("Favourite Memory: ")
                userinfo["annevesary"] = input("Anniversary: ")


            userinfo["misc"] = "."

            with open("userinfo.json", "w") as f:
                json.dump(userinfo, f)

        def showUser():
            try:
                with open("userinfo.json") as f:
                    userinfo = json.load(f)
                    pprint.pprint(userinfo)
            except FileNotFoundError:
                print("No user info found. Create one using the command 'usergen' or '-cu'")
                sys.exit(0)

        n = len(sys.argv)

        arguments = ("help", "-h", "add", "-a", "show", '-s', "remove", "-rm", "keys", "refresh", "-r" "genkeys", "genpass", "-p", "usergen", "-cu", "user", '-u')

        if os.path.isfile("accountinfo.json"):
            with open("accountinfo.json", "r") as f:
                accounts = json.load(f)
        else:
            accounts = {}

        appname = "passman"

        if n < 2:
            help()
            print(f"Usage: {appname} command.")
        elif sys.argv[1] not in arguments:
            print("No use for the command {", sys.argv[1], "} found. Try using appname.py help.")

        if n == 2:
            assign_task(sys.argv[1])
        elif n == 3:
            assign_task(sys.argv[1], sys.argv[2])
        elif n == 4:
            assign_task(sys.argv[1], sys.argv[2], sys.argv[3]) 
    except KeyboardInterrupt:
        sys.exit(0)

# main()
if __name__ == "__main__":
    main()