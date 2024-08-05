from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from .models import Empleado, InformacionLaboral, Departamento, Area, Cargo, ContactoEmergencia, ContactoEmpleado, CargaFamiliar, Perfil
from . import forms

# Create your views here.

def index(req):
    return render(req, 'index.html')

def acceso(req):

    if req.method == 'POST':
        registro = req.POST
        validacion_rut = registro['form_acceso_rut'].endswith('-',7 ,9)

        try:
            empleado = Empleado.objects.get(rut_empleado=registro['form_acceso_rut'])
            perfil = Perfil.objects.get(id_empleado=empleado)

            if registro['form_acceso_nombre'] != perfil.nombre_perfil:
                print("El nombre de usuario es distinto. Intenta otra vez")
                messages.error(req, 'El nombre de usuario es distinto. Intenta otra vez')
                return redirect('/acceso')

            if registro['form_acceso_clave'] != perfil.clave_perfil:
                print("La clave de acceso es distinta. Intenta otra vez")
                messages.error(req, 'La clave de acceso es distinta. Intenta otra vez')
                return redirect('/acceso')
        except:
            print(f"No se encontro un perfil registrado con el Rut: {registro['form_acceso_rut']}")
            messages.error(req, f"No se encontro un perfil registrado con el Rut: {registro['form_acceso_rut']}")
            if not validacion_rut:
                print(f"El Rut {registro['form_acceso_rut']} debe contener el guion.")
                messages.error(req, f"El Rut {registro['form_acceso_rut']} debe contener el guion.")
                return redirect('/acceso')
            return redirect('/acceso')
        
        if perfil.tipo_perfil == 'recursos humanos':
            return redirect(f'/administrador/listar/{empleado.id_empleado}')
        if perfil.tipo_perfil == 'empleado':
            return redirect(f'/empleado/verInformacion/{empleado.id_empleado}')

    datos = {}
    return render(req, 'acceso.html')

def registro(req):
    if req.method == 'POST':
        registro = req.POST

        # Valida las claves de acceso
        if registro['clave_perfil'] != registro['clave2_perfil']:
            print('Las claves no coinciden')
            messages.error(req, 'Las claves no coinciden. Intentalo otra vez')
            return redirect('/registro')
        
        # Verifica si existe un perfil asociado al empleado
        rut_existente = Empleado.objects.filter(rut_empleado=registro['rut_perfil']).exists()
        if rut_existente:
            print(f"Ya existe registrado un empleado con el Rut: {registro['rut_perfil']}")
            
            try:
                empleado = Empleado.objects.get(rut_empleado=registro['rut_perfil'])
                perfil_existente = Perfil.objects.filter(id_empleado=empleado)

                if perfil_existente:
                    print(f"Ya existe registrado un perfil para el empleado con el Rut: {registro['rut_perfil']}")
                    messages.error(req, f"Ya existe registrado un perfil para el empleado con el Rut: {registro['rut_perfil']}")
                    return redirect("/registro")

                perfil = Perfil(
                    nombre_perfil=registro['nombre_perfil'], 
                    clave_perfil=registro['clave_perfil'],
                    tipo_perfil=registro['tipo_perfil'],
                    id_empleado=empleado
                )
                perfil.save()
                messages.success(req, 'Se ha registrado con exito.')
            except:
                print(f"No existe ningun empleado con el Rut: {registro['rut_perfil']}")
                messages.error(req, f"No existe ningun empleado con el Rut: {registro['rut_perfil']}")
                return redirect("/registro")

            return redirect('/registro')
        
        messages.error(req, f'No se encuentra registrado el empleado con rut: {registro["rut_perfil"]}')
        return redirect('/registro')
    else:
        print("no se pudo realizar el registro")
        # messages.error(req, 'No se pudo realizar el registro.')

    return render(req, 'registro.html')

