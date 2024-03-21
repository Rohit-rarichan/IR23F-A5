import unittest
from ds_messenger import DirectMessenger

class TestDirectMessenger(unittest.TestCase):
    def setUp(self):
        self.dsuserver = "localhost"
        self.port = 3021
        self.direct_messenger = DirectMessenger(self.dsuserver, "test_user", "test_password")

    def test_send_success(self):
        # Simulate a successful send response from the server
        self.direct_messenger.client = MockClient(response=b'{"response": {"type": "ok"}}')
        message = "Hello"
        recipient = "recipient_user"
        
        result = self.direct_messenger.send(message, recipient)
        
        self.assertTrue(result)

    def test_send_failure(self):
        # Simulate a failure response from the server
        self.direct_messenger.client = MockClient(response=b'{"response": {"type": "error"}}')
        message = "Hello"
        recipient = "recipient_user"
        
        result = self.direct_messenger.send(message, recipient)
        
        self.assertFalse(result)

    def test_retrieve_new(self):
        # Simulate a response containing new messages from the server
        self.direct_messenger.client = MockClient(response=b'{"message": "test_message", "sender": "test_sender", "timestamp": "test_timestamp"}')
        expected_result = [{"recipient": "test_user", "message": "test_message", "timestamp": "test_timestamp"}]
        
        result = self.direct_messenger.retrieve_new()
        
        self.assertEqual(result, expected_result)

    def test_retrieve_all(self):
        # Simulate a response containing all messages from the server
        self.direct_messenger.client = MockClient(response=b'{"message": "test_message", "sender": "test_sender", "timestamp": "test_timestamp"}')
        expected_result = [{"recipient": "test_user", "message": "test_message", "timestamp": "test_timestamp"}]
        
        result = self.direct_messenger.retrieve_all()
        
        self.assertEqual(result, expected_result)

class MockClient:
    def __init__(self, response=b''):
        self.response = response

    def send(self, data):
        pass

    def recv(self, bufsize):
        return self.response

if __name__ == "__main__":
    unittest.main()