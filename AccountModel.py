class AccountModel():
    def __init__(self):
        """
        Initializes a new account model.

        This model stores a list of accounts (public keys) and a dictionary of balances.
        Each account is identified by its unique public key, which is used to track
        its associated balance.
        """
        self.accounts = []  # List to store public keys of accounts
        self.balances = {}  # Dictionary to map public keys to their respective balances

    def addAccount(self, publicKeyString):
        """
        Adds a new account to the model if the public key is not already present.

        If the public key is new, it will be appended to the `accounts` list
        and initialized with a balance of 0 in the `balances` dictionary.

        :param publicKeyString: The public key of the account to be added
        """
        if not publicKeyString in self.accounts:  # Check if the account already exists
            self.accounts.append(publicKeyString)  # Add the public key to the accounts list
            self.balances[publicKeyString] = 0  # Initialize the account balance to 0

    def getBalance(self, publicKeyString):
        """
        Retrieves the balance of the account associated with the given public key.

        If the account does not exist, it will be automatically added with a balance of 0.
        This ensures that every valid public key has an entry in the `balances` dictionary.

        :param publicKeyString: The public key of the account
        :return: The balance of the account
        """
        if publicKeyString not in self.accounts:  # Check if the account exists
            self.addAccount(publicKeyString)  # Add the account if it does not exist
        return self.balances[publicKeyString]  # Return the balance of the account

    def updateBalance(self, publicKeyString, amount):
        """
        Updates the balance of the account associated with the given public key.

        The `amount` parameter can be positive (for credit) or negative (for debit).
        If the account does not exist, it will be automatically added with a balance of 0
        before applying the update.

        :param publicKeyString: The public key of the account
        :param amount: The amount to be added to (or subtracted from) the balance
        """
        if publicKeyString not in self.accounts:  # Check if the account exists
            self.addAccount(publicKeyString)  # Add the account if it does not exist
        self.balances[publicKeyString] += amount  # Update the account balance by the specified amount