def listar(req, id_usuario):
    empleados = Empleado.objects.all()
    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)
    cargos = Cargo.objects.all()
    
    # filtro de empleados
    generos_filtro = Empleado.objects.values_list('genero_empleado', flat=True).distinct()
    cargos_filtro = Cargo.objects.values_list('nombre_cargo', flat=True).distinct()
    areas_filtro = Area.objects.values_list('nombre_area', flat=True).distinct()
    departamentos_filtro = Departamento.objects.values_list('nombre_departamento', flat=True).distinct()
    
    datos = {
        'empleados' : empleados,
        'cargos' : cargos,
        'empleado_usuario' : empleado_usuario,
        'generos': generos_filtro,
        'cargos_disponibles': cargos_filtro,
        'areas_disponibles': areas_filtro,
        'departamentos_disponibles': departamentos_filtro
    }
    return render(req, 'listarEmpleados.html', datos)

def agregar(req, id_usuario):
    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)

    if req.method == 'POST':
        registro = req.POST
        if registro.get('form_cantidad_cargas', 0) == '':
            cantidad = 0
        else:
            cantidad = int(registro.get('form_cantidad_cargas', 0))

        validacion_rut = registro['form_rut_empleado'].endswith('-',7 ,9)
        rut_existente = Empleado.objects.filter(rut_empleado = registro['form_rut_empleado']).exists()

        if not validacion_rut:
            print(f"El Rut {registro['form_rut_empleado']} debe contener el guion.")
            return redirect(f'/administrador/agregar/{id_usuario}')

        if rut_existente:
            print(f"El empleado con rut: {registro['form_rut_empleado']} ya existe")
            return redirect(f'/administrador/agregar/{id_usuario}')

        for i in range(cantidad):
            rut_carga_existente = CargaFamiliar.objects.filter(rut_carga = registro[f'form_rut_carga{str(i)}']).exists()

            if rut_carga_existente:
                print(f"La carga familiar con Nombre: {registro[f'form_nombre_carga{str(i)}']} rut: {registro[f'form_rut_carga{str(i)}']} ya existe")
                return redirect(f'/administrador/agregar/{id_usuario}')

        empleado = Empleado(
            nombre_empleado=registro['form_nombre_empleado'],
            rut_empleado=registro['form_rut_empleado'],
            genero_empleado=registro['form_genero_empleado'],
            direccion_empleado=registro['form_direccion_empleado'],
            telefono_empleado=registro['form_telefono_empleado']
        )
        empleado.save()
        print("Guardado 1")

        informacionLaboral = InformacionLaboral(
            fecha_ingreso=registro['form_fecha_ingreso'],
            id_empleado=empleado
        )
        informacionLaboral.save()
        print("Guardado 2")

        departamento = Departamento(
            nombre_departamento=registro['form_nombre_departamento'],
            id_empleado=empleado
        )
        departamento.save()
        print("Guardado 3")

        area = Area(
            nombre_area=registro['form_nombre_area'],
            id_empleado=empleado,
            id_departamento=departamento
        )
        area.save()
        print("Guardado 4")

        cargo = Cargo(
            nombre_cargo=registro['form_nombre_cargo'],
            id_empleado=empleado,
            id_area=area
        )
        cargo.save()
        print("Guardado 5")

        contactoEmergencia = ContactoEmergencia(
            nombre_contacto=registro['form_nombre_contacto'],
            relacion_contacto=registro['form_relacion_contacto'],
            telefono_contacto=registro['form_telefono_contacto'],
            id_empleado=empleado
        )
        contactoEmergencia.save()
        print("Guardado 6")

        contactoEmpleado = ContactoEmpleado(
            id_empleado = empleado,
            id_contacto_emergencia = contactoEmergencia
        )
        contactoEmpleado.save()

        for i in range(cantidad):
            cargaFamiliar = CargaFamiliar(
                nombre_carga=registro[f'form_nombre_carga{str(i)}'],
                rut_carga=registro[f'form_rut_carga{str(i)}'],
                genero_carga=registro[f'form_genero_carga{str(i)}'],
                parentesco_carga=registro[f'form_parentesco_carga{str(i)}'],
                id_empleado=empleado
            )

            cargaFamiliar.save()
            print("Guardado carga familiar")

        

        messages.success(req, 'Se ha agregado con exito el empleado.')
            
        return redirect(f'/administrador/listar/{id_usuario}')
    else:
        print("No se pudo enviar el formulario.")
    
    datos = {
        'empleado_usuario' : empleado_usuario
    }

    return render(req, 'agregarEmpleados.html', datos)

