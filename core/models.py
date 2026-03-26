from django.db import models
from django.contrib.auth.models import User

# ============= RULE-BASED PERFORMANCE CLASSIFICATION =============
# These are simple helper functions that classify user performance
# based on quiz scores using IF-ELSE logic (no ML needed!).
# This approach is simple, transparent, and easy to explain.

def get_performance_level(score):
    """
    Classify user performance level based on quiz score.
    
    Rules:
    - score < 40   --> Beginner (needs to review fundamentals)
    - 40 <= score <= 70  --> Intermediate (decent understanding)
    - score > 70   --> Advanced (strong grasp of topic)
    
    Args:
        score: Integer quiz score (0-100)
    
    Returns:
        String: 'Beginner', 'Intermediate', or 'Advanced'
    """
    if score < 40:
        return 'Beginner'
    elif score <= 70:
        return 'Intermediate'
    else:
        return 'Advanced'

def get_recommendation_logic(score, subject):
    """
    Generate learning recommendations based on performance level and subject.
    
    This function uses simple IF-ELSE logic to suggest topics students should
    focus on. Each subject has 3 recommended topics mapped to 3 levels.
    
    Args:
        score: Integer quiz score (0-100)
        subject: String, one of 'python', 'dbms', 'networking', 'os', 'dsa'
    
    Returns:
        String: Personalized recommendation message
    
    Example:
        score=25, subject='python' -> 'Focus on fundamentals: Python Syntax & Variables.'
        score=55, subject='python' -> 'Improve your knowledge on: Functions & Loops.'
        score=85, subject='python' -> 'Great job! Review advanced topics like: Data Structures (Lists, Dictionaries).'
    """
    level = get_performance_level(score)
    
    # Define 3 topic progression levels for each subject
    # These topics progress from basic → intermediate → advanced
    topics = {
        'python': [
            "Python Syntax & Variables",  # Level 0: Beginner
            "Functions & Loops",           # Level 1: Intermediate
            "Data Structures (Lists, Dictionaries)"  # Level 2: Advanced
        ],
        'dbms': [
            "Database Basics",
            "SQL Queries (JOINs)",
            "Normalization (1NF, 2NF, 3NF)"
        ],
        'networking': [
            "OSI & TCP/IP Models",
            "IP Addressing & Subnetting",
            "Routing Protocols"
        ],
        'os': [
            "OS Basics & Functions",
            "Process Scheduling",
            "Memory Management & Deadlocks"
        ],
        'dsa': [
            "Arrays & Strings",
            "Linked Lists",
            "Trees & Graphs"
        ],
    }
    
    # Get topics for this subject, or use default if subject not found
    subject_topics = topics.get(subject, ["Review core concepts", "Practice more questions", "Read documentation"])
    
    # Return recommendation based on performance level
    if level == 'Beginner':
        return f"Focus on fundamentals: {subject_topics[0]}."
    elif level == 'Intermediate':
        return f"Improve your knowledge on: {subject_topics[1]}."
    else:
        return f"Great job! Review advanced topics like: {subject_topics[2]}."



# ============= DATABASE MODELS =============
# Models define the structure of data stored in the database.
# Each model maps to a database table.


class Question(models.Model):
    """
    Stores MCQ quiz questions.
    
    Each question has:
    - subject: Which subject this question belongs to (Python, DBMS, etc.)
    - text: The question text
    - option_a, option_b, option_c, option_d: Four multiple choice options
    - correct_option: Which option (A, B, C, or D) is the correct answer
    
    Example:
        Question(
            subject='python',
            text='What is the output of print(type(10))?',
            option_a="<class 'int'>",
            option_b="<class 'str'>",
            option_c="<class 'float'>",
            option_d="<class 'bool'>",
            correct_option='A'
        )
    """
    SUBJECT_CHOICES = [
        ('python', 'Python'),
        ('dbms', 'DBMS'),
        ('networking', 'Networking'),
        ('os', 'Operating Systems'),
        ('dsa', 'Data Structures'),
    ]

    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return f"{self.subject} — {self.text[:50]}"


class QuizResult(models.Model):
    """
    Records each time a user completes a quiz.
    
    Stores:
    - user: Which student took this quiz (links to User table)
    - subject: Which subject was tested (Python, DBMS, etc.)
    - score: The percentage score (0-100)
    - total_questions: How many questions were in the quiz
    - correct_answers: How many the student answered correctly
    - date_taken: When the quiz was completed
    
    Rule-Based Properties (no ML):
    - level: Returns 'Beginner', 'Intermediate', or 'Advanced' based on score
    - recommendation: Returns a personalized learning suggestion
    
    Example flow:
    1. Student takes a 10-question quiz
    2. Gets 7 correct
    3. score = 70%, total_questions = 10, correct_answers = 7
    4. level property -> 'Intermediate' (because 40 <= 70 <= 70)
    5. recommendation property -> Personalized topic suggestion
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.subject} — {self.score}%"

    @property
    def level(self):
        """Rule-based performance classification."""
        return get_performance_level(self.score)

    @property
    def recommendation(self):
        """Rule-based topic recommendation."""
        return get_recommendation_logic(self.score, self.subject)

class Feedback(models.Model):
    """User feedback submissions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.subject}"

class Flashcard(models.Model):
    """User flashcards for practice."""
    subject = models.CharField(max_length=50, choices=Question.SUBJECT_CHOICES)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"{self.subject} Flashcard: {self.question[:30]}"
