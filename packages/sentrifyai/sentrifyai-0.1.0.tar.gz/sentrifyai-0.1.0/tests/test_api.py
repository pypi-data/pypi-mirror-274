import unittest
from sentrifyai import SentrifyAI, SentrifyAIError, ModelNotFoundError

class TestSentrifyAI(unittest.TestCase):
    def setUp(self):
        self.client = SentrifyAI(api_key='test_api_key')

    def test_list_models(self):
        models = self.client.list_models()
        self.assertIsInstance(models, list)

    def test_classify_message(self):
        result = self.client.classify_message(model_slug='test_model', message='Hello world')
        self.assertIn('classification', result)
        self.assertIn('confidence', result)

if __name__ == '__main__':
    unittest.main()
