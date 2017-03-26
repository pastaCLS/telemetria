from django.conf.urls.defaults import * # import patterns, include, url
from django.conf import settings
from django.contrib import admin
from control.views import main, entrar, cerrar, administracion, parser, ajax_niveles, ajax_portfolio, modificar_tanque, ver_tareas, activar_bomba, cambiar_estado
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'telemetria.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', main),
	url(r'^entrar', entrar),
	url(r'^cerrar', cerrar),
	url(r'^privado', administracion),
	url(r'^test.php$', parser),
	url(r'^nivel/tanque', ajax_niveles),
	url(r'^lista/productos.json', ajax_portfolio),
	url(r'^configurar/(?P<tanque>\d+)', modificar_tanque),
	url(r'^activar/bomba/(?P<tanque>\d+)', activar_bomba),
	url(r'^tasks', ver_tareas),
	url(r'^change/task/(?P<tarea>\d+)', cambiar_estado),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
    url(r'^admin/', include(admin.site.urls)),
)
