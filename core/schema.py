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
        fields = (
            "id",
            "quiz",
            "type",
            "title",
            "difficulty",
            "date_created",
            "is_active",
        )


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
