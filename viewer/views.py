from django.db.models import Avg
from django.shortcuts import render, redirect
from logging import getLogger

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from viewer.models import *
from django.forms import Form, ModelChoiceField, Textarea, IntegerField, CharField, ModelMultipleChoiceField, \
    CheckboxSelectMultiple, ModelForm, DateField, SelectDateWidget, DateInput

LOGGER = getLogger()


# Create your views here.


def hello(request):
    return HttpResponse('Hello Zoltan')



def hello1(request, s):
    return HttpResponse(f'hello {s}')


def hello2(request):
    print(10*'*')
    print(request)
    print()
    print(request.GET)
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello {s}')


def hello3(request):
    return render(request, template_name='index.html')


def index(request):
    return render(request, 'index.html')

def movies(request):
    list_of_movies = Movie.objects.all()
    context = {'movies': list_of_movies}
    return render(request, 'movies.html', context)


def movie(request, pk):
    movie_obj = Movie.objects.get(id=pk)
    comments = Comment.objects.filter(movie=movie_obj).order_by('-created')
    print(comments)



    avg_rating = None
    if len(Rating.objects.filter(movie=movie_obj)) > 0:
        avg_rating = Rating.objects.filter(movie=movie_obj).aggregate(Avg('rating'))
    print('avg_rating:', avg_rating)
    user = request.user
    user_rating = None
    if request.user.is_authenticated:
        if Rating.objects.filter(movie=movie_obj, user=user).count() > 0:
            user_rating = Rating.objects.get(movie=movie_obj, user=user)

    context = {'movie': movie_obj, 'avg_rating': avg_rating, 'user_rating': user_rating, 'comments': comments}

    return render(request, 'movie_detail.html', context)

############ FORMS

# from django.forms import (
#     Form, ModelChoiceField, CharField, IntegerField, Textarea, ModelMultipleChoiceField, CheckboxSelectMultiple
# )
# from viewer.models import Country, Genre, Person
#
# from django.views.generic import FormView
# from django.urls import reverse_lazy
# from logging import getLogger
# from .models import *
#
# LOGGER = getLogger()


class MovieForm(Form):
    title_orig = CharField(max_length=64)
    title_cz = CharField(max_length=64, required=False)
    title_sk = CharField(max_length=64, required=False)
    countries = ModelMultipleChoiceField(queryset=Country.objects)
    genres = ModelMultipleChoiceField(queryset=Genre.objects, widget=CheckboxSelectMultiple)
    directors = ModelMultipleChoiceField(queryset=Person.objects)
    actors = ModelMultipleChoiceField(queryset=Person.objects)
    year = IntegerField(min_value=1900, max_value=2025)
    video = CharField(max_length=128, required=False)
    description = CharField(widget=Textarea, required=False)

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieModelForm(ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieFormView(FormView):
    template_name = 'movie_create.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        new_movie = Movie.objects.create(
            title_orig=cleaned_data['title_orig'],
            title_cz=cleaned_data['title_cz'],
            title_sk=cleaned_data['title_sk'],
            #countries=cleaned_data['countries'],
            #genres=cleaned_data['genres'],
            #directors=cleaned_data['directors'],
            #actors=cleaned_data['actors'],
            year=cleaned_data['year'],
            video=cleaned_data['video'],
            description=cleaned_data['description']
        )
        new_movie.countries.set(cleaned_data['countries'])
        new_movie.genres.set(cleaned_data['genres'])
        new_movie.directors.set(cleaned_data['directors'])
        new_movie.actors.set(cleaned_data['actors'])
        new_movie.save()
        return result

    def form_invalid(self, form):
        print('User provided invalid data.')
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieCreateView(CreateView):
    template_name = 'movie_create.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')



class PersonForm(Form):
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    birth_date = DateField(required=False)
    biography = CharField(required=False)

    def clean_first_name(self):
        initial_data = super().clean()
        initial = initial_data['first_name']
        return initial.capitalize()

    def clean_last_name(self):
        initial_data = super().clean()
        inital = initial_data['last_name']
        return initial.capitalize()

class PersonCreateView(FormView):
    template_name = 'person_create.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_create')


def rate_movie(request):
    user = request.user
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_obj = Movie.objects.get(id=movie_id)
        rating = request.POST.get('rating')

        if Rating.objects.filter(movie=movie_obj, user=user).count() > 0:
            # aktulaizujeme hodnotenie
            user_rating =  Rating.objects.get(movie=movie_obj, user=user)
            user_rating.rating = rating
            user_rating.save()
        else:
            Rating.objects.create(
                movie=movie_obj,
                user=user,
                rating=rating
            )
    return redirect(f"/movie/{movie_id}")


def add_comment(request):
    user = request.user
    print(request.POST)
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_obj = Movie.objects.get(id=movie_id)
        comment = request.POST.get('comment')
        Comment.objects.create(
            movie=movie_obj,
            user=user,
            comment=comment
        )
    print(20*'#')
    print(user)
    print(comment)
    print(movie_id)
    return redirect(f"/movie/{movie_id}")



