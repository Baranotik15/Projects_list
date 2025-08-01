from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)


def task_list(request):
    tasks = Task.objects.order_by("-created_at")
    return render(request, "todo/todo_home_page.html", {"tasks": tasks})


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(title=title)
    return redirect("task_list")


def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect("task_list")


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("task_list")


@csrf_exempt
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")

            if "due_date" in data:
                if data["due_date"] and data["due_date"] != "":
                    from django.utils.dateparse import parse_datetime

                    parsed_date = parse_datetime(data["due_date"])
                    if parsed_date:
                        task.due_date = parsed_date
                        logger.info(f"Updated due_date to: {parsed_date}")
                    else:
                        logger.error(f"Could not parse date: {data['due_date']}")
                else:
                    task.due_date = None
                    logger.info("Cleared due_date")

            if "categories" in data:
                task.categories.clear()
                for category_name in data["categories"]:
                    if category_name.strip():
                        category, created = Category.objects.get_or_create(
                            name=category_name.strip()
                        )
                        task.categories.add(category)
                        logger.info(f"Added category: {category.name}")

            task.save()
            logger.info(f"Task {task.id} saved successfully")
            return JsonResponse({"status": "success"})

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return render(request, "todo/task_detail.html", {"task": task})
