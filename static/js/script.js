const LOCATION = document.location;
const subpath = LOCATION.pathname.split('/')[LOCATION.pathname.split('/').length -1];

let keysProducts = []
let keysClients = []
let keysOrders = []
let keysMaterials = []
let keysPersonal = []


const URL_GET_LIST_PRODUCT = 'get_lista_productos'
const URL_GET_LIST_CLIENT = 'get_lista_clientes'
const URL_GET_LIST_ORDER = 'get_lista_pedidos'
const URL_GET_LIST_MATERIAL = 'get_lista_materias_primas'
const URL_GET_LIST_PERSONAL = 'get_lista_usuarios'


// product
const URL_CREATE_PRODUCT = 'igresar_datos_producto'
const URL_MODIFY_PRODUCT = 'modificar_datos_producto'
const URL_GET_PRODUCT = 'get_datos_producto'

// client
const URL_CREATE_CLIENT= 'dar_alta_cliente'
const URL_MODIFY_CLIENT= 'modificar_datos_cliente'
const URL_GET_CLIENT= 'get_datos_cliente'
const URL_DELETE_CLIENT= 'dar_baja_cliente'

// order
const URL_CREATE_ORDER= 'igresar_datos_pedido'
const URL_MODIFY_ORDER= 'modificar_datos_pedido'
const URL_GET_ORDER= 'get_datos_pedido'
const URL_DELETE_ORDER= 'eliminar_pedido'

// material
const URL_CREATE_MATERIAL= 'igresar_datos_materia_prima'
const URL_GET_MATERIAL= 'get_datos_materia_prima'
const URL_DELETE_MATERIAL= 'eliminar_meteria_prima'

// personal
const URL_CREATE_PERSONAL= 'ingresar_usuario'
const URL_GET_PERSONAL= 'get_datos_usuario'
const URL_DELETE_PERSONAL= 'eliminar_usuario'
const URL_MODIFY_PERSONAL= 'modificar_usuario'

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })
  

const makeGet = async(url) => {

    const response = fetch(`${LOCATION.protocol}//${LOCATION.hostname}:${LOCATION.port}/${url}`);

    return response.json();
}

const makePost = async(url, datos) => {

    const data = new FormData();
    Object.entries(datos).forEach(([key, value]) => {
        data.append(key, value);
    });

    const respone = await fetch(`${LOCATION.protocol}//${LOCATION.hostname}:${LOCATION.port}/${url}`, {
        method: 'POST',
        // headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: data
    })

    return respone.json();
}

(function() {

    switch (subpath) {
        case 'productos':
            console.log("PRODUCTOS")
            get_productos()
            break;

        case 'clientes':
            get_clientes()
            break;

        case 'pedidos':
            get_productos()
            get_clientes()
            break;

        case 'materias':
            get_materias()
            break;

        case 'personal':
            get_personal()
            break;

        default:
            break;
    }

    if(subpath != '' && subpath != 'login'){
        document.getElementById(`span-${subpath}`).classList.remove('hidden');
        document.getElementById(`main-${subpath}`).classList.remove('hidden');
    }

})();

function get_productos(){
    makePost(URL_GET_LIST_PRODUCT, {})
    .then(data => {
        console.log(data);
        printListProducts(data.products)
    })
    .catch(err => console.error)
}
function get_clientes(){
    makePost(URL_GET_LIST_CLIENT, {})
    .then(data => {
        console.log(data);
        printListClients(data.clients)
        get_pedidos();
    })
    .catch(err => console.error)
}
function get_pedidos(){
    makePost(URL_GET_LIST_ORDER, {})
        .then(data => {
            console.log(data);
            printListOrders(data.pedido)
        })
        .catch(err => console.error)
}
function get_materias(){
    makePost(URL_GET_LIST_MATERIAL, {})
    .then(data => {
        console.log(data);
        printListMaterial(data.materias)
    })
    .catch(err => console.error)
}
function get_personal(){
    makePost(URL_GET_LIST_PERSONAL, {})
        .then(data => {
            console.log(data);
            printListPersonal(data.users)
        })
        .catch(err => console.error)
}