def eliminar(req, id_usuario):
    empleados = Empleado.objects.all()
    cargos = Cargo.objects.all()

    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)

    datos = {
        'empleados' : empleados,
        'cargos' : cargos,
        'empleado_usuario' : empleado_usuario
    }
    return render(req, 'eliminarEmpleados.html', datos)

def eliminarEmpleado(req, id, id_usuario):
    empleado_eliminar = Empleado.objects.get(id_empleado=id)
    empleado_sesion = Empleado.objects.get(id_empleado=id_usuario)

    if empleado_eliminar.id_empleado == empleado_sesion.id_empleado:
        messages.error(req, "No puedes eliminar tu propio registro mientras tu sesión está activa.")
    else:
        empleado_eliminar.delete()
        messages.success(req, f"Empleado {empleado_eliminar.nombre_empleado} eliminado exitosamente.")
    return redirect(f'/administrador/eliminar/{id_usuario}')

def actualizar(req, id_usuario):
    empleados = Empleado.objects.all()
    cargos = Cargo.objects.all()

    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)

    datos = {
        'empleados' : empleados,
        'cargos' : cargos,
        'empleado_usuario' : empleado_usuario
    }
    return render(req, 'actualizarEmpleados.html', datos)

def actualizarEmpleado(req, id, id_usuario):
    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)

    actualizar = True
    formularioCargas = []

    empleado = Empleado.objects.get(id_empleado=id)
    informacion_laboral = InformacionLaboral.objects.get(id_empleado=empleado)
    departamento = Departamento.objects.get(id_empleado=empleado)
    area = Area.objects.get(id_empleado=empleado)
    cargo = Cargo.objects.get(id_empleado=empleado)
    contacto_emergencia = ContactoEmergencia.objects.get(id_empleado=empleado)
    cargas_familiares = CargaFamiliar.objects.filter(id_empleado=empleado)
    cantidad_cargas = CargaFamiliar.objects.filter(id_empleado=empleado).count()

    print('cargas familiares', len(formularioCargas))

    if req.method == 'POST':
        registro = req.POST
        cantidad = int(registro.get('form_cantidad_cargas', 0))

        print(cantidad)

        empleado = Empleado.objects.get(id_empleado=id)
        # Actualizar Empleado
        empleado.nombre_empleado = registro['form_nombre_empleado']
        empleado.rut_empleado = registro['form_rut_empleado_hidden']
        empleado.genero_empleado = registro['form_genero_empleado']
        empleado.direccion_empleado = registro['form_direccion_empleado']
        empleado.telefono_empleado = registro['form_telefono_empleado']
        empleado.save()
        print("Actualizado Empleado")

        # Actualizar InformacionLaboral
        informacion_laboral = InformacionLaboral.objects.get(id_empleado=empleado)
        informacion_laboral.fecha_ingreso = registro['form_fecha_ingreso']
        informacion_laboral.save()
        print("Actualizado InformacionLaboral")

        # Actualizar Departamento
        departamento = Departamento.objects.get(id_empleado=empleado)
        departamento.nombre_departamento = registro['form_nombre_departamento']
        departamento.save()
        print("Actualizado Departamento")

        # Actualizar Area
        area = Area.objects.get(id_empleado=empleado)
        area.nombre_area = registro['form_nombre_area']
        area.save()
        print("Actualizado Area")

        # Actualizar Cargo
        cargo = Cargo.objects.get(id_empleado=empleado)
        cargo.nombre_cargo = registro['form_nombre_cargo']
        cargo.save()
        print("Actualizado Cargo")

        # Actualizar ContactoEmergencia
        contacto_emergencia = ContactoEmergencia.objects.get(id_empleado=empleado)
        contacto_emergencia.nombre_contacto = registro['form_nombre_contacto']
        contacto_emergencia.relacion_contacto = registro['form_relacion_contacto']
        contacto_emergencia.telefono_contacto = registro['form_telefono_contacto']
        contacto_emergencia.save()
        print("Actualizado ContactoEmergencia")

        # Actualizar ContactoEmpleado
        contacto_empleado = ContactoEmpleado.objects.get(id_empleado=empleado)
        contacto_empleado.id_contacto_emergencia = contacto_emergencia
        contacto_empleado.save()
        print("Actualizado ContactoEmpleado")

        # Actualizar Cargas Familiares
        for i, carga in enumerate(cargas_familiares, start=1):
            carga.nombre_carga = registro[f'form_nombre_cargaRegistrada{str(i)}']
            carga.rut_carga = registro[f'form_rut_cargaRegistrada{str(i)}_hidden']
            carga.genero_carga = registro[f'form_genero_cargaRegistrada{str(i)}']
            carga.parentesco_carga = registro[f'form_parentesco_cargaRegistrada{str(i)}']
            carga.save()
            print(f"actualizada Carga Familiar registro {i}")

        if registro.get('form_nombre_carga0') is not None:
            for carga in range(cantidad):
                nueva_carga = CargaFamiliar(
                    nombre_carga=registro[f'form_nombre_carga{str(i-1)}'],
                    rut_carga=registro[f'form_rut_carga{str(i-1)}'],
                    genero_carga=registro[f'form_genero_carga{str(i-1)}'],
                    parentesco_carga=registro[f'form_parentesco_carga{str(i-1)}'],
                    id_empleado=empleado
                )
                nueva_carga.save()
                print(f"agregado nueva Carga Familiar {i}")

        return redirect(f'/administrador/listar/{id_usuario}')

    else:
        print("nuevo instanciamiento de formularios")
        formularioEmpleado = forms.EmpleadoForm(instance=empleado)
        formularioLaboral = forms.InformacionLaboralForm(instance=informacion_laboral)
        formularioDepartamento = forms.DepartamentoForm(instance=departamento)
        formularioArea = forms.AreaForm(instance=area)
        formularioCargo = forms.CargoForm(instance=cargo)
        formularioContacto = forms.ContactoEmergenciaForm(instance=contacto_emergencia)
        for carga_familiar in cargas_familiares:
            formularioCargas.append(forms.CargaFamiliarForm(instance=carga_familiar))
   
    datos = {
        'formularioEmpleado': formularioEmpleado,
        'formularioLaboral': formularioLaboral,
        'formularioDepartamento': formularioDepartamento,
        'formularioArea': formularioArea,
        'formularioCargo': formularioCargo,
        'formularioContacto': formularioContacto,
        'formularioCargas': formularioCargas,
        'actualizar': actualizar,
        'cantidadCargas': cantidad_cargas,
        'empleado_usuario' : empleado_usuario,
        'empleado': empleado
    }
    return render(req, 'agregarEmpleados.html', datos)

