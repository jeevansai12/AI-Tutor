from django.core.management.base import BaseCommand
from core.models import Question


class Command(BaseCommand):
    """
    Django management command to load sample MCQ questions into the database.
    
    Usage:
        python manage.py load_questions
    
    What it does:
    1. Defines a list of MCQ questions across 5 subjects
    2. Tries to insert each question into the database
    3. Skips duplicates (checks by question text)
    4. Prints how many new questions were added
    
    Note: Questions are organized by subject (Python, DBMS, Networking, OS, DSA)
    Making them easy to find and update.
    """
    help = 'Load sample MCQ questions into the database'

    def handle(self, *args, **kwargs):
        """Main method that gets called when command is executed."""
        questions = [
            # Python
            {
                'subject': 'python',
                'text': 'What is the output of print(type(10))?',
                'option_a': "<class 'int'>",
                'option_b': "<class 'str'>",
                'option_c': "<class 'float'>",
                'option_d': "<class 'bool'>",
                'correct_option': 'A',
            },
            {
                'subject': 'python',
                'text': 'Which keyword is used to define a function in Python?',
                'option_a': 'func',
                'option_b': 'define',
                'option_c': 'def',
                'option_d': 'function',
                'correct_option': 'C',
            },
            {
                'subject': 'python',
                'text': 'What does len() function do?',
                'option_a': 'Returns the type',
                'option_b': 'Returns the length',
                'option_c': 'Returns the value',
                'option_d': 'Returns the index',
                'correct_option': 'B',
            },
            {
                'subject': 'python',
                'text': 'Which data type is immutable in Python?',
                'option_a': 'List',
                'option_b': 'Dictionary',
                'option_c': 'Set',
                'option_d': 'Tuple',
                'correct_option': 'D',
            },
            {
                'subject': 'python',
                'text': 'How do you start a comment in Python?',
                'option_a': '//',
                'option_b': '#',
                'option_c': '/*',
                'option_d': '--',
                'correct_option': 'B',
            },
            # DBMS
            {
                'subject': 'dbms',
                'text': 'What does SQL stand for?',
                'option_a': 'Structured Query Language',
                'option_b': 'Simple Query Language',
                'option_c': 'Standard Query Logic',
                'option_d': 'Sequential Query Language',
                'correct_option': 'A',
            },
            {
                'subject': 'dbms',
                'text': 'Which command is used to retrieve data from a database?',
                'option_a': 'GET',
                'option_b': 'FETCH',
                'option_c': 'SELECT',
                'option_d': 'RETRIEVE',
                'correct_option': 'C',
            },
            {
                'subject': 'dbms',
                'text': 'What is a primary key?',
                'option_a': 'A key that allows duplicates',
                'option_b': 'A unique identifier for each record',
                'option_c': 'A foreign reference',
                'option_d': 'An index key',
                'correct_option': 'B',
            },
            {
                'subject': 'dbms',
                'text': 'Which normal form removes partial dependency?',
                'option_a': '1NF',
                'option_b': '2NF',
                'option_c': '3NF',
                'option_d': 'BCNF',
                'correct_option': 'B',
            },
            {
                'subject': 'dbms',
                'text': 'DROP TABLE removes which of the following?',
                'option_a': 'Only rows',
                'option_b': 'Only columns',
                'option_c': 'Entire table structure and data',
                'option_d': 'Only indexes',
                'correct_option': 'C',
            },
            # Networking
            {
                'subject': 'networking',
                'text': 'What does HTTP stand for?',
                'option_a': 'HyperText Transfer Protocol',
                'option_b': 'High Transfer Text Protocol',
                'option_c': 'HyperText Transmission Process',
                'option_d': 'Home Tool Transfer Protocol',
                'correct_option': 'A',
            },
            {
                'subject': 'networking',
                'text': 'Which layer of OSI model is responsible for routing?',
                'option_a': 'Data Link',
                'option_b': 'Transport',
                'option_c': 'Network',
                'option_d': 'Session',
                'correct_option': 'C',
            },
            {
                'subject': 'networking',
                'text': 'What is the default port for HTTPS?',
                'option_a': '80',
                'option_b': '443',
                'option_c': '8080',
                'option_d': '22',
                'correct_option': 'B',
            },
            {
                'subject': 'networking',
                'text': 'IP address belongs to which layer?',
                'option_a': 'Application',
                'option_b': 'Transport',
                'option_c': 'Network',
                'option_d': 'Physical',
                'correct_option': 'C',
            },
            {
                'subject': 'networking',
                'text': 'What does DNS stand for?',
                'option_a': 'Data Name System',
                'option_b': 'Domain Name System',
                'option_c': 'Digital Network Service',
                'option_d': 'Domain Number System',
                'correct_option': 'B',
            },
            # Operating Systems
            {
                'subject': 'os',
                'text': 'What is the main function of an operating system?',
                'option_a': 'Compile code',
                'option_b': 'Manage hardware and software resources',
                'option_c': 'Browse the internet',
                'option_d': 'Create documents',
                'correct_option': 'B',
            },
            {
                'subject': 'os',
                'text': 'Which scheduling algorithm can cause starvation?',
                'option_a': 'FCFS',
                'option_b': 'Round Robin',
                'option_c': 'SJF',
                'option_d': 'All of the above',
                'correct_option': 'C',
            },
            {
                'subject': 'os',
                'text': 'What is a deadlock?',
                'option_a': 'When CPU is idle',
                'option_b': 'When processes wait forever for resources held by each other',
                'option_c': 'When memory is full',
                'option_d': 'When disk fails',
                'correct_option': 'B',
            },
            {
                'subject': 'os',
                'text': 'Which is NOT a type of operating system?',
                'option_a': 'Batch OS',
                'option_b': 'Real-time OS',
                'option_c': 'Compiler OS',
                'option_d': 'Distributed OS',
                'correct_option': 'C',
            },
            {
                'subject': 'os',
                'text': 'Virtual memory uses which storage?',
                'option_a': 'RAM only',
                'option_b': 'Hard disk as extension of RAM',
                'option_c': 'Cache memory',
                'option_d': 'ROM',
                'correct_option': 'B',
            },
            # Data Structures
            {
                'subject': 'dsa',
                'text': 'Which data structure uses LIFO?',
                'option_a': 'Queue',
                'option_b': 'Stack',
                'option_c': 'Array',
                'option_d': 'Linked List',
                'correct_option': 'B',
            },
            {
                'subject': 'dsa',
                'text': 'What is the time complexity of binary search?',
                'option_a': 'O(n)',
                'option_b': 'O(n²)',
                'option_c': 'O(log n)',
                'option_d': 'O(1)',
                'correct_option': 'C',
            },
            {
                'subject': 'dsa',
                'text': 'Which data structure uses FIFO?',
                'option_a': 'Stack',
                'option_b': 'Queue',
                'option_c': 'Tree',
                'option_d': 'Graph',
                'correct_option': 'B',
            },
            {
                'subject': 'dsa',
                'text': 'A binary tree has at most how many children per node?',
                'option_a': '1',
                'option_b': '2',
                'option_c': '3',
                'option_d': 'Unlimited',
                'correct_option': 'B',
            },
            {
                'subject': 'dsa',
                'text': 'Which sorting algorithm has worst-case O(n²)?',
                'option_a': 'Merge Sort',
                'option_b': 'Heap Sort',
                'option_c': 'Bubble Sort',
                'option_d': 'Counting Sort',
                'correct_option': 'C',
            },
        ]

        # Insert all questions into database
        # get_or_create ensures we don't add duplicates
        count = 0
        for q_data in questions:
            _, created = Question.objects.get_or_create(
                text=q_data['text'],  # Use question text as unique identifier
                defaults=q_data,       # These are the default values if question doesn't exist
            )
            if created:
                count += 1

        # Print success message
        self.stdout.write(self.style.SUCCESS(
            f'Loaded {count} new questions ({Question.objects.count()} total).'
        ))
