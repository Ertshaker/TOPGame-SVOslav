from Site.models import *
from Site.forms import *
from django.views.generic import DetailView, UpdateView
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, reverse
from django.views.decorators.cache import cache_page

# Create your views here.

def index_view(request):
    games = Game.objects.all()
    return render(request, 'index.html',
                  {'games': games})

class GameDetailView(DetailView):
    model = Game
    template_name = 'game.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()  # Получаем объект Game
        context['page_name'] = game.name
        return context

    def post(self, request, *args, **kwargs):
        game = self.get_object()
        user: Account = request.user
        if request.POST.get(""):
            change_password_form = ChangePasswordForm(request.POST)
            if not change_password_form.is_valid():
                messages.error(request, 'Какое то из полей заполнено неверно!')
                return HttpResponseRedirect(reverse('user-detail', kwargs={'username': user.username}))

            if not user.check_password(change_password_form.cleaned_data['old_password']):
                messages.error(request, 'Старый пароль введен неверно!')
                return HttpResponseRedirect(reverse('user-detail', kwargs={'username': user.username}))

            username = user.username
            new_password = change_password_form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            change_password_form.clean()

            login(request, authenticate(username=username, password=new_password))



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

    top_games = games.order_by('-general_rate')
    top1 = top_games[0]
    top2 = top_games[1]
    top3 = top_games[2]

    sorted_games = Game.objects.exclude(id__in=[top1.id, top2.id, top3.id])



    return render(request, 'rating.html',
                  {'sorted_games': sorted_games, 'top1': top1, 'top2': top2, 'top3': top3})
