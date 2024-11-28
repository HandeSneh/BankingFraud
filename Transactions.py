import multiprocessing
import random
import time
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create a file handler and set the level with 'w' for write mode
file_handler = logging.FileHandler('my_app.log', mode='w')  
file_handler.setLevel(logging.INFO)
# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(file_handler)


def generate_transactions(num_transactions):
    """
    Generate a list of random transactions.

    Args:
        num_transactions (int): Number of transactions to generate.

    Returns:
        list: A list of transaction dictionaries.
    """
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
    """
    Apply fraud detection rules to a transaction.

    Args:
        transaction (dict): A transaction dictionary.

    Returns:
        tuple: A tuple containing transaction ID, a flag indicating fraud, 
               and the rules triggered.
    """
    try:
        rules = {
            "large_amount": transaction["amount"] > 4000,
            "rapid_transaction": transaction["timestamp"] % 10 == 0,  # Mock condition
            "unusual_location": transaction["location"] == "NV",  # Mock unusual location
        }
        is_fraudulent = any(rules.values())
        return transaction["transaction_id"], is_fraudulent, rules
    except KeyError as e:
        logger.info(f"Transaction is missing a key: {e}")
        raise
    except Exception as e:
        logger.info(f"Unexpected error in fraud_detection_rules: {e}")
        raise


def process_transactions(transactions_chunk, results_queue):
    """
    Process a chunk of transactions and check for fraud.

    Args:
        transactions_chunk (list): A list of transactions to process.
        results_queue (multiprocessing.Queue): Queue to store the results.
    """
    try:
        results = []
        for transaction in transactions_chunk:
            transaction_id, is_fraudulent, rules = fraud_detection_rules(transaction)
            if is_fraudulent:
                results.append({"transaction_id": transaction_id, "rules_triggered": rules})
        results_queue.put(results)
    except Exception as e:
        logger.info(f"Error in processing transactions: {e}")
        results_queue.put([])


def divide_transactions(transactions, num_processes):
    """
    Divide transactions into chunks for multiprocessing.

    Args:
        transactions (list): List of transactions.
        num_processes (int): Number of processes.

    Returns:
        list: List of transaction chunks.
    """
    chunk_size = len(transactions) // num_processes
    return [transactions[i:i + chunk_size] for i in range(0, len(transactions), chunk_size)]


def collect_results(results_queue, num_processes):
    """
    Collect results from the multiprocessing queue.

    Args:
        results_queue (multiprocessing.Queue): Queue containing the results.
        num_processes (int): Number of processes.

    Returns:
        list: Combined list of results from all processes.
    """
    all_results = []
    try:
        for _ in range(num_processes):
            all_results.extend(results_queue.get())
    except Exception as e:
        logger.info(f"Error while collecting results: {e}")
    return all_results


def main():
    """
    Main function to perform fraud detection using multiprocessing.

    Steps:
    1. Generate sample transactions.
    2. Divide transactions into chunks for parallel processing.
    3. Process chunks in parallel and collect results.
    4. Log the fraudulent transactions detected.
    """
    try:
        num_transactions = 1000
        num_processes = 4

        # Step 1: Generate transactions
        transactions = generate_transactions(num_transactions)
        logger.info(f"Generated {num_transactions} transactions.")

        # Step 2: Divide transactions into chunks
        chunks = divide_transactions(transactions, num_processes)

        # Step 3: Initialize multiprocessing
        results_queue = multiprocessing.Queue()
        processes = []
        for chunk in chunks:
            process = multiprocessing.Process(
                target=process_transactions, args=(chunk, results_queue)
            )
            processes.append(process)
            process.start()

        # Step 4: Collect results
        all_results = collect_results(results_queue, len(processes))

        # Wait for all processes to complete
        for process in processes:
            process.join()

        # Step 5: Log fraudulent transactions
        logger.info(f"Detected {len(all_results)} fraudulent transactions:")
        for result in all_results:
            logger.info(result)

    except Exception as e:
        logger.info(f"Unexpected error in main: {e}")


if __name__ == "__main__":
    main()
