from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, FeedbackForm
from .models import Question, QuizResult, Flashcard
from .services.gemini_service import GeminiService


# ------------------ AUTH ------------------

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created!")
        return redirect('dashboard')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------ DASHBOARD ------------------

@login_required
def dashboard_view(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')[:5]
    return render(request, 'dashboard.html', {
        'results': results,
        'latest': results[0] if results else None
    })


# ------------------ QUIZ ------------------

@login_required
def quiz_select_view(request):
    return render(request, 'quiz_select.html', {
        'subjects': Question.SUBJECT_CHOICES
    })


@login_required
def quiz_take_view(request, subject):
    questions = Question.objects.filter(subject=subject)

    if not questions:
        messages.warning(request, "No questions available")
        return redirect('quiz_select')

    if request.method == 'POST':
        correct = sum(
            1 for q in questions
            if request.POST.get(f'q_{q.id}', '').upper() == q.correct_option
        )

        total = questions.count()
        score = int((correct / total) * 100)

        result = QuizResult.objects.create(
            user=request.user,
            subject=subject,
            score=score,
            total_questions=total,
            correct_answers=correct
        )

        return redirect('quiz_result', result.id)

    return render(request, 'quiz_take.html', {
        'questions': questions,
        'subject': subject
    })


@login_required
def quiz_result_view(request, result_id):
    result = QuizResult.objects.get(id=result_id, user=request.user)
    return render(request, 'quiz_result.html', {'result': result})




# ------------------ CHAT ------------------

@login_required
def chat_view(request):
    api_key = request.session.get('api_key')
    chat_history = request.session.setdefault('chat_history', [])

    if request.method == 'POST':
        # 1. Update/Save API Key
        if 'api_key' in request.POST:
            request.session['api_key'] = request.POST['api_key']
            return redirect('chat')

        # 2. Clear Chat History
        if 'clear_chat' in request.POST:
            request.session['chat_history'] = []
            return redirect('chat')

        # 3. Remove API Key
        if 'clear_key' in request.POST:
            request.session.pop('api_key', None)
            request.session.pop('chat_history', None)
            return redirect('chat')

        # 4. Handle User Message
        user_msg = request.POST.get('user_msg')
        if user_msg and api_key:
            try:
                ai = GeminiService(api_key)
                reply = ai.generate(f"Explain: {user_msg}")
                # Update history
                chat_history.append({'role': 'user', 'text': user_msg})
                chat_history.append({'role': 'ai', 'text': reply})
                request.session.modified = True
            except Exception as e:
                messages.error(request, f"AI Error: {str(e)}")

        return redirect('chat')

    return render(request, 'chat.html', {
        'chat_history': chat_history,
        'has_key': bool(api_key)
    })



# ------------------ NOTES ------------------

@login_required
def generate_notes_view(request):
    notes_content = None
    api_key = request.session.get('api_key')

    if request.method == 'POST':
        if not api_key:
            messages.warning(request, "Please enter your Gemini API key in the AI Tutor Chat first to use this feature.")
            return redirect('chat')
            
        topic = request.POST.get('topic')
        if topic:
            try:
                ai = GeminiService(api_key)
                notes_content = ai.generate(f"Generate concise study notes and 3 important questions for {topic}")
            except Exception as e:
                messages.error(request, f"AI Error: {str(e)}")

    return render(request, 'notes.html', {'notes_content': notes_content})



# ------------------ FEEDBACK ------------------

@login_required
def feedback_view(request):
    form = FeedbackForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.save()
        return redirect('dashboard')

    return render(request, 'feedback.html', {'form': form})


# ------------------ FLASHCARDS ------------------

@login_required
def flashcard_select_view(request):
    return render(request, 'flashcard_select.html', {
        'subjects': Question.SUBJECT_CHOICES
    })


@login_required
def flashcards_view(request, subject):
    cards = Flashcard.objects.filter(subject=subject)

    if not cards:
        return redirect('flashcard_select')

    return render(request, 'flashcards.html', {'cards': cards})