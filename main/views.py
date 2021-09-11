from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import *

@login_required
def index(request):
    current_user = request.session['user']['id']
    owner = Trip.objects.all().filter(manager=current_user)
    travelers = Trip.objects.all().filter(traveler=current_user).exclude(manager=current_user)
    trips = Trip.objects.all().exclude(traveler=current_user).exclude(manager=current_user)
    context = {
        "owners" : owner,
        "travelers": travelers,
        "trips" : trips
    }
    return render(request, 'travel_section.html', context)

@login_required
def add(request):

    return render(request, 'add.html')

def add_trip(request):
    try:
        datetime.datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
    except:
        messages.error(request, "ingrese una fecha")
        return redirect("/add")
    try:
        datetime.datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
    except:
        messages.error(request, "ingrese una fecha")
        return redirect("/add")
    errors = Trip.objects.validador_basico(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/add")
    
    current_user = request.session['user']['id']
    in_manager = User.objects.get(id=current_user)
    # in_traveler = User.objects.get(id=current_user)
    in_destination=request.POST['destination']
    in_description=request.POST['description']
    in_start_date=request.POST['start_date']
    in_end_date=request.POST['end_date']
    new_trip = Trip.objects.create(manager=in_manager,
                        # traveler=in_traveler,
                        destination=in_destination,
                        description=in_description,
                        start_date=in_start_date,
                        end_date=in_end_date)
    
    new_trip.traveler.add(in_manager)

    return redirect("/travels")

# author.books.remove(book)
# INSTANCIA_TRIP . VARIABLE OBJETIVO . COMANDO ( INSTANCIA_USER )

def cancel_trip(request, trip_id):
    current_user_id = request.session['user']['id']
    current_user = User.objects.get(id=current_user_id)
    trip = Trip.objects.get(id=int(trip_id))
    trip.traveler.remove(current_user)
    return redirect("/travels")

def delete_trip(request, trip_id):
    Trip.objects.filter(id=int(trip_id)).delete()
    return redirect("/travels")

def join_trip(request, trip_id):
    current_user_id = request.session['user']['id']
    current_user = User.objects.get(id=current_user_id)
    trip = Trip.objects.get(id=int(trip_id))
    trip.traveler.add(current_user)
    return redirect("/travels")

def view_trip(request, trip_id):
    trip = Trip.objects.get(id=int(trip_id))
    manager = User.objects.filter(managers = trip)
    travelers = User.objects.filter(travelers = trip).exclude(managers = trip)

    context = {
        "trip":trip,
        "manager":manager,
        "travelers":travelers
    }

    return render(request, 'view.html', context)