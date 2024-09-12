from django.shortcuts import render
from Site.models import *

# Create your views here.

def index_view(request):
    games = Game.object.all()
    return render(request, 'index.html',
                  {'games': games})

def GameDetailView(DetailView):
    model = Game
    template_name = game.html
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()  # Получаем объект Game
        meme_gallery = MemeGallery.objects.filter(meme=meme.id)
        context['page_name'] = game.name
        return context


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Какое то из полей заполнено неверно!')
            messages.error(request, form.errors)
            return HttpResponseRedirect('/login', locals())

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.info(request, 'Неверные логин или пароль!')
            return HttpResponseRedirect('/login', locals())

        login(request, user)

        return HttpResponseRedirect(f'/user/{request.user.username}', locals())
    else:
        form = LoginForm()
        return render(request, 'login.html', {'login_form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print(form.errors)
        if not form.is_valid():
            messages.error(request, 'Какое то из полей заполнено неверно!')
            messages.error(request, form.errors)
            return HttpResponseRedirect('/authorization', locals())

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        confirmed_password = form.cleaned_data.get('confirm_password')
        if password != confirmed_password:
            print("Invalid password details: {0}, {1}".format(password, confirmed_password))
            messages.error(request, 'Пароли не совпадают!')
            return HttpResponseRedirect('/authorization', locals())

        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user = Account.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name

        if user is None:
            return HttpResponseRedirect('/login', locals())

        user.save()
        login(request, user)

        return HttpResponseRedirect('/', locals())
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'registration_form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/', locals())

def rating(request):
    games = Game.objects.all()

    sorted_games = games.order_by('general_rate')

    return render(request, 'rating.html',
                  {'sorted_games': sorted_games})
