import pyperclip
import inquirer
import os
import dotenv

dotenv.load_dotenv()
ACCESS_PASSWORD = os.getenv('PASSWORD')
os.system('cls')


def read_password_file(filename, separator=':'):
    """Opens a text file of account/password key-value pairs separated by a string.

        For example: 
        `account;password`

        Parameters:
        ----------
        filename : str
            Name of the file.
        separator : str
            String that separates the account name and the password.

        Returns: 
        ----------
        dict
            Dictionary of accounts and passwords.
    """

    with open(filename, encoding='utf-8') as file:
        read_data = file.read()

        lines = read_data.split('\n')

        account_password_dict = {}

        for line in lines:
            # Split the account and password as they are separated by a colon in the file
            [account, password] = line.split(separator)
            # Populate dictionary with account-password key-value pairs
            account_password_dict[account] = password

    file.close()
    return account_password_dict


def write_to_password_file(filename, account_name, password):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write('\n' + account_name + ':' + password)
    file.close()


def get_or_add():
    decision = inquirer.prompt([inquirer.List(
        'decision', message='What would you like to do?', choices=['Get a password', 'Add a password'])])
    if(decision['decision'] == 'Get a password'):
        return True
    return False


# Welcome user and ask for access password
access_password = inquirer.prompt([inquirer.Password(
    'password', message='Welcome, please enter your access password:')])

if(access_password['password'] == ACCESS_PASSWORD):
    # Ask user if they want to get or add a new password
    if (get_or_add()):
        # If they want to get a password:
        account_password_dict = read_password_file('.passwords.txt', ':')

        # Display accounts
        account = inquirer.prompt([
            inquirer.List('account', message='Which account would you like the password for?',
                          choices=account_password_dict.keys())
        ])

        os.system('cls')

        # Copy selected password to clipboard
        pyperclip.copy(account_password_dict[account['account']])

        print('\nCopied to clipboard!')
    else:
        # If they want to add a password:
        new_account = inquirer.prompt([inquirer.Text('name', message='What is the name of the account?'), inquirer.Password(
            'password', message='What is the password for {name}')])
        write_to_password_file(
            '.passwords.txt', new_account['name'], new_account['password'])

        os.system('cls')
        print('\nAdded account!')
