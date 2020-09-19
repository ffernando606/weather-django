import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=es&appid=YOURKEY'
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                
                else:
                    err_msg = 'La ciudad no existe'
            else:
                err_msg = 'La ciudad ya está indexada!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'La ciudad fue agregada correctamente'
            message_class = 'is-success '
    print(err_msg)        

    form = CityForm()
    
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
            
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'main': r['weather'][0]['main'],
            'icon': r['weather'][0]['icon'],
            'humidity': r['main']['humidity'],
            'feels_like': r['main']['feels_like'],
            }

        weather_data.append(city_weather)

    

    context = {
        'weather_data': weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class,
    }
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')