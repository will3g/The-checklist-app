from django.shortcuts import render

from tasks.models import Task

def search_task(request):
    tasks = Task.objects.order_by(
        '-created_at'
    )

    if 'find' in request.GET:
        get_params = request.GET['find']
        if search_task:
            tasks = tasks.filter(title__icontains=get_params)

    return render(
        request=request,
        template_name='tasks/search.html',
        context={
            'tasks': tasks,
            'search_params': get_params
        }
    )
