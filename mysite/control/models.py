#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Producto(models.Model):
	nombre = models.CharField(max_length=40)
	descripcion = models.TextField(max_length=2000)
	foto = models.ImageField(upload_to="products")
	precio = models.FloatField()
	
	def __unicode__(self):
		return "<Name: %s>" % self.nombre

ARGENTINA = u"AR"
BRASIL = u"BR"
CHILE = u"CH"
PARAGUAY = u"PA"

PAIS_CHOICES = (
	(ARGENTINA, u"Argentina"),
	(BRASIL, u"Brasil"),
	(CHILE, u"Chile"),
	(PARAGUAY, u"Paraguay"),
)

CLARO = u"CL"
MOVISTAR = u"MV"
PERSONAL = u"PE"

OPERADORA_CHOICES = (
	(CLARO, u"Claro"),
	(MOVISTAR, u"Movistar"),
	(PERSONAL, u"Personal")
)

BUENOSAIRES = u"BA"
SANTAFE = u"SF"
CATAMARCA = u"CT"
JUJUY = u"JY"
MISIONES = u"MS"
LARIOJA = u"LR"

PROVINCIA_CHOICES = (
	(BUENOSAIRES, u"Buenos Aires"),
	(SANTAFE, u"Santa Fé"),
	(CATAMARCA, u"Catamarca"),
	(JUJUY, u"Jujuy"),
	(MISIONES, u"Mísiones"),
	(LARIOJA, u"La Ríoja")
)

CAPITAL = u"CF"
RAFAELCALZADA = u"RC"

LOCALIDAD_CHOICES = (
	(CAPITAL, u"Capital Federal"),
	(RAFAELCALZADA, u"Rafael Calzada"),
)

class Profile(models.Model):
	usuario = models.OneToOneField(User, primary_key=True)
	pais = models.CharField(max_length=2, choices=PAIS_CHOICES)
	provincia = models.CharField(max_length=2, choices=PROVINCIA_CHOICES)
	localidad = models.CharField(max_length=2, choices=LOCALIDAD_CHOICES)
	operadora = models.CharField(max_length=2, choices=OPERADORA_CHOICES)
	
	def __unicode__(self):
		return "<Profile: %s, %s>" % (self.usuario.username, self.operadora)

class Tanque(models.Model):
	usuario = models.ForeignKey(User)
	yacimiento = models.CharField(max_length=25)
	producto = models.CharField(max_length=30)
	funcion = models.CharField(max_length=30)
	bomba = models.CharField(max_length=30)
	dosificacion = models.CharField(max_length=10)
	caudal = models.IntegerField()
	lectura = models.IntegerField()
	critico = models.IntegerField()
	capacidad = models.IntegerField()
	altura = models.FloatField()

	def __unicode__(self):
		return "<Tanque: %s, %s>" % (self.yacimiento, self.producto)
	
class Lector(models.Model):
	tanque = models.OneToOneField(Tanque, primary_key=True)
	equipo = models.CharField(max_length=8)
	periodo_de_lectura = models.IntegerField()
	tiempo_de_encendido = models.IntegerField()
	operador = models.CharField(max_length=2, choices=OPERADORA_CHOICES)
	celular = models.CharField(max_length=15)
	detencion = models.IntegerField()

	def __unicode__(self):
		return "<Lector: %s, %s>" % (self.tanque.yacimiento, self.celular)

class Lectura(models.Model):
	lector = models.ForeignKey(Lector)
	fecha = models.DateTimeField(auto_now=True)
	stock = models.IntegerField()

	def __unicode__(self):
		return "<Lectura: %s, %s>" % (self.lector.equipo, self.fecha)
	
class Task(models.Model):
	lector = models.ForeignKey(Lector)
	horario = models.IntegerField()
	done = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "<Task: %s, %d>" % (self.lector.equipo, self.horario)