// pintar productos
const makeCardProduct = (product) => {

    let listImg = ['vino_mujercanon.jpg', 'vino_valbuena.jpg']

    return `
        <div class="max-w-md w-full lg:flex shadow cursor-pointer">
            <div class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" title="Woman holding a mug" onclick="getDataProduct(${product.id})">
            <img class="w-full h-full object-cover" src="/static/img/${listImg[Math.ceil(Math.random()*2) - 1 ]}" alt="vino">
            </div>
            <div class="bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
            <div class="mb-8 h-full" onclick="getDataProduct(${product.id})">
                <div class="text-black font-bold text-xl mb-2">${product.nombre}</div>
                <p class="text-grey-darker text-base">${product.descripcion}</p>
            </div>
            <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 bg-${color} text-white rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="showFullModal('modify-product',${product.id})"
                >
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
                    ></path>
                </svg>
                    <div class="w-full">
                        Modificar
                    </div>
                </button>
            </div>
        </div>
    `
}
function printListProducts(listProducts){

    const container = document.getElementById('container-productos');

    let text = ''
    listProducts.forEach(product => {
        text+= makeCardProduct(product);
    })

    container.innerHTML = text;
    keysProducts= listProducts;

    let option=''
    keysProducts.forEach(client => {
        option+=`<option value="${client.id}">${client.nombre}</option>`
    })

    document.getElementById('modal-order-id_producto').innerHTML= option;
}

// pintar clientes
const makeRowClient = (client) => {
    
    return `
        <tr class="text-gray-700 dark:text-gray-400 cursor-pointer">
            <td class="px-4 py-3" onclick="getDataClient(${client.id})">
            <div class="flex items-center text-sm">
                <!-- Avatar with inset shadow -->
                <div
                class="relative hidden w-8 h-8 mr-3 rounded-full md:block"
                >
                <img
                    class="object-cover w-full h-full rounded-full"
                    src="https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&ixid=eyJhcHBfaWQiOjE3Nzg0fQ"
                    alt=""
                    loading="lazy"
                />
                <div
                    class="absolute inset-0 rounded-full shadow-inner"
                    aria-hidden="true"
                ></div>
                </div>
                <div>
                <p class="font-semibold">${client.nombre} ${client.apellido}</p>
                </div>
            </div>
            </td>
            <td class="px-4 py-3 text-sm" onclick="getDataClient(${client.id})">
            ${client.email}
            </td>
            <td class="px-4 py-3 text-sm" onclick="getDataClient(${client.id})">
            ${client.telefono}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="showFullModal('modify-client',${client.id})">
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
                    ></path>
                </svg>
                </button>
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Delete"
                onclick="deleteClient(${client.id})">
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                    ></path>
                </svg>
                </button>
            </div>
            </td>
        </tr>
    `

}
function printListClients(listClients){
    const container = document.getElementById('container-clients');

    let text = ''
    listClients.forEach(client => {
        text+= makeRowClient(client);
    })

    container.innerHTML = text;
    keysClients= listClients;

    let option=''
    keysClients.forEach(client => {
        option+=`<option value="${client.id}">${client.nombre}</option>`
    })
    document.getElementById('modal-order-id_cliente').innerHTML= option;
}

// pintar pedidos
const makeRowOrder = (order) => {

    let domicilio = ''
    if(order.enviar_a_domicilio){
        domicilio = ` <span class="px-7 py-1 font-semibold leading-tight text-green-700 bg-green-100 rounded-full dark:bg-green-700 dark:text-green-100" >
            si
        </span>`
    }else{
        domicilio = ` <span class="px-7 py-1 font-semibold leading-tight text-gray-700 bg-gray-100 rounded-full dark:bg-green-700 dark:text-green-100" >
        no
    </span>`
    }

    return `
        <tr class="text-gray-700 dark:text-gray-400 cursor-pointer">
            <td class="px-4 py-3 text-sm" onclick="getDataOrder(${order.id})">
                ${order.id}
            </td>
            <td class="px-4 py-3" onclick="getDataOrder(${order.id})">
            <div class="flex items-center text-sm">
                <!-- Avatar with inset shadow -->
              
                <p class="font-semibold">${keysClients.filter(clien => clien.id === order.id_cliente)[0].nombre}</p>
            </div>
            </td>
            <td class="px-4 py-3 text-sm" onclick="getDataOrder(${order.id})">
                ${order.fecha_compra}
            </td>
            <td class="px-4 py-3 text-xs" onclick="getDataOrder(${order.id})">
                ${domicilio}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="showFullModal('modify-order',${order.id})"
                >
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
                    ></path>
                </svg>
                </button>
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Delete"
                onclick="deleteOrder(${order.id})"
                >
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                    ></path>
                </svg>
                </button>
            </div>
            </td>
        </tr>
    `
}
function printListOrders(listOrders){
    const container = document.getElementById('container-orders');

    let text = ''
    listOrders.forEach(order => {
        text+= makeRowOrder(order);
    })

    container.innerHTML = text; 
    keysOrders= listOrders;
}

