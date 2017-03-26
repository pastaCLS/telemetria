from django.contrib import admin
from models import Producto, Profile, Tanque, Lector, Lectura, Task

class ProductoAdmin(admin.ModelAdmin):
	pass

class TanqueAdmin(admin.ModelAdmin):
	pass

class ProfileAdmin(admin.ModelAdmin):
	pass

class LectorAdmin(admin.ModelAdmin):
	pass

class LecturaAdmin(admin.ModelAdmin):
	pass

class TaskAdmin(admin.ModelAdmin):
	pass

admin.site.register(Lectura, LecturaAdmin)
admin.site.register(Lector, LectorAdmin)
admin.site.register(Tanque, TanqueAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Task, TaskAdmin)
