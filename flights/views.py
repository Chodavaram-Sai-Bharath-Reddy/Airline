from django.shortcuts import render
from .models import Flight, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

flights = Flight.objects.all()


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))
    else:
        return render(request, 'flights/index.html', {
            'flights': flights
        })


def flight(request, flight_id):

    try:
        flight = Flight.objects.get(pk=flight_id)
    except:
        flight = None

    if flight:
        return render(request, 'flights/flight.html', {
            'flight': flight,
            'passengers': flight.passengers.all(),
            'non_passengers': Passenger.objects.exclude(flights=flight).all()
        })
    else:
        return render(request, 'flights/noFlight.html')


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
