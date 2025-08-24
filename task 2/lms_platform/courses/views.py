from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Course, Lesson, Quiz, UserProgress

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    quizzes = course.quizzes.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes
    })

def upload_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course = Course.objects.create(title=title, description=description)
        return redirect('course_detail', course_id=course.id)
    return render(request, 'courses/upload_course.html')

def track_progress(request, course_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        course = get_object_or_404(Course, id=course_id)
        progress, created = UserProgress.objects.get_or_create(
            user_id=user_id,
            course=course
        )
        progress.completed = True
        progress.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def take_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizzes = course.quizzes.all()
    
    if request.method == 'POST':
        score = 0
        total = quizzes.count()
        for quiz in quizzes:
            user_answer = request.POST.get(f'quiz_{quiz.id}')
            if user_answer == quiz.answer:
                score += 1
        return render(request, 'courses/quiz_result.html', {
            'score': score,
            'total': total,
            'course': course
        })
    
    return render(request, 'courses/take_quiz.html', {
        'course': course,
        'quizzes': quizzes
    })