// pintar materias prima
const makeRowMaterial = (material) => {

    return `
        <tr class="text-gray-700 dark:text-gray-400 cursor-pointer">
            <td class="px-4 py-3" onclick="getDataMaterial(${material.id})">
            <div class="flex items-center text-sm">
                
                <p class="font-semibold">${material.tipo_materia}</p>
            </div>
            </td>
            <td class="px-4 py-3 text-sm" onclick="getDataMaterial(${material.id})">
                ${material.cantidad}
            </td>
            <td class="px-4 py-3 text-xs" onclick="getDataMaterial(${material.id})">
                ${material.fecha_llegada}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Delete"
                onclick="deleteMaterial(${material.id})"
                >
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                    ></path>
                </svg>
                </button>
            </div>
            </td>
        </tr>
    `
}
function printListMaterial(listMaterial) {
    const container = document.getElementById('container-material');

    let text = ''
    listMaterial.forEach(order => {
        text+= makeRowMaterial(order);
    })

    container.innerHTML = text; 
}

// pintar usuarios
const makeRowPersonal = (personal) => {

    let permision= ''
    switch (personal.acceso) {
        case 0:
            permision='Dolores';
            break;
        case 1:
            permision= 'Personal';
            break;
        case 2:
            permision = 'Administrador';
            break;
    }
    permision = `<span class="px-7 py-1 font-semibold leading-tight text-green-700 bg-green-100 rounded-full dark:bg-green-700 dark:text-green-100" >
        ${permision}
    </span>`

    return `
        <tr class="text-gray-700 dark:text-gray-400 cursor-pointer">
            <td class="px-4 py-3" onclick="getDataPersonal(${personal.id})">
            <div class="flex items-center text-sm">
                <!-- Avatar with inset shadow -->
                <div
                class="relative hidden w-8 h-8 mr-3 rounded-full md:block"
                >
                <img
                    class="object-cover w-full h-full rounded-full"
                    src="https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&ixid=eyJhcHBfaWQiOjE3Nzg0fQ"
                    alt=""
                    loading="lazy"
                />
                <div
                    class="absolute inset-0 rounded-full shadow-inner"
                    aria-hidden="true"
                ></div>
                </div>
                <div>
                <p class="font-semibold">${personal.nombre} ${personal.apellido}</p>
            </div>
            </td>
            <td class="px-4 py-3 text-sm" onclick="getDataPersonal(${personal.id})">
                ${personal.email}
            </td>
            <td class="px-4 py-3 text-xs" onclick="getDataPersonal(${personal.id})">
                ${permision}
            </td>
            <td class="px-4 py-3 text-xs" onclick="getDataPersonal(${personal.id})">
                ${personal.telefono}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="showFullModal('modify-personal',${personal.id})"
                >
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
                    ></path>
                </svg>
                </button>
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Delete"
                onclick="deletePersonal(${personal.id})"
                >
                <svg
                    class="w-5 h-5"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                    ></path>
                </svg>
                </button>
            </div>
            </td>
        </tr>
    `
}
function printListPersonal(listPersonal) {
    const container = document.getElementById('container-personal');

    let text = ''
    listPersonal.forEach(order => {
        text+= makeRowPersonal(order);
    })

    container.innerHTML = text; 
    keysPersonal= listPersonal;
}



// view details product
function viewDetailsProduct(id){
    console.log(id)
    showFullModal()
    let o = {'name': 'Marcos Martin', 'description': 'adadadad'}
    createModal(o)
}

// view detail client
function viewDetailsClient(id){
    console.log(id)
    showFullModal()
    let o = {'name': 'Marcos Martin', 'description': 'adadadad'}
    createModal(o)
}

