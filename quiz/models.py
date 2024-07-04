from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Quizzes(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name="quizzes", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Questions(models.Model):
    DIFFICULTY_LEVELS = [
        (0, "Fundamental"),
        (1, "Beginner"),
        (2, "Intermediate"),
        (3, "Advance"),
        (4, "Expert"),
    ]
    TYPE = [
        (0, "Multiple Choice"),
    ]

    quiz = models.ForeignKey(
        Quizzes, related_name="questions", on_delete=models.CASCADE
    )
    technique = models.CharField(max_length=100, default=0, choices=TYPE)
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=100, default=0, choices=DIFFICULTY_LEVELS)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Questions, related_name="answers", on_delete=models.CASCADE
    )
    answer_text = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
