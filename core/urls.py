from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.quiz_select_view, name='quiz_select'),
    path('quiz/<str:subject>/', views.quiz_take_view, name='quiz_take'),
    path('quiz/result/<int:result_id>/', views.quiz_result_view, name='quiz_result'),
    path('chat/', views.chat_view, name='chat'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('flashcards/', views.flashcard_select_view, name='flashcard_select'),
    path('flashcards/<str:subject>/', views.flashcards_view, name='flashcards'),
    path('notes/', views.generate_notes_view, name='generate_notes'),
]
