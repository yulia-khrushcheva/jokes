import unittest
from bot_func_abc import AtomicBotFunctionABC
from functions.atomic.example_bot_function import AtomicExampleBotFunction

class TestTeleBot(unittest.TestCase):
    
    def test_class_inherit(self):
        fobj = AtomicExampleBotFunction()
        self.assertIs(type(fobj).__base__, AtomicBotFunctionABC, msg="Function class must be inherited from AtomicBotFunctionABC !!!")
            

if __name__ == '__main__':
    unittest.main()