// view detail order
function viewDetailsOrder(id){
    console.log(id)
    showFullModal()

    let o = {'name': 'Marcos Martin', 'description': 'adadadad'}
    createModal(o)
}

// view detail personal
function viewDetailsPersonal(id){
    console.log(id)
    showFullModal()
    createModal
}


// eliminar personal
function deletePersonal(id){

    console.log(id)

    showModalDelete()
        .then((result) => {
            if (result.isConfirmed) {
                eliminarPersonal(id)
            }
        })
}

// TODO show modal
function showFullModal(typeOpen, data, modi) {
    const btnSave = document.getElementById('save-modal')
    const modal = document.getElementById('modal-full')
    modal.style.transform= 'translateY(6.5%)'

    if(typeOpen != undefined) {
        let type= typeOpen.split('-')[0];
        const list= typeOpen.split('-')[1]
        let datosPasar = data

        const tileModal = document.getElementById('title-modal')
        switch(type){
            case 'get':
                if(modi){
                    type= modi;
                    tileModal.innerHTML= `Modificar ${data.nombre ? data.nombre : data.id}`
                }else
                    tileModal.innerHTML= data.nombre ? data.nombre : data.id;

                    if(list=== 'order'){
                        document.getElementById('imprimir-pdf').classList.remove('hidden');
                        document.getElementById('imprimir-pdf').setAttribute('onclick', `imprimirPDF(${data.id})`)                       
                    }
                break;
            case 'create':
                btnSave.classList.remove('hidden')
                switch(list){
                    case 'product':
                        btnSave.setAttribute('onclick', 'createProduct()')
                        tileModal.innerHTML= 'Crear Producto';
                        break;
                    case 'client':
                        btnSave.setAttribute('onclick', 'createClient()')
                        tileModal.innerHTML= 'Crear Cliente';
                        break;
                    case 'order':
                        btnSave.setAttribute('onclick', 'createOrder()')
                        tileModal.innerHTML= 'Crear Pedido';
                        break;
                    case 'material':
                        btnSave.setAttribute('onclick', 'createMaterial()')
                        tileModal.innerHTML= 'Crear Materia Prima';
                        break;
                    case 'personal':
                        btnSave.setAttribute('onclick', 'createPersonal()')
                        tileModal.innerHTML= 'Crear Personal';
                        break;
                }
                break;
            case 'modify':
                btnSave.classList.remove('hidden')
                switch(list){
                    case 'product':
                        btnSave.setAttribute('onclick', `modifyProduct(${data})`)
                        getDataProduct(data, 'modify');
                        break;
                    case 'client':  
                        btnSave.setAttribute('onclick', `modifyClient(${data})`)
                        getDataClient(data, 'modify');
                        break;
                    case 'order':  
                        btnSave.setAttribute('onclick', `modifyOrder(${data})`)
                        getDataOrder(data, 'modify');
                        break;
                    case 'personal':
                        btnSave.setAttribute('onclick', `modifyPersonal(${data})`)
                        getDataPersonal(data, 'modify');
                        break;
                }
                return;
        }
        
        document.getElementById('close-btn-modal').setAttribute('onclick', `closeFullModal('${list}')`)
        createModal({type, 'use': list, data})
    }

}

// TODO close modal
function closeFullModal(use){
    const modal = document.getElementById('modal-full')
    modal.style.transform= 'translateY(100%)'

    const container = document.getElementById(`modal-${use}`)
    container.classList.add('hidden')

    document.getElementById('save-modal').classList.add('hidden')
    document.getElementById('imprimir-pdf').classList.add('hidden');

    document.querySelectorAll('.marca').forEach(element => {
        element.disabled = false
        element.value= ''
        element.classList.remove('marca')
    })
}

// TODO show swal
function showModalDelete(){
    return Swal.fire({
        title: '¿Estas seguro?',
        text: "Esta accion no se podra revertir!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, eliminarlo'
      })
}