def verInformacionEmpleado(req, id):

    empleado = Empleado.objects.get(id_empleado=id)

    formularioCargas = []
    verInformacion = "ver"

    empleado = Empleado.objects.get(id_empleado=id)
    informacion_laboral = InformacionLaboral.objects.get(id_empleado=empleado)
    departamento = Departamento.objects.get(id_empleado=empleado)
    area = Area.objects.get(id_empleado=empleado)
    cargo = Cargo.objects.get(id_empleado=empleado)
    contacto_emergencia = ContactoEmergencia.objects.get(id_empleado=empleado)
    cargas_familiares = CargaFamiliar.objects.filter(id_empleado=empleado)
    cantidad_cargas = CargaFamiliar.objects.filter(id_empleado=empleado).count()

    print("instanciamiento de formularios")
    formularioEmpleado = forms.EmpleadoForm(instance=empleado)
    formularioLaboral = forms.InformacionLaboralForm(instance=informacion_laboral)
    formularioDepartamento = forms.DepartamentoForm(instance=departamento)
    formularioArea = forms.AreaForm(instance=area)
    formularioCargo = forms.CargoForm(instance=cargo)
    formularioContacto = forms.ContactoEmergenciaForm(instance=contacto_emergencia)
    for carga_familiar in cargas_familiares:
        formularioCargas.append(forms.CargaFamiliarForm(instance=carga_familiar))

    print('cargas familiares', len(formularioCargas))

    datos = {
        'formularioEmpleado': formularioEmpleado,
        'formularioLaboral': formularioLaboral,
        'formularioDepartamento': formularioDepartamento,
        'formularioArea': formularioArea,
        'formularioCargo': formularioCargo,
        'formularioContacto': formularioContacto,
        'formularioCargas': formularioCargas,
        'cantidadCargas': cantidad_cargas,
        'verInformacion': verInformacion,
        'empleado': empleado
    }

    return render(req, 'verInformacionEmpleado.html', datos)

