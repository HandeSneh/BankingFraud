import multiprocessing
import random
import time


# Sample transaction structure: (transaction_id, account_id, amount, location, timestamp)
def generate_transactions(num_transactions):
    """Generate a list of random transactions."""
    locations = ["NY", "CA", "TX", "FL", "NV"]
    return [
        {
            "transaction_id": i,
            "account_id": random.randint(1000, 2000),
            "amount": random.uniform(10, 5000),
            "location": random.choice(locations),
            "timestamp": time.time() + i,
        }
        for i in range(num_transactions)
    ]


def fraud_detection_rules(transaction):
    """Check for fraud based on simple rules."""
    rules = {
        "large_amount": transaction["amount"] > 4000,
        "rapid_transaction": transaction["timestamp"] % 10 == 0,  # Mock rapid check
        "unusual_location": transaction["location"] == "NV",  # Mock unusual location
    }
    # A transaction is fraudulent if any rule is triggered
    is_fraudulent = any(rules.values())
    return transaction["transaction_id"], is_fraudulent, rules


def process_transactions(transactions_chunk, results_queue):
    """Process a chunk of transactions and check for fraud."""
    results = []
    for transaction in transactions_chunk:
        transaction_id, is_fraudulent, rules = fraud_detection_rules(transaction)
        if is_fraudulent:
            results.append({"transaction_id": transaction_id, "rules_triggered": rules})
    results_queue.put(results)


def main():
    # Generate sample transactions
    num_transactions = 1000
    transactions = generate_transactions(num_transactions)

    # Divide transactions into chunks for multiprocessing
    num_processes = 4
    chunk_size = len(transactions) // num_processes
    chunks = [
        transactions[i : i + chunk_size]
        for i in range(0, len(transactions), chunk_size)
    ]

    # Create a multiprocessing queue to collect results
    results_queue = multiprocessing.Queue()

    # Create and start processes
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(
            target=process_transactions, args=(chunk, results_queue)
        )
        processes.append(process)
        process.start()

    # Collect results
    all_results = []
    for _ in range(num_processes):
        all_results.extend(results_queue.get())

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Print detected frauds
    print(f"Detected {len(all_results)} fraudulent transactions:")
    for result in all_results:
        print(result)


if __name__ == "__main__":
    main()
