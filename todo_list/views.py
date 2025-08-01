from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    return render(
        request,
        'todo/todo_home_page.html',
        {'tasks': tasks}
    )

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
    return redirect('task_list')

def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

