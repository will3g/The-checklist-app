from asyncio import tasks
from django.shortcuts import redirect, render

from users.models import UserProfile
from tasks.models import Task

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    tasks = Task.objects.order_by('-created_at').filter(author=request.user.id)

    return render(
        request=request,
        template_name='tasks/dashboard.html',
        context={'tasks': tasks}
    )
