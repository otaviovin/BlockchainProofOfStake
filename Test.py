from ProofOfStake import ProofOfStake
from Lot import Lot
import string
import random

def getRandomString(length):
    """
    Generates a random string of lowercase letters of a specified length.

    :param length: The length of the random string to generate.
    :return: A random string of lowercase letters of the given length.
    """
    letters = string.ascii_lowercase  # Set of lowercase letters
    resultString = ''.join(random.choice(letters) for i in range(length))  # Generate a random string
    return resultString  # Return the generated random string

if __name__ == '__main__':
    pos = ProofOfStake()  # Instantiate the Proof of Stake system
    pos.update('bob', 100)  # Bob adds 100 units to his stake
    pos.update('alice', 100)  # Alice adds 100 units to her stake

    bobWins = 0  # Counter for Bob's wins
    aliceWins = 0  # Counter for Alice's wins

    for i in range(100):  # Simulate 100 iterations
        forger = pos.forger(getRandomString(i))  # Get the forger using a random string of length 'i'
        if forger == 'bob':
            bobWins += 1  # Increment Bob's win counter
        elif forger == 'alice':
            aliceWins += 1  # Increment Alice's win counter

    print('Bob won: ' + str(bobWins) + ' times')  # Display the total number of wins for Bob
    print('Alice won: ' + str(aliceWins) + ' times')  # Display the total number of wins for Alice
