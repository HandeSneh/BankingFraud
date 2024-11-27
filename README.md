# Multiprocessing:

Multiprocessing allows you to run multiple processes concurrently on a multi-core system. This can significantly speed up tasks that can be broken down into smaller, independent subtasks.
Multiprocessing in Python is a built-in library that allows you to leverage multiple processes on a multi-core system to execute tasks concurrently. This can significantly improve the performance of your Python code, especially for tasks that can be broken down into smaller, independent subtasks.\
Key Concepts: \
1.Process: An instance of a program being executed. \
2.Multiprocessing: Running multiple processes simultaneously. \
3.Multiprocessing Module: A Python library that provides tools for managing multiple processes.\
4.Pool: A collection of worker processes that can execute tasks concurrently.\
5.Queue/Manager: Tools to share data between processes.\

# Problem Statement: Fraud Detection System for Real-Time Transactions

Scenario:
A bank monitors transactions in real time to detect fraudulent activities. Each transaction is checked against multiple fraud detection rules, such as:\
	•	Unusual location of the transaction.\
	•	Large transaction amount compared to account history.\
	•	Rapid consecutive transactions.

Task:\
Build a multiprocessing system to:\
	1.	Divide the incoming stream of transactions among multiple processes.\
	2.	Each process applies the fraud detection rules independently.\
	3.	Combine the flagged results from all processes into a centralized log for further review.

   # Key Features:
	1.Fraud Rules:
		Large transaction amount.
		Rapid transactions (mock condition based on timestamp).
		Transactions from an unusual location.
	2.Multiprocessing:
		The transactions are split into chunks, and each chunk is processed by a separate process.
		Results from each process are collected in a multiprocessing queue.
	3.Scalable Design:
		Number of processes can be adjusted based on the system’s CPU capacity.
		Transaction chunks ensure balanced workload distribution.



