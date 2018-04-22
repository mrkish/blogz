import re

def verify_email(email):
    '''Checks for valid email via regex; returns a bool.
    Only admits common TLD emails.'''

    valid_email = re.compile('\w.+@\w+.(net|edu|com|org)')

    if valid_email.match(email):
        return True
    else:
        return False

#
def verify_password(password, verify):
    '''Checks for password symmetry and min. requirements via regex; returns a bool.
    Requirements: 8-20 length, 1 special, 1 uppercase, 1 digit'''

    valid_pass = re.compile(
        '(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@$#!%*?&]{8,20}')

    if password == verify and valid_pass.match(password):
        return True
    else:
        return False
