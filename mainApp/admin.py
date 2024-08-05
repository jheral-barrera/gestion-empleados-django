from django.contrib import admin

from mainApp.models import Empleado, Perfil, CargaFamiliar, InformacionLaboral, Departamento, Area, Cargo, ContactoEmergencia, ContactoEmpleado

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'nombre_empleado', 'rut_empleado', 'genero_empleado', 'direccion_empleado', 'telefono_empleado')

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id_perfil', 'nombre_perfil', 'clave_perfil', 'tipo_perfil', 'id_empleado')

class CargaFamiliarAdmin(admin.ModelAdmin):
    list_display = ('id_carga_familiar', 'nombre_carga', 'rut_carga', 'genero_carga', 'parentesco_carga', 'id_empleado')

class InformacionLaboralAdmin(admin.ModelAdmin):
    list_display = ('id_informacion_laboral', 'fecha_ingreso', 'id_empleado')

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id_departamento', 'nombre_departamento', 'id_empleado')

class AreaAdmin(admin.ModelAdmin):
    list_display = ('id_area', 'nombre_area', 'id_departamento', 'id_empleado')

class CargoAdmin(admin.ModelAdmin):
    list_display = ('id_cargo', 'nombre_cargo', 'id_area', 'id_empleado')

class ContactoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_contacto_empleado', 'id_empleado', 'id_contacto_emergencia')

class ContactoEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('id_contacto_emergencia', 'nombre_contacto', 'relacion_contacto', 'telefono_contacto', 'id_empleado')


admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(CargaFamiliar, CargaFamiliarAdmin)
admin.site.register(InformacionLaboral, InformacionLaboralAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(ContactoEmergencia, ContactoEmergenciaAdmin)
admin.site.register(ContactoEmpleado, ContactoEmpleadoAdmin)
