import json
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
        if command == "help":
            help()
        elif command == "add":
            add(additional, additional2)
        elif command == "show":
            show(additional)
            refreshkeys()
        elif command == "remove":
            remove(additional)
        elif command == "refresh":
            refreshkeys()
        elif command == "keys":
            (pub, priv) = fetchKeys()
            print(pub, priv)
        elif command == "genkeys":
            generateKeys()
        elif command == "genpass":
            passwordGen()

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
        refresh      Refresh account information
        genpass      Create and generate a strong password of the length of your choice
        keys         View your current RSA encryption keys protecting your passwords
        genkeys      Generate new keys. This will also be done automatically everytime you run "passman show".
        help         Show this help message

    Examples:
        passman add                        
        passman add Google                # Add a new account named "Google"
        passman add Facebook password     # Add a new account named "Facebook" with password "password"
        passman show                        # Promted to a list to choose your account from
        passman show all                       # Show all accounts
        passman show Google               # Show account password for "Google"
        passman refresh                     # Refresh keys

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
                    message = "Choose Account:",
                    choices = ['Y', 'N']
                ).execute()
        if message.upper() == "Y":
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
        return
    
    def genpass(length):
        digits = [x for x in "0123456789"]
        lowercase = [x for x in "abcdefghijklmnopqrstuvwxyz"]
        uppercase = [x for x in "abcdefghijklmnopqrstuvwxyz".upper()]
        special = [x for x in "!@#$%^&*()_+~|}{:'?><" +'"']
        combinedList = digits + lowercase + uppercase + special

        password = "" + random.choice(uppercase) + random.choice(lowercase) + random.choice(special)
        for i in range (length - 3):
            password += random.choice(combinedList)

        return password
    
    def passwordGen():
        length = inquirer.select(
                    message = "Choose Length of Password to be generated:",
                    choices = [12, 16, 24]
                ).execute()
        password = genpass(length=length)
        print("\t", password)
        savePassword = inquirer.select(
                    message = "Do you want to save this password for an account?",
                    choices = ["yes", "no"]
                ).execute()
        if savePassword == "yes":
            chooseIt = ["Create a New Account"]
            for k, v in accounts.items():
                chooseIt.append(k)
            accountName = inquirer.select(
                message = "Choose the account:",
                choices = chooseIt
            ).execute()

            if accountName == "Create a New Account":
                add(password=password)
            else:
                add(accountName=accountName, password=password)

    n = len(sys.argv)

    arguments = ("help", "-h", "add", "-a", "show", '-s', "remove", "-rm", "keys", "refresh", "-r" "genkeys", "genpass", "-p")

    if os.path.isfile("accountinfo.json"):
        with open("accountinfo.json", "r") as f:
            accounts = json.load(f)
    else:
        accounts = {}

    appname = "passman"

    if n < 2:
        print(f"Usage: {appname} command. Use {appname} help for more info.")
    elif sys.argv[1] not in arguments:
        print("No use for the command {", sys.argv[1], "} found. Try using appname.py help.")

    if n == 2:
        assign_task(sys.argv[1])
    elif n == 3:
        assign_task(sys.argv[1], sys.argv[2])
    elif n == 4:
        assign_task(sys.argv[1], sys.argv[2], sys.argv[3]) 


#main()