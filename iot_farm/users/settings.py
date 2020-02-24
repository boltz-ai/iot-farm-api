"""
Settings for app users
"""

MOBILE_REGEX = r'\d+'
MOBILE_ERROR = r'Enter valid mobile number.'

# Password regex
# Minimum eight characters, at least one letter and one number:
PASSWORD_REGEX_1 = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

# Minimum eight characters, at least one letter, one number and one special character:
PASSWORD_REGEX_2 = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

# Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
PASSWORD_REGEX_3 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'

# Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
PASSWORD_REGEX_4 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%\^&*?])[A-Za-z\d!@#$%\^&*?]{8,}'

# Minimum eight and maximum 128 characters, at least one uppercase letter,
# one lowercase letter, one number and one special character:
PASSWORD_REGEX_5 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%\^&*?])[A-Za-z\d!@#$%\^&*?]{8,128}'

CREATE_OR_UPDATE_USER_ERROR = r'You do not have permission to create this user.'
