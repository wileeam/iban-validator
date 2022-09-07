import pycountry
import string


class IbanValidationError(ValueError):
    pass


class IbanInvalidCharactersError(IbanValidationError):
    def __init__(self, account, *args):
        super().__init__(args)
        self.account = account

    def __str__(self):
        return f"The IBAN account provided ({self.account}) contains non-alphanumeric characters."


class IbanTooLongError(IbanValidationError):
    def __init__(self, account, *args):
        super().__init__(args)
        self.account = account

    def __str__(self):
        return f"The IBAN account provided ({self.account}) has {len(self.account)} characters and the maximum allowed is 34."


class Iban:
    """
    Stores an IBAN number and provides some checking and validation functionality
    """

    def __init__(self, account: str):
        # IBAN number can only be digits and characters...
        if not account.isalnum():
            raise IbanInvalidCharactersError(account)

        # IBAN number can not be more than 34 alphanumeric characters
        if len(account) > 34:
            raise IbanTooLongError(account)

        self.iban = account.upper()

    def __str__(self):
        return self.iban[:4] + " " + self.iban[4:]

    def validate(self):
        """
        Validates an IBAN number
        See https://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN

        :return: bool whether IBAN number passes the mod-97 check or not
        """

        # Move the four initial characters to the end of the string
        iban_rearranged = self.__rearrange(self.iban)

        # Replace each letter in the string with two digits, thereby expanding the string, where A = 10, B = 11, ..., Z = 35
        iban_numerised = self.__numerise(iban_rearranged)

        # Interpret the string as a decimal integer and compute the remainder of that number on division by 97
        # If the remainder is 1, the check digit test is passed and the IBAN might be valid.
        return (int(iban_numerised) % 97) == 1

    def generate_check_digits(self):
        """
        Generates the two check digits of an IBAN numebr
        See https://en.wikipedia.org/wiki/International_Bank_Account_Number#Generating_IBAN_check_digits

        :return: str IBAN number's check digits
        """

        # Replace the two check digits by 00 (e.g., GB00 for the UK)
        iban_check_digits_replaced = self.iban[:2] + "00" + self.iban[4:]

        # And move the four initial characters to the end of the string
        iban_rearranged = self.__rearrange(iban_check_digits_replaced)

        # Replace each letter in the string with two digits, thereby expanding the string, where A = 10, B = 11, ..., Z = 35
        iban_numerised = self.__numerise(iban_rearranged)

        # Interpret the string as a decimal integer and compute the remainder of that number on division by 97
        # Subtract the remainder from 98 and use the result for the two check digits.
        # If the result is a single-digit number, pad it with a leading 0 to make a two-digit number.
        return "{:0>2}".format(98 - (int(iban_numerised) % 97))

    def is_correct(self):
        """
        Checks that an IBAN number is actually correct
        That is, generated check digits match the IBAN number and it validates as well

        :return: bool IBAN number passes mod-97 and check digits tests or not
        """
        return (
            self.generate_check_digits() == self.iban[2:4] and self.validate()
        )

    def belongs_to_country(self):
        """
        Checks that the IBAN number has a valid country code
        That is, the length of the country code is two and the country exists

        :return: bool IBAN number belongs to an existing country or not
        """

        # Doing an extra check on the check digits as well
        return (
            self.iban[2:4].isdecimal()
            and self.iban[:2].isalpha()
            and self.__country_exists(self.iban[:2])
        )

    def __rearrange(self, line, size=4):
        """
        Shifts the first characters of a string to the end
        """

        return line[size:] + line[:size]

    def __numerise(self, line):
        """
        Converts uppercase characters of a string into decimal numbers (A = 10, B = 11,...,Z = 35)
        """
        CHARACTERS = {
            ord(d): str(i)
            for i, d in enumerate(string.digits + string.ascii_uppercase)
        }

        return line.translate(CHARACTERS)

    def __country_exists(self, country):
        """
        Check for an existing country
        """
        try:
            country = pycountry.countries.lookup(country)
        except:
            country = None

        return bool(country)
