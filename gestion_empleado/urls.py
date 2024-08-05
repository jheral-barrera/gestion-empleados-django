from django.contrib import admin
from django.urls import path

from mainApp.views import index, acceso, registro, listar, verInformacionEmpleado, actualizarInformacionEmpleado, eliminar, actualizar, agregar, eliminarEmpleado, actualizarEmpleado, filtradoEmpleados, eliminarCargaFamiliar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('acceso/', acceso),
    path('registro/', registro),
    path('administrador/listar/<int:id_usuario>', listar),
    path('administrador/eliminar/<int:id_usuario>', eliminar),
    path('administrador/eliminar/<int:id>/<int:id_usuario>', eliminarEmpleado),
    path('administrador/actualizar/<int:id_usuario>', actualizar),
    path('administrador/actualizar/<int:id>/<int:id_usuario>', actualizarEmpleado),
    path('administrador/agregar/<int:id_usuario>', agregar),
    path('empleado/verInformacion/<int:id>', verInformacionEmpleado),
    path('empleado/actualizarInformacion/<int:id>', actualizarInformacionEmpleado),
    path('administrador/listar/filtro/<int:id_usuario>', filtradoEmpleados, name='filtrado'),
    path('administrador/eliminarCarga/<int:id>/<int:id_carga>/<int:id_usuario>', eliminarCargaFamiliar)
]
