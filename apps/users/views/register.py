from django.shortcuts import redirect, render

from users.models import UserProfile


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        thumbnail = request.FILES['upload_image']
        color = request.POST['color_by_avatar']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
    else:
        return render(
            request=request,
            template_name='users/register.html',
        )

    errors = {}

    check_text_input(
        input_value=name,
        input_name='name',
        errors=errors,
    )

    check_text_input(
        input_value=last_name,
        input_name='last_name',
        errors=errors,
    )

    check_password(
        password=password,
        confirm_password=confirm_password,
        errors=errors,
    )

    check_if_user_exists_in_db(
        user_model=UserProfile,
        email=email,
        username=username,
        errors=errors,
    )

    user = UserProfile.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=name,
        last_name=last_name
    )
    user.thumbnail = thumbnail
    user.profile_color = color
    user.save()

    return redirect('login')

def check_text_input(input_value, input_name, errors):
    '''
        Função destinada a verificação de campos de entrada via 
        html do tipo texto
    '''
    if not input_value.strip():
        errors[input_name] = 'Nome inválido.'
        return redirect('register')

    if any(char.isdigit() for char in input_value):
        errors[input_name] = 'Campo inválido: Não inclua números.'
        return redirect('register')

def check_password(password, confirm_password, errors):
    '''
        Função destinada a verificação de password e confirmação
    '''

    if password != confirm_password:
        errors['confirm_password'] = 'As senhas não são iguais.'
        return redirect('register')

def check_if_user_exists_in_db(user_model, email, username, errors):
    '''
        Função para verificar se o usuário já existe no sistema.
        Não pode ter usuário e emails iguais no sistema.
        Para isso, nessa função é executado dois filtros.
    '''

    if user_model.objects.filter(email=email).exists():
        errors['email'] = 'Email já existente no sistema.'
        return redirect('register')

    if user_model.objects.filter(username=username).exists():
        errors['username'] = 'Usuário já existente no sistema.'
        return redirect('register')
