import random

def genpass(length):
    digits = [x for x in "0123456789"]
    lowercase = [x for x in "abcdefghijklmnopqrstuvwxyz"]
    uppercase = [x for x in "abcdefghijklmnopqrstuvwxyz".upper()]
    special = [x for x in "!@#$%^&*()_+~|}{:'?><" +'"']
    combinedList = digits + lowercase + uppercase + special

    password = ""
    for i in range (length):
        password += random.choice(combinedList)

    return password