function createModal(object){
    const container = document.getElementById(`modal-${object.use}`)
    container.classList.remove('hidden')
    
    if(object.type === 'create'){
        container.querySelectorAll('input').forEach(element => {
            element.classList.add('marca')
        })
        container.querySelectorAll('select').forEach(element => {
            element.classList.add('marca')
        })
        container.querySelectorAll('textarea').forEach(element => {
            element.classList.add('marca')
        })
    }

    let input = ''
    for(let key in object.data) {
        try{
            input = document.getElementById(`modal-${object.use}-${key}`)
           
            if(input){
                input.value = object.data[key]
                if(object.type === 'get'){
                    input.disabled = true
                }
                input.classList.add('marca')
            }
        }catch(error){
            console.error(error)
        }
    }

}


// function crear producto -> FUNCIONA
function createProduct(){
    
    let listValue = {}
    document.querySelectorAll('.marca').forEach(input => {

        let i = input.id.split('-')
        let key = i[i.length - 1]
        
        if(key === 'etiquetas'){
            listValue[ key ] = input.value.split(',')
        }else
            listValue[ key ] = input.value
       
    })
   
    if(inputFree(listValue))
        makePost(URL_CREATE_PRODUCT, {
            'id': 0,
            'nombre': listValue.nombre,
            'cantidad': listValue.cantidad,
            "precio": listValue.precio,
            'fecha_inicio_venta': listValue.fecha_inicio_venta,
            'fecha_fin_venta': listValue.fecha_fin_venta,
            'etiquetas': listValue.etiquetas,
            'descripcion': listValue.descripcion,
        })
            .then(data => {
                console.log(data);
                get_productos()
                closeFullModal('product')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        }) 
}