def actualizarInformacionEmpleado(req, id):
    empleado = Empleado.objects.get(id_empleado=id)

    actualizar = True
    formularioCargas = []

    informacion_laboral = InformacionLaboral.objects.get(id_empleado=empleado)
    departamento = Departamento.objects.get(id_empleado=empleado)
    area = Area.objects.get(id_empleado=empleado)
    cargo = Cargo.objects.get(id_empleado=empleado)
    contacto_emergencia = ContactoEmergencia.objects.get(id_empleado=empleado)
    cargas_familiares = CargaFamiliar.objects.filter(id_empleado=empleado)
    cantidad_cargas = CargaFamiliar.objects.filter(id_empleado=empleado).count()

    print('cargas familiares', len(formularioCargas))

    if req.method == 'POST':
        registro = req.POST
        cantidad = int(registro.get('form_cantidad_cargas', 0))

        print(cantidad)

        empleado = Empleado.objects.get(id_empleado=id)
        # Actualizar Empleado
        empleado.nombre_empleado = registro['form_nombre_empleado']
        empleado.rut_empleado = registro['form_rut_empleado_hidden']
        empleado.genero_empleado = registro['form_genero_empleado']
        empleado.direccion_empleado = registro['form_direccion_empleado']
        empleado.telefono_empleado = registro['form_telefono_empleado']
        empleado.save()
        print("Actualizado Empleado")

        # Actualizar InformacionLaboral
        # ARREGLAR CONVERCION DE LA FECHA
        informacion_laboral = InformacionLaboral.objects.get(id_empleado=empleado)
        informacion_laboral.fecha_ingreso = registro['form_fecha_ingreso_hidden']
        # fecha_ingreso = datetime.strptime(registro['form_fecha_ingreso_hidden'], '%Y-%m-%d').date()
        # fecha_ingreso = datetime.strptime(fecha_ingreso_str, '%Y-%m-%d').date()
        informacion_laboral.save()
        print("Actualizado InformacionLaboral")

        # Actualizar Departamento
        departamento = Departamento.objects.get(id_empleado=empleado)
        departamento.nombre_departamento = registro['form_nombre_departamento_hidden']
        departamento.save()
        print("Actualizado Departamento")

        # Actualizar Area
        area = Area.objects.get(id_empleado=empleado)
        area.nombre_area = registro['form_nombre_area_hidden']
        area.save()
        print("Actualizado Area")

        # Actualizar Cargo
        cargo = Cargo.objects.get(id_empleado=empleado)
        cargo.nombre_cargo = registro['form_nombre_cargo_hidden']
        cargo.save()
        print("Actualizado Cargo")

        # Actualizar ContactoEmergencia
        contacto_emergencia = ContactoEmergencia.objects.get(id_empleado=empleado)
        contacto_emergencia.nombre_contacto = registro['form_nombre_contacto']
        contacto_emergencia.relacion_contacto = registro['form_relacion_contacto']
        contacto_emergencia.telefono_contacto = registro['form_telefono_contacto']
        contacto_emergencia.save()
        print("Actualizado ContactoEmergencia")

        # Actualizar ContactoEmpleado
        contacto_empleado = ContactoEmpleado.objects.get(id_empleado=empleado)
        contacto_empleado.id_contacto_emergencia = contacto_emergencia
        contacto_empleado.save()
        print("Actualizado ContactoEmpleado")

        # Actualizar Cargas Familiares
        for i, carga in enumerate(cargas_familiares, start=1):
            carga.nombre_carga = registro[f'form_nombre_cargaRegistrada{str(i)}']
            carga.rut_carga = registro[f'form_rut_cargaRegistrada{str(i)}_hidden']
            carga.genero_carga = registro[f'form_genero_cargaRegistrada{str(i)}']
            carga.parentesco_carga = registro[f'form_parentesco_cargaRegistrada{str(i)}']
            carga.save()
            print(f"actualizada Carga Familiar registro {i}")

        if registro.get('form_nombre_carga0') is not None:
            for i in range(cantidad):
                nueva_carga = CargaFamiliar(
                    nombre_carga=registro[f'form_nombre_carga{str(i)}'],
                    rut_carga=registro[f'form_rut_carga{str(i)}'],
                    genero_carga=registro[f'form_genero_carga{str(i)}'],
                    parentesco_carga=registro[f'form_parentesco_carga{str(i)}'],
                    id_empleado=empleado
                )
                nueva_carga.save()
                print(f"agregado nueva Carga Familiar {i}")

        return redirect(f'/empleado/verInformacion/{id}')

    else:
        print("nuevo instanciamiento de formularios")
        formularioEmpleado = forms.EmpleadoForm(instance=empleado)
        formularioLaboral = forms.InformacionLaboralForm(instance=informacion_laboral)
        formularioDepartamento = forms.DepartamentoForm(instance=departamento)
        formularioArea = forms.AreaForm(instance=area)
        formularioCargo = forms.CargoForm(instance=cargo)
        formularioContacto = forms.ContactoEmergenciaForm(instance=contacto_emergencia)
        for carga_familiar in cargas_familiares:
            formularioCargas.append(forms.CargaFamiliarForm(instance=carga_familiar))
   
    datos = {
        'formularioEmpleado': formularioEmpleado,
        'formularioLaboral': formularioLaboral,
        'formularioDepartamento': formularioDepartamento,
        'formularioArea': formularioArea,
        'formularioCargo': formularioCargo,
        'formularioContacto': formularioContacto,
        'formularioCargas': formularioCargas,
        'actualizar': actualizar,
        'cantidadCargas': cantidad_cargas,
        'empleado': empleado
    }

    return render(req, 'actualizarInformacionEmpleado.html', datos)

