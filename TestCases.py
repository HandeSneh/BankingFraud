import unittest
import Transactions
import random
import time
import multiprocessing

class TestTransactionFunctions(unittest.TestCase):

    def test_generate_transactions(self):
        num_transactions = 10
        transactions = Transactions.generate_transactions(num_transactions)
        self.assertEqual(len(transactions), num_transactions)
        for transaction in transactions:
            self.assertIn("transaction_id", transaction)
            self.assertIn("account_id", transaction)
            self.assertIn("amount", transaction)
            self.assertIn("location", transaction)
            self.assertIn("timestamp", transaction)

    def test_fraud_detection_rules_large_amount(self):
        transaction = {"transaction_id": 1, "account_id": 1001, "amount": 5000, "location": "NY", "timestamp": time.time()}
        transaction_id, is_fraudulent, rules = Transactions.fraud_detection_rules(transaction)
        self.assertTrue(is_fraudulent)
        self.assertTrue(rules["large_amount"])


    def test_fraud_detection_rules_rapid_transaction(self):
        transaction = {"transaction_id": 1, "account_id": 1001, "amount": 100, "location": "NY", "timestamp": 1678886400} # A timestamp divisible by 10
        transaction_id, is_fraudulent, rules = Transactions.fraud_detection_rules(transaction)
        self.assertTrue(is_fraudulent)
        self.assertTrue(rules["rapid_transaction"])


    def test_fraud_detection_rules_unusual_location(self):
        transaction = {"transaction_id": 1, "account_id": 1001, "amount": 100, "location": "NV", "timestamp": time.time()}
        transaction_id, is_fraudulent, rules = Transactions.fraud_detection_rules(transaction)
        self.assertTrue(is_fraudulent)
        self.assertTrue(rules["unusual_location"])

    def test_fraud_detection_rules_no_fraud(self):
        transaction = {"transaction_id": 1, "account_id": 1001, "amount": 100, "location": "NY", "timestamp": time.time() + 5}
        transaction_id, is_fraudulent, rules = Transactions.fraud_detection_rules(transaction)
        self.assertFalse(is_fraudulent)


    def test_process_transactions(self):
      transactions = Transactions.generate_transactions(5)
      results_queue = multiprocessing.Queue()
      Transactions.process_transactions(transactions, results_queue)
      results = results_queue.get()
      self.assertIsInstance(results, list)


    # Add more test cases for other functions as needed.


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)