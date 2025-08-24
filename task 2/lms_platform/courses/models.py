from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class UserProgress(models.Model):
    user_id = models.IntegerField()
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Progress of user {self.user_id} in {self.course.title}"
