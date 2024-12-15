import unittest
from unit.testBot import TestBot
from unit.testCard import TestCard
from unit.testDealer import TestDealer
from unit.testDeck import TestDeck
from unit.testHand import TestHand
from unit.testPlayer import TestPlayer


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBot))
    suite.addTest(unittest.makeSuite(TestCard))
    suite.addTest(unittest.makeSuite(TestDealer))
    suite.addTest(unittest.makeSuite(TestDeck))
    suite.addTest(unittest.makeSuite(TestHand))
    suite.addTest(unittest.makeSuite(TestPlayer))
    
    runner = unittest.TextTestRunner(verbosity=10)
    runner.run(suite)