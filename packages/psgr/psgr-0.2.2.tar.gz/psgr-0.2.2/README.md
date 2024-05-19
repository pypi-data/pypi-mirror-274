# PSGR - Password Manager

PSGR is a command-line based password manager that helps you manage and store your account credentials securely using RSA encryption. The passwords are stored locally in a JSON file that is encrypted. It provides functionalities for adding, viewing, removing, and generating passwords, along with user information management for personalized password generation.

## Features

### Add Account:

Add new account credentials.

```
passman add AccountName Password
```

```
passman -a
```

## Show Account:

Display stored account credentials.

```
passman show
```

```
passman -s
```

## Remove Account:

Remove an account from storage.

```
passman remove
```

```
passman -rm
```

## Generate Password:

Create strong passwords, with options for personalization.

```
passman genpass
```

```
passman -p
```

## User Information Management:

Store user information to facilitate personalized password generation.

```
passman -u
```

To create and ovverrite an existing user data:

```
passman -cu
```

## Help:

Display a help message detailing all available commands.

```
passman help
```

```
passman -h
```

## Installation

To run Passman, you need to have Python installed on your system along with the following packages:

```
rsa
tabulate
InquirerPy
```

You can install the entire package in a simple command:

```
pip install psgr
```

# Author

K V Naresh Karthigeyan