// FUNCIONA
function modifyProduct(id){
    
    console.log(id)
    let listValue= {}

    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })

    console.log(listValue)

    if(inputFree(listValue))
        makePost(URL_MODIFY_PRODUCT, {
            id,
            'nombre': listValue.nombre,
            'cantidad': listValue.cantidad,
            "precio": listValue.precio,
            'fecha_inicio_venta': listValue.fecha_inicio_venta,
            'fecha_fin_venta': listValue.fecha_fin_venta,
            'etiquetas': listValue.etiquetas,
            'descripcion': listValue.descripcion,
        })
            .then(data => {
                console.log(data);
                get_productos()
                closeFullModal('product')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function get dato producto -> FUNCIONA
function getDataProduct(id, modify){
    
    makePost(URL_GET_PRODUCT, {
        id
    })
        .then(data => {
            console.log(data);
            showFullModal('get-product', data, modify)
        })
        .catch(err => console.error)
}


// function create client -> FUNCTIONA
function createClient(){

    let listValue = {}
    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })

    console.log(listValue)

    if(inputFree(listValue))
        makePost(URL_CREATE_CLIENT, {
            "id": 0,
            "email": listValue.email,
            "nombre": listValue.nombre,
            "apellido": listValue.apellido,
            "apellido2": "Apellido 2",
            "telefono": listValue.telefono,
            "edad": listValue.edad,
            "fecha_nacimiento": listValue.fecha_nacimiento,
            "domicilio": listValue.domicilio,
            "sexo": listValue.sexo,
        })
            .then(data => {
                console.log(data);
                get_clientes()
                closeFullModal('client')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function modify client -> FUNCTIONA
function modifyClient(id){

    console.log(id)
    let listValue= {}

    let listOrigin = keysClients.filter(key => key.id == id);
    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })

    console.log(listValue)

    if(inputFree(listValue))
        makePost(URL_MODIFY_CLIENT, {
            id,
            "email": listValue.email,
            "nombre": listValue.nombre,
            "apellido": listValue.apellido,
            "apellido2": "Apellido 2",
            "telefono": listValue.telefono,
            "edad": listValue.edad,
            "fecha_nacimiento": listValue.fecha_nacimiento,
            "domicilio": listValue.domicilio,
            "sexo": listValue.sexo
        })
            .then(data => {
                console.log(data);
                get_clientes()
                closeFullModal('client')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function get data client -> FUNCTIONA
function getDataClient(id, modify){

    makePost(URL_GET_CLIENT, {
        id
    })
        .then(data => {
            console.log(data);
            showFullModal('get-client', data, modify)
        })
        .catch(err => console.error)
}

// function delete client -> FUNCTIONA
function deleteClient(id){

    showModalDelete()
        .then((result) => {
            if (result.isConfirmed) {
               
                makePost(URL_DELETE_CLIENT, {
                    "id": id
                })
                .then(data => {
                    
                    console.log(data);
                    
                    const clien = keysClients.filter(per => per.id === id)[0]
    
                    if(data.params && data.post_result){
                        printListClients(keysClients.filter(clien => clien.id != id))
                        Swal.fire(
                            'Ha sido eliminado!',
                            `${clien.nombre} ha sido eliminado`,
                            'success'
                        )
                    } else{
                        Swal.fire(
                            'Ha ocurrido un error',
                            `No se ha podido eliminar a ${clien.nombre}`,
                            'warning'
                        )
                    }
                })
                .catch(err => console.error)

            }
        })
        
}



// function create order -> FUNCIONA
function createOrder(){

    let listValue = {}
    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })

    console.log(listValue)

    let c = {
        "id": 0, 
        "id_cliente": listValue.id_cliente, 
        "enviar_a_domicilio": listValue.enviar_a_domicilio === "true" ? true : false, 
        "id_producto": listValue.id_producto, 
        "fecha_entrega": listValue.fecha_entrega, 
        "fecha_compra": listValue.fecha_compra,
        "fecha_entregado": listValue.fecha_entregado
    }

    console.log('HOLA', c)

    if(inputFree(listValue))
        makePost(URL_CREATE_ORDER, c)
            .then(data => {
                console.log(data);
                get_pedidos()
                closeFullModal('order')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function modify order ->  FUNCTIONA
function modifyOrder(id){

    console.log(id)
    let listValue= {}

    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })

    console.log(listValue)

    if(inputFree(listValue))
        makePost(URL_MODIFY_ORDER, {
            id,
            "id_cliente": listValue.id_cliente, 
            "enviar_a_domicilio": listValue.enviar_a_domicilio === "true" ? true : false, 
            "id_producto": listValue.id_producto, 
            "fecha_entrega": listValue.fecha_entrega, 
            "fecha_compra": listValue.fecha_compra,
            "fecha_entregado": listValue.fecha_entregado
        })
            .then(data => {
                console.log(data);
                get_pedidos()
                closeFullModal('order')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function get order ->  FUNCIONA
function getDataOrder(id, modify){

    makePost(URL_GET_ORDER, {
        id
    })
        .then(data => {
            console.log(data);
            showFullModal('get-order', data, modify)
        })
        .catch(err => console.error)
}

// function delete order ->  FUNCIONA
function deleteOrder(id){

    showModalDelete()
    .then((result) => {
        if (result.isConfirmed) {
            makePost(URL_DELETE_ORDER, {
                id
            })
                .then(data => {
                    console.log(data);
                    
                    const orid = keysOrders.filter(per => per.id === id)[0]
    
                    if(data.params && data.post_result){
                        printListClients(keysOrders.filter(clien => clien.id != id))
                        Swal.fire(
                            'Ha sido eliminado!',
                            `${orid.id} ha sido eliminado`,
                            'success'
                        )
                    } else{
                        Swal.fire(
                            'Ha ocurrido un error',
                            `No se ha podido eliminar a ${orid.id}`,
                            'warning'
                        )
                    }

                })
                .catch(err => console.error)
        }
    })

}


// function create material ->  FUNCIONA
function createMaterial(){

    let listValue = {}
    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })

    console.log(listValue)

    if(inputFree(listValue))
        makePost(URL_CREATE_MATERIAL, {
            "id": 0,
            "tipo_materia": listValue.tipo_materia,
            "cantidad": listValue.cantidad,
            "registro": {'casa': 'casa'},
            "cantidad_recibida": listValue.cantidad_recibida,
            "fecha_llegada": listValue.fecha_llegada
        })
            .then(data => {
                console.log(data);
                get_materias()
                closeFullModal('material')
            })
            .catch(err => console.error)
    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function get material ->  FUNCIONA
function getDataMaterial(id, modify){

    makePost(URL_GET_MATERIAL, {
        id
    })
        .then(data => {
            console.log(data);
            showFullModal('get-material', data, modify)
        })
        .catch(err => console.error)
}

// function delete material ->  FUNCIONA
function deleteMaterial(id){

    showModalDelete()
        .then((result) => {
        if (result.isConfirmed) {

            makePost(URL_DELETE_MATERIAL, {
                id
            })
                .then(data => {
                    console.log(data);
                    const mat = keysMaterials.filter(per => per.id === id)[0]
    
                    if(data.params && data.post_result){
                        get_materias()
                        Swal.fire(
                            'Ha sido eliminado!',
                            `${mat.nombre} ha sido eliminado`,
                            'success'
                        )
                    } else{
                        Swal.fire(
                            'Ha ocurrido un error',
                            `No se ha podido eliminar a ${mat.nombre}`,
                            'warning'
                        )
                    }
                })
                .catch(err => console.error)

        }
    })
}



// function create personal -> FUNCIONA 
function createPersonal(){

    let listValue = {}
    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })
  
    if(inputFree(listValue))

        Swal.fire({
            title: "Escribe la contraseña para este usuario",
            input: "text",
            showCancelButton: true,
            confirmButtonText: "Guardar",
            cancelButtonText: "Cancelar",
        })
        .then(resultado => {
            if (resultado.value) {
            listValue.password = resultado.value;

                const jsonSend = {
                    "id": 0,
            
                    "email": listValue.email,
                    "nombre": listValue.nombre,
                    "apellido": listValue.apellido,
                    "apellido2": listValue.apellido,
                    "telefono": listValue.telefono,
                    "edad": listValue.edad,
                    "fecha_nacimiento": listValue.fecha_nacimiento,
                    "domicilio": "None",
                    "sexo": listValue.sexo,
                    
                    "acceso": listValue.acceso,
                    "password": listValue.password
                }
                
                console.log(jsonSend)

                
            makePost(URL_CREATE_PERSONAL, jsonSend)
                .then(data => {
                    console.log(data);
                    get_personal()
                    closeFullModal('personal')
                })
                .catch(err => console.error)
            }
        });

    else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
    
}

// function modify personal ->  
function modifyPersonal(id){

    let listValue= {}
    let listOrigin = keysPersonal.filter(key => key.id == id);

    document.querySelectorAll('.marca').forEach(input => {
        let i = input.id.split('-')
        listValue[ i[i.length - 1] ] = input.value
    })
    

    if(inputFree(listValue)){
        makePost(URL_MODIFY_PERSONAL, {
            "id": id,

            "email": listValue.email,
            "nombre": listValue.nombre,
            "apellido": listValue.apellido,
            "apellido2": "Apellido 2",
            "telefono": listValue.telefono,
            "edad": listValue.edad,
            "fecha_nacimiento": listValue.fecha_nacimiento,
            "domicilio": "None",
            "sexo": listValue.sexo,
            
            "acceso": listValue.acceso,
            "password": ''
        })
            .then(data => {
                console.log(data);
                get_personal()
                closeFullModal('personal');
            })
            .catch(err => console.error)
    }else
        Toast.fire({
            icon: 'error',
            title: 'No puedes dejar ningun campo vacio'
        })
}

// function get data personal ->  
function getDataPersonal(id, modify){

    makePost(URL_GET_PERSONAL, {
        id
    })
        .then(data => {
            console.log(data);
            showFullModal('get-personal', data, modify)
        })
        .catch(err => console.error)
}

// function delete personal ->  FUNCIONA
function eliminarPersonal(id){

    makePost(URL_DELETE_PERSONAL, {
        id
    })
        .then(data => {
            
            const perso = keysPersonal.filter(per => per.id === id)[0]

            if(data.params && data.post_result){
                printListPersonal(keysPersonal.filter(per => per.id != id))
                Swal.fire(
                    'Ha sido eliminado!',
                    `${perso.nombre} ha sido eliminado`,
                    'success'
                )
            } else{
                Swal.fire(
                    'Ha ocurrido un error',
                    `No se ha podido eliminar a ${perso.nombre}`,
                    'warning'
                )
            }
        })
        .catch(err => console.error)
}

// function imprimir pdf ->  
function imprimirPDF(id){

    makePost('imprimir', {
        id
    })
        .then(data => {
            console.log(data);
            window.location= `${LOCATION.protocol}//${LOCATION.hostname}:${LOCATION.port}/getFile/${data.pdfname}`
        })
        .catch(err => console.error)
}

function inputFree(object){
    for(let i in object){
        if(object[i]=== ''){
            return false;
        }
    }
    return true;
}