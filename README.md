# Part 2: Queries with GraphQL

**Summary of Part 1**
In the previous part, we created a simple Django project with a books application, set up a model with title and author fields, configured a GraphQL schema to query book data, and populated the database with sample data. We then tested the GraphQL endpoint to make sure it was working correctly.

[Creating a Simple Django Project with GraphQL](https://github.com/nimodb/SimpleDjangoProjectWithGraphQL.git)

## Step 1: Clone the repository
```bash
git clone https://github.com/nimodb/QueriesWithGraphQL_Part2
cd QueriesWithGraphQL_Part2
```

## Step 2: Set Up Virtual Environment and Install Packages
First, create a virtual environment and install the necessary packages.
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows
env\Scripts\activate

# On macOS/Linux
source env/bin/activate

# Install the required packages:
pip install -r requirements.txt
```

## Step 3: Create New Django App
Start the second part by creating a new app called `quiz`:
```bash
python manage.py startapp quiz
```

## Step 4: Set Up Models and Database
Set up models for the `quiz` app:
```bash
# models.py (quiz app)

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
    type = models.CharField(max_length=100, default=0, choices=TYPE)
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
```

Add the `quiz` app to `INSTALLED_APPS` in `settings.py`.
```python
# settings.py (core project)

INSTALLED_APPS = [
    ...
    'quiz',
]
```

**Database Migration**

Run the migrations to set up the database.
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Set Up GraphQL Schema
Create a combined GraphQL `schema.py` in the `core` project and set up the GraphQL schemas for the `books` and `quiz` apps:
```python
# schema.py (core project)

import graphene
from graphene_django import DjangoObjectType
from books.models import Books
from quiz.models import Category, Quizzes, Questions, Answer

class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "author")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "date_created")

class QuestionsType(DjangoObjectType):
    class Meta:
        model = Questions
        fields = ("id", "quiz", "type", "title", "difficulty", "date_created", "is_active")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("id", "question", "answer_text", "is_right")

class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)
    all_categories = graphene.List(CategoryType)
    all_quizzes = graphene.List(QuizzesType)
    all_questions = graphene.List(QuestionsType)
    all_answers = graphene.List(AnswerType)

    def resolve_all_books(root, info):
        return Books.objects.all()

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.all()

    def resolve_all_questions(root, info):
        return Questions.objects.all()

    def resolve_all_answers(root, info):
        return Answer.objects.all()

schema = graphene.Schema(query=Query)
```

## Step 6: Set Up URLs
Set up URLs to link the combined schema:
```python
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("books.urls")),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
]
```

## Step 7: Add Sample Data
Create a JSON file with sample quiz data and load it into the database.
```json
// quiz_data.json

[
    {"model": "quiz.category", "pk": 1, "fields": {"name": "Science"}},
    {"model": "quiz.category", "pk": 2, "fields": {"name": "History"}},
    {"model": "quiz.quizzes", "pk": 1, "fields": {"title": "General Science", "category": 1, "date_created": "2024-07-04T00:00:00Z"}},
    {"model": "quiz.quizzes", "pk": 2, "fields": {"title": "World History", "category": 2, "date_created": "2024-07-04T00:00:00Z"}},
    {"model": "quiz.questions", "pk": 1, "fields": {"quiz": 1, "type": 0, "title": "What is the chemical symbol for water?", "difficulty": 0, "date_created": "2024-07-04T00:00:00Z", "is_active": true}},
    {"model": "quiz.questions", "pk": 2, "fields": {"quiz": 2, "type": 0, "title": "Who was the first President of the United States?", "difficulty": 1, "date_created": "2024-07-04T00:00:00Z", "is_active": true}},
    {"model": "quiz.answer", "pk": 1, "fields": {"question": 1, "answer_text": "H2O", "is_right": true}},
    {"model": "quiz.answer", "pk": 2, "fields": {"question": 1, "answer_text": "O2", "is_right": false}},
    {"model": "quiz.answer", "pk": 3, "fields": {"question": 2, "answer_text": "George Washington", "is_right": true}},
    {"model": "quiz.answer", "pk": 4, "fields": {"question": 2, "answer_text": "Thomas Jefferson", "is_right": false}}
]
```

Load the data into the database.
```bash
python manage.py loaddata quiz_data.json
```