from django import forms

from .models import Empleado, Perfil, CargaFamiliar, InformacionLaboral, Departamento, Area, Cargo, ContactoEmergencia

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'

class CargaFamiliarForm(forms.ModelForm):
    class Meta:
        model = CargaFamiliar
        fields = '__all__'  # Incluir todos los campos, incluyendo id_empleado
        exclude = ['id_empleado']

class InformacionLaboralForm(forms.ModelForm):
    class Meta:
        model = InformacionLaboral
        fields = '__all__'  # Incluir todos los campos, incluyendo id_empleado
        exclude = ['id_empleado']

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'  # Incluir todos los campos, incluyendo id_empleado
        exclude = ['id_empleado']

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'  # Incluir todos los campos, incluyendo id_empleado
        exclude = ['id_empleado', 'id_departamento']

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'  # Incluir todos los campos, incluyendo id_empleado
        exclude = ['id_empleado', 'id_area']

class ContactoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = '__all__'  # Incluir todos los campos, incluyendo id_empleado
        exclude = ['id_empleado']

