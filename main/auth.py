from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User, Trip


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/")
    

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "first_name": f"{log_user}",
                    "last_name" : log_user.last_name,
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['user'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/travels")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Password o Email  incorrectos.")

        return redirect("/")
    else:
        return render(request, 'home.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)

        email_checkers = User.objects.all()

        for mail in email_checkers:
            if request.POST['email'] == mail.email:
                messages.error(request, "Este correo ya ha sido utilizado previamente")
                return redirect("/")

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_name'] =  request.POST['first_name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo.first_name}",
                "name": usuario_nuevo.last_name,
                "email": usuario_nuevo.email
            }
            return redirect("/travels")

        return redirect("/")
    else:
        return render(request, 'home.html')