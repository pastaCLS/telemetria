from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from models import Producto, Tanque, Lector, Lectura, Task
from forms import TanqueForm
# Create your views here.

from ftplib import FTP

def main(request):
	formulario = AuthenticationForm()
	return render_to_response("index.html", {'formulario':formulario}, context_instance=RequestContext(request))

def entrar(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					msg = "El usuario se encuentra inactivo momentaneamente, pongase en contacto con nuestro <a class='alert-link' href='mailto://'>administrador</a>."
					return render_to_response('error.html', {"mensaje": msg}, context_instance=RequestContext(request))
			else:
				msg = "Usuario o Password incorrecto, por favor verifique."
				return render_to_response('error.html', {'mensaje': msg}, context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', {'formulario': formulario}, context_instance=RequestContext())

@login_required(login_url="/entrar")
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url="/entrar")
def administracion(request):
	tanques = Tanque.objects.filter(usuario=request.user)
	lecturas = []
    paso = 25
	for i in tanques:
	    counter = Lectura.objects.filter(lector=Lector.objects.get(tanque=i)).count()
        desde = request.GET.get("desde")
        hasta = request.GET.get("hasta")
        if not desde or not hasta:
            # por default muestra las ultimas 25
            desde = counter-paso
            hasta = counter

            if desde < 0 or hasta > counter:
                desde = 0
                hasta = paso

		lecturas.append(Lectura.objects.filter(lector=Lector.objects.get(tanque=i))[desde:hasta])

	return render_to_response('panel.html', {'tanques': tanques, 'lecturas_tanque': lecturas, 'desde': desde, 'hasta': hasta, 'paso': paso}, context_instance=RequestContext(request))

@csrf_exempt
def parser(request):
    if request.method == "GET":
        try:
            log = Lector.objects.get(equipo=request.GET["tanque_id"])
            lectura = Lectura(lector=log)
            lectura.stock = int(request.GET["stock"])
            lectura.save()
        except:
            return HttpResponse("error")

	#if request.method == 'POST':
	#	for filename, file in request.FILES.iteritems():
	#		name = request.FILES[filename].name
	#		linea = request.FILES[filename].read()
	#		spliteado = linea.split(",")

	#		log = Lector.objects.get(equipo=spliteado[0])
	#		lectura = Lectura(lector=log)
	#		lectura.stock = int(spliteado[1])
	#		lectura.save()

	return HttpResponse("success")

	#return HttpResponse("failed")

@login_required(login_url="/entrar")
def ajax_niveles(request):
	if request.is_ajax():
		response = []
		for tank in Tanque.objects.filter(usuario=request.user):
			try:
				response.append(Lectura.objects.filter(lector=Lector.objects.get(tanque=tank)).order_by('-fecha')[0])
			except IndexError:
				pass

		return HttpResponse(serializers.serialize("json", response), content_type="application/json")
	else:
		raise Http404

@csrf_exempt
def ajax_portfolio(request):
	if request.is_ajax():
		return HttpResponse(serializers.serialize("json", Producto.objects.all(), fields=("nombre")), content_type="application/json")
	else:
		raise Http404

@login_required(login_url="/entrar")
def modificar_tanque(request, tanque):
	if request.method == "POST":
		if Tanque.objects.get(id=tanque).usuario == request.user:
			modificado = Tanque.objects.get(id=tanque)
			modificado.producto = request.POST['producto']
			modificado.funcion = request.POST['funcion']
			modificado.bomba = request.POST['bomba']
			modificado.dosificacion = request.POST['dosificacion']
			modificado.caudal = request.POST['caudal']
			modificado.lectura = request.POST['lectura']
			modificado.critico = request.POST['critico']
			modificado.capacidad = request.POST['capacidad']

			modificado.save()
			#aqui tengo que grabar los tasks

			bar = Task()
			bar.lector = modificado.lector
			bar.horario = request.POST['lectura']

			bar.save()

			msg="Los datos de su tanque han sido actualizados satisfactoriamente. En breve sera redirigido a su panel de control."
			return render_to_response("tanquemodificado.html", {'mensaje': msg}, context_instance=RequestContext(request));
		else:
			return render_to_response("error.html")

		return HttpResponse(request.POST['capacidad']);


def ver_tareas(request):
	return render_to_response("tareas.html", {'tareas': Task.objects.filter(done=False)})

@login_required(login_url="/entrar")
def activar_bomba(request, tanque):
	#tanque es el id del tanque a cambiar
	# caudal = metros_cubicos/tiempo
	# metros_cubicos/caudal = tiempo

	#los metros cubicos van cargados en metros_cubicos/minuto
	minutos = 60*(float(request.GET['litros'])/float(Tanque.objects.get(id=tanque).caudal))

	#fh = open("A1234567config.txt", "wb")
	#fh.write(str(int(minutos)))
	#fh.close()

	#fh = open("A1234567config.txt", "r")
	#ftps = FTP('ftp.dframirez80.esy.es', 'u232318282', 'boca1980')
	#ftps.storlines('STOR A1234567config.txt', fh)
	#ftps.close()
	#fh.close()

	tarea = Task()
	tarea.horario = minutos
	tarea.lector = Tanque.objects.get(id=tanque).lector
	tarea.done = False
	tarea.save()

	return render_to_response("tanquemodificado.html", {"mensaje":"Los datos fueron enviados al sensor"}, context_instance=RequestContext(request))

def cambiar_estado(request, tarea):
	tarea = Task.objects.get(id=tarea)
	tarea.done = True
	tarea.save()
	return HttpResponse("OK")
