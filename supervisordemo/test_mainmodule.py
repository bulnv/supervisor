import supervisor
import unittest 
import time


class TestStringMethods(unittest.TestCase):
    args = {
        'logs_toggle': True,
        'debug': True,
        'cooldown': 1,
        'number_attempts': 1,
        'process': 'sleep 1',
        'inetrval_check': 3,
    }

    def test_oserror(self):
        # sv = supervisor.supervisor(self.args)
        # sv.start_subprocess()
        # while sv.prograssbar < 100:
        #     time.sleep(10)
        #     print('still running')
        # self.assertEqual(sv.result['success'], 3)
        pass
        
if __name__ == '__main__':
    unittest.main()