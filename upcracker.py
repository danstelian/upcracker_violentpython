"""
Module documentation
UNIX Password Cracker
A script from the book Violent Python by TJ. O'Connon
Uses the crypt() algorithm that hashes UNIX passwords
"""
import crypt
import os
from time import sleep
from collections import namedtuple


Users = namedtuple('Users', ['user', 'passwd'])


def test_passwd(user_list, path_dict):
    """
    function documentation
    takes the user/password list and the dictionary file as parameters
    prints a message indicating the matching word for each encrypted password hash
    or prints "not found" after exhausting the words in the dictionary
    """
    print('Opening the dictionary file')

    with open(path_dict) as file_dict:
        for usr, pas in user_list:  # for every passward in the list

            file_dict.seek(0)  # for each loop, start reading from the top of the file
            salt = pas[:2]  # strips out the salt from the first two characters of the encrypted password hash
            sleep(1)
            print(f'{usr} : {pas}', end=' | ')

            found = False
            for word in file_dict:  # iterates through each word in the dictionary
                word = word.rstrip()
                word_crypt = crypt.crypt(word, salt)  # creates an encrypted password hash from the word and the salt
                if word_crypt == pas:  # if the resulted hash matches the password hash
                    print(f'found: {word}')
                    found = True
                    break

            if not found:
                print('not found')
    return None


def get_passwd(path_pass):
    """
    function documentation
    takes the password file as a parameter
    opens the encrypted password file and reads the content of each line in the file
    for each line, it splits out the username and the hashed password; returns them as pairs in a list
    the main function calls the test_passwd() function; tests each hashed passwords against a dictionary file
    """
    print('Opening the passwd file...', end=' ')

    with open(path_pass) as file_pass:
        try:
            user_list = [Users(line.split(':')[0].strip(), line.split(':')[1].strip()) for line in file_pass if line.strip()]
            # extracts the first two columns separated by colon from the password file; removes all whitespaces
        except Exception as e:
            print(e)
            return None

        if user_list:  # if the list is not empty
            print('{0} passwords found'.format(len(user_list)))
            for usr in user_list:
                print(f'{usr.user}: {usr.passwd}')
            return user_list  # returns list after printing the content
        else:
            print('0 passwords found')
            return None  # returns None if the list is empty; no passwords found


def main():
    """
    main function documentation
    employs the two functions get_passwd() and text_passwd() to
    get a list of user/password pairs from "passwords.txt"
    tests passwords against every word in "dictionary.txt"
    """
    path_pass = os.path.join(os.path.dirname(__file__), 'passwords.txt')
    path_dict = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
    # searches for the two files "passwords.txt" and "dictionary.txt" in the same dir as the running script
    if os.path.isfile(path_pass) and os.path.isfile(path_dict):  # verifies the existence of the files
        user_list = get_passwd(path_pass)
        if user_list:  # if the returned list is not empty
            print()
            sleep(1)
            test_passwd(user_list, path_dict)
    else:
        print('Unable to locate "passwords.txt" and/or "dictionary.txt"')


if __name__ == "__main__":
    main()
