from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice
from django.utils import timezone


def index(request):
    if request.method == 'POST':
        # Assuming the form is submitted via POST method
        # You can modify this according to your actual implementation
        question_text = request.POST.get('question_text')  # Assuming you have an input field with name 'question_text'
        # Create a new Question object and save it to the database
        question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
        # Create a new Choice object related to the newly created question (you can adjust this according to your logic)
        choice = Choice.objects.create(question=question, choice_text="Default Choice", votes=0)
        question.save()
        choice.save()
        # Optionally, you can redirect to another page after adding the entry
        return HttpResponse("Entry added successfully!")
    else:
        return render(request, 'my_template.html')