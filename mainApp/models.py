from django.db import models

# Create your models here.
class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre_empleado = models.CharField(max_length=100)
    rut_empleado = models.CharField(max_length=20)
    genero_empleado = models.CharField(max_length=20, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    direccion_empleado = models.CharField(max_length=100)
    telefono_empleado = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_empleado

    def obtener_id_empleado(self):
        return self.id_empleado
    
class InformacionLaboral(models.Model):
    id_informacion_laboral = models.AutoField(primary_key=True)
    fecha_ingreso = models.DateField()
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=100)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_departamento
    
class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=100)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_area
    
class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=100)
    id_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_cargo

    def obtener_id_empleado(self):
        return self.id_empleado.id_empleado
    
class ContactoEmergencia(models.Model):
    id_contacto_emergencia = models.AutoField(primary_key=True)
    nombre_contacto = models.CharField(max_length=100)
    relacion_contacto = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_contacto
    
class ContactoEmpleado(models.Model):
    id_contacto_empleado = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    id_contacto_emergencia = models.ForeignKey(ContactoEmergencia, on_delete=models.CASCADE)


class CargaFamiliar(models.Model):
    id_carga_familiar = models.AutoField(primary_key=True)
    nombre_carga = models.CharField(max_length=100)    
    rut_carga = models.CharField(max_length=100)    
    genero_carga = models.CharField(max_length=100)    
    parentesco_carga = models.CharField(max_length=100)    
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_carga

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre_perfil = models.CharField(max_length=100)
    clave_perfil = models.CharField(max_length=100)
    tipo_perfil = models.CharField(max_length=20, choices=[('empleado', 'Empleado'), ('recursos humanos', 'Recursos Humanos')])
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_perfil