def filtradoEmpleados(req, id_usuario):
    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)
    # Obtener valores distintos de la base de datos
    generos_disponibles = Empleado.objects.values_list('genero_empleado', flat=True).distinct()
    cargos_disponibles = Cargo.objects.values_list('nombre_cargo', flat=True).distinct()
    areas_disponibles = Area.objects.values_list('nombre_area', flat=True).distinct()
    departamentos_disponibles = Departamento.objects.values_list('nombre_departamento', flat=True).distinct()

    if req.method == "POST":
        print(req.POST)
        # Obtener valores seleccionados por el usuario en el formulario
        genero = req.POST.get('genero')
        cargo = req.POST.get('cargo')
        area = req.POST.get('area')
        departamento = req.POST.get('departamento')

        if req.POST.get('limpiar_todo'):
            genero = None
            cargo = None
            area = None
            departamento = None

        # Filtrar empleados en base a los criterios seleccionados
        empleados = Empleado.objects.all()

        if genero:
            empleados = empleados.filter(genero_empleado=genero)
            print(empleados)

        if cargo:
            empleados = empleados.filter(cargo__nombre_cargo=cargo)

        if area:
            empleados = empleados.filter(area__nombre_area=area)

        if departamento:
            empleados = empleados.filter(departamento__nombre_departamento=departamento)

        cargos_seleccionados = Cargo.objects.filter(id_empleado__in=empleados)
    else:
        # En caso de un método GET, mostrar todos los empleados sin filtrar
        empleados = Empleado.objects.all()
        cargos_seleccionados = Cargo.objects.all()

    datos = {
        'empleado_usuario': empleado_usuario,
        'empleados': empleados,
        'cargos': cargos_seleccionados,
        'generos': generos_disponibles,
        'cargos_disponibles': cargos_disponibles,
        'areas_disponibles': areas_disponibles,
        'departamentos_disponibles': departamentos_disponibles,
    }

    return render(req, 'listarEmpleados.html', datos)

def eliminarCargaFamiliar(req, id, id_carga, id_usuario):
    empleado_usuario = Empleado.objects.get(id_empleado=id_usuario)
    empleado = Empleado.objects.get(id_empleado=id)
    carga_familiar = CargaFamiliar.objects.get(id_carga_familiar=id_carga)

    carga_familiar.delete()

    messages.success(req, f"Carga familiar de {carga_familiar.nombre_carga} eliminada exitosamente.")
    return redirect(f'/administrador/actualizar/{id}/{id_usuario}')
