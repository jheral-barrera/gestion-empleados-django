document.addEventListener("DOMContentLoaded", () => {
    const btnAgregarCarga = document.getElementById('btnAgregarCarga');
    const cargasFamiliaresContainer = document.querySelector('.cargas-familiares-container');
    const inputCantidadCargas = document.getElementById('inputCargasFamiliares');

    let indexCargaFamiliar = 0;

    btnAgregarCarga.addEventListener("click", () => {
        crearCargaFamiliarForm(indexCargaFamiliar);
        indexCargaFamiliar++;
        actualizarCantidadCargas();
    });

    cargasFamiliaresContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains('btnEliminarCarga')) {
            removerCargaFamiliar(event.target.closest('.carga-familiar'));
            indexCargaFamiliar--;
            actualizarCantidadCargas();
        }
    });

    function crearCargaFamiliarForm(index) {
        const cargaFamiliarForm = document.createElement("div");
        cargaFamiliarForm.classList.add('row', 'm-0', 'p-0', 'carga-familiar');

        cargaFamiliarForm.innerHTML = `
        <div class='row m-0 pt-3  border-top'>
            <div class="col-md-6 text-start px-0 py-3 m-0 align-self-end ">
                <h3 class='p-0 m-0 text-start'>Carga Familiar ${index} </h3>
            </div>
            <div class="col-md-6 text-start px-2 py-3 m-0 ">
                <a class="btnEliminarCarga btn btn-secondary p-2 m-0">Eliminar Carga Familiar</a>
            </div>
        </div>
        <div class='row m-0 p-0 '>
            <div class="col-md-6 text-start px-2 py-3 m-0">
                <label for="inputNombre${index}" class="form-label p-0 m-0 fw-semibold">Nombre Completo de la carga familiar</label>
                <input name='form_nombre_carga${index}' type="text" class="form-control" id="inputNombre${index}" placeholder='Ingresa el nombre completo...' required>
            </div>
            <div class="col-md-6 text-start px-2 py-3 m-0">
                <label for="inputRut${index}" class="form-label p-0 m-0 fw-semibold">Rut de la carga familiar</label>
                <input name='form_rut_carga${index}' type="text" class="form-control" id="inputRut${index}" placeholder='Ingresa el Rut (12345678-9)...' required>
            </div>
        </div>
        <div class='row m-0 p-0 '>
            <div class="col-md-6 text-start px-2 py-3 m-0">
                <label for="inputGenero${index}" class="form-label p-0 m-0 fw-semibold">Genero de la carga familiar</label>
                <select name='form_genero_carga${index}' class="form-select" id="inputGenero${index}" required>
                    <option value="" disabled selected>Selecciona el genero...</option>
                    <option value="Masculino">Masculino</option>
                    <option value="Femenino">Femenino</option>
                </select>
            </div>
            <div class="col-md-6 text-start px-2 py-3 m-0">
                <label for="inputParentesco${index}" class="form-label p-0 m-0 fw-semibold">Parentesco con el empleado</label>
                <input name='form_parentesco_carga${index}' type="text" class="form-control" id="inputParentesco${index}" placeholder='Ingresa el parentesco con el empleado...' required>
            </div>
        </div>
        `;

        cargasFamiliaresContainer.appendChild(cargaFamiliarForm);
    }

    function removerCargaFamiliar(cargaFamiliar) {
        cargasFamiliaresContainer.removeChild(cargaFamiliar);
    }

    function actualizarCantidadCargas() {
        inputCantidadCargas.value = indexCargaFamiliar;
    }
});