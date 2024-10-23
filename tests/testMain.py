import unittest
from unit.testCard import TestCard
from unit.testDeck import TestDeck
from unit.testHand import TestHand


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCard))
    suite.addTest(unittest.makeSuite(TestDeck))
    suite.addTest(unittest.makeSuite(TestHand))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)