from django.contrib import admin
from .models import Question, QuizResult, Feedback, Flashcard


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text', 'correct_option')
    list_filter = ('subject',)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'score', 'date_taken')
    list_filter = ('subject', 'user')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subject', 'message', 'user__username')


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question')
    list_filter = ('subject',)
    search_fields = ('question', 'answer')
