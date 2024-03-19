from ds_protocol import *
import unittest

class TestProtocol(unittest.TestCase):
    def test_direct_message(self):
        dump = direct_message("token","my message","cooliotimmy","19:20:33")
        self.assertEqual(dump,"""{"token": "token", "directmessage": {"entry": "my message", "recipient": "cooliotimmy", "timestamp": "19:20:33"}}""")

    def test_msgs_response(self):
        dump1 = msgs_response("token", "new")
        self.assertEqual(dump1, """{"token": "token", "directmessage": "new"}""")
        dump2 = msgs_response("token", "all")
        self.assertEqual(dump2, """{"token": "token", "directmessage": "all"}""")



if __name__ == "__main__" :
    unittest.main()