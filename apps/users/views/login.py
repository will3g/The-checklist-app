from django.shortcuts import redirect, render
from django.contrib import auth

from users.models import UserProfile


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        check_empty_inputs(
            request=request,
            email=email,
            password=password,
        )

        check_if_user_exists(
            request=request,
            user_model=UserProfile,
            email=email,
        )

        user_instance = get_user(
            user_model=UserProfile,
            email=email,
        )

        user_authenticated = auth.authenticate(
            request=request,
            username=user_instance,
            password=password
        )

        if user_authenticated is not None:
            auth.login(
                request=request,
                user=user_authenticated
            )
            return redirect('dashboard')

        # messages.error(request, 'Senha ou usuário inválido.')

    return render(
        request=request,
        template_name='users/login.html'
    )

def check_empty_inputs(request, email, password):
    if email == '' or password == '':
        # messages.error(request, 'Email ou senha inválidos.')
        return redirect('login')

def check_if_user_exists(request, user_model, email):
    if not user_model.objects.filter(email=email).exists():
        # messages.error(request, 'Usuário não encontrado no sistema.')
        return redirect('login')

def get_user(user_model, email):
    """
        Faz o filtro no banco pelo email e nos traz o usuário do objeto.
        Para depois utilizar o autenticador default da lib do django
    """
    # TODO: Está bugando nessa parte quando tento entrar com admin
    return user_model.objects.filter(email=email).values_list('username', flat=True).get()