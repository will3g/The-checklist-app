from django.shortcuts import redirect, render, get_object_or_404

from users.models import UserProfile
from tasks.models import Task

def my_task(request, task_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        pass

    task = get_object_or_404(
        klass=Task,
        pk=task_id
    )

    return render(
        request=request,
        template_name='tasks/task.html',
        context={
            'task': task,
            'task_id': task_id,
        }
    )

def new_task(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        thumbnail = request.FILES['upload-image']
        primary_color = request.POST['primary-color']
        secondary_color = request.POST['secondary-color']
        subtasks = request.POST.getlist('subtasks')

        errors = {}

        check_if_subtasks_is_valid_to_create_or_edit_task(
            list=subtasks,
            input_name='title',
            errors=errors,
        )

        subtasks = {
            'list_of_subtasks': subtasks
        }

        check_text_input(
            input_value=title,
            input_name='title',
            errors=errors,
        )

        # get user by form frontend to link with task
        user = get_object_or_404(UserProfile, pk=request.user.id)

        task = Task.objects.create(
            author=user,
            title=title,
            description=description,
            thumbnail=thumbnail,
            primary_color=primary_color,
            secondary_color=secondary_color,
            subtasks=subtasks
        )
        task.save()

        return redirect('dashboard')

    return render(
        request=request,
        template_name='tasks/new_task.html',
    )

def edit_task(request):
    if not request.user.is_authenticated:
        return redirect('login')

    task_id = request.__dict__.get('environ').get('HTTP_REFERER').split('/')[-1]

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        thumbnail = request.FILES.get('upload-image', '') # for new thumbnail
        if not thumbnail:

            task = get_object_or_404(
                klass=Task,
                pk=task_id
            )

            thumbnail = task.thumbnail

        # TODO: (Live-Reload) Create function/button (html) to update primary color for task
        primary_color = request.POST['primary-color']
        secondary_color = request.POST['secondary-color']
        subtasks = request.POST.getlist('subtasks')

        errors = {}

        check_if_subtasks_is_valid_to_create_or_edit_task(
            list=subtasks,
            input_name='title',
            errors=errors,
        )

        subtasks = {
            'list_of_subtasks': subtasks
        }

        check_text_input(
            input_value=title,
            input_name='title',
            errors=errors,
        )

        check_text_input(
            input_value=description,
            input_name='description',
            errors=errors,
        )

        task = get_object_or_404(Task, pk=task_id)
        task.title = title
        task.description = description
        task.thumbnail = thumbnail
        task.primary_color = primary_color
        task.secondary_color = secondary_color
        task.subtasks = subtasks
        task.save()

        return redirect('dashboard')

    return redirect('dashboard')

def check_if_subtasks_is_valid_to_create_or_edit_task(list, input_name, errors):
    if len(list) < 2:
        errors[input_name] = 'Para criar uma nova tarefa é necessário criar subtarefas.'
        return redirect('new_task')

    for subtask in list:
        check_text_input(
            input_value=subtask,
            input_name='subtasks',
            errors=errors,
        )

def check_text_input(input_value, input_name, errors):
    '''
        Função destinada a verificação de campos de entrada via 
        html do tipo texto
    '''
    if not input_value.strip():
        errors[input_name] = 'Campo inválido.'
        return redirect('new_task')