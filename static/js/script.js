const LOCATION = document.location;
const subpath = LOCATION.pathname.split('/')[LOCATION.pathname.split('/').length -1];

const keysProducts = ['id', 'nombre', 'cantidad', 'precio', 'fecha_inicio_venta', 'fecha_fin_venta', 'etiquetas', 'descripcion']
const keysClients = ['id', 'email', 'nombre', 'apellido', 'apellido2', 'telefono', 'edad', 'fecha_nacimiento', 'domicilio',
'sexo']
const keysOrders = ['id', 'id_cliente', 'enviar_a_domicilio', 'id_producto', 'fecha_entrega', 'fecha_compra',
'fecha_entregado']
const keysMaterials = ['id', 'tipo_materia', 'cantidad', 'registro', 'cantidad_recibida', 'fecha_llegada']
const keysPersonal = ['id', 'email', 'nombre', 'apellido', 'apellido2', 'telefono', 'edad', 'fecha_nacimiento', 'domicilio',
'sexo', 'acceso']


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
            makePost(URL_GET_LIST_PRODUCT, {})
                .then(data => {
                    console.log(data);
                    printListProducts(data.products)
                })
                .catch(err => console.error)
            break;
        case 'clientes':
            makePost(URL_GET_LIST_CLIENT, {})
                .then(data => {
                    console.log(data);
                    printListClients(data.clients)
                })
                .catch(err => console.error)
            break;
    
        case 'pedidos':
            makePost(URL_GET_LIST_ORDER, {})
                .then(data => {
                    console.log(data);
                    printListOrders(data.pedido)
                })
                .catch(err => console.error)
            break;

        case 'materias':
            makePost(URL_GET_LIST_MATERIAL, {})
            .then(data => {
                console.log(data);
                printListMaterial(data.materias)
            })
            .catch(err => console.error)
            break;

        case 'personal':
            makePost(URL_GET_LIST_PERSONAL, {})
            .then(data => {
                console.log(data);
                printListPersonal(data.users)
            })
            .catch(err => console.error)
            break;

        default:
            break;
    }

    if(subpath != '' && subpath != 'login'){
        document.getElementById(`span-${subpath}`).classList.remove('hidden');
        document.getElementById(`main-${subpath}`).classList.remove('hidden');
    }

})();

// pintar productos
const makeCardProduct = (product) => {

    let listImg = ['vino_mujercanon.jpg', 'vino_valbuena.jpg']

    return `
        <div class="max-w-md w-full lg:flex shadow cursor-pointer" onclick="viewDetailsProduct(1)">
            <div class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" title="Woman holding a mug">
            <img class="w-full h-full object-cover" src="/static/img/${listImg[Math.ceil(Math.random()*2) - 1 ]}" alt="vino">
            </div>
            <div class="bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
            <div class="mb-8">
                <div class="text-black font-bold text-xl mb-2">${product.nombre}</div>
                <p class="text-grey-darker text-base">${product.descripcion}</p>
            </div>

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
}

// pintar clientes
const makeRowClient = (client) => {

    return `
        <tr class="text-gray-700 dark:text-gray-400 cursor-pointer">
            <td class="px-4 py-3">
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
            <td class="px-4 py-3 text-sm">
            ${client.email}
            </td>
            <td class="px-4 py-3 text-sm">
            ${client.telefono}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="viewDetailsClient('client')">
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
                onclick="deleteClient('id_cliente')">
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
            <td class="px-4 py-3">
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
                <p class="font-semibold">${order.id_cliente}</p>
            </div>
            </td>
            <td class="px-4 py-3 text-sm">
            ${order.fecha_compra}
            </td>
            <td class="px-4 py-3 text-xs">
                ${domicilio}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="viewDetailsOrder('order')"
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
                onclick="deleteOrder('order')"
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
}

// pintar materias prima
const makeRowMaterial = (material) => {

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
            <td class="px-4 py-3">
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
                <p class="font-semibold">${order.id_cliente}</p>
            </div>
            </td>
            <td class="px-4 py-3 text-sm">
            ${order.fecha_compra}
            </td>
            <td class="px-4 py-3 text-xs">
                ${domicilio}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="viewDetailsOrder('order')"
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
                onclick="deleteOrder('order')"
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
            <td class="px-4 py-3">
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
            <td class="px-4 py-3 text-sm">
                ${personal.email}
            </td>
            <td class="px-4 py-3 text-xs">
                ${permision}
            </td>
            <td class="px-4 py-3 text-xs">
                ${personal.telefono}
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-${color} rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
                aria-label="Edit"
                onclick="viewDetailsPersonal(${personal.id})"
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
}


// eliminar cliente
function deleteClient(id){

    showModalDelete()
        .then((result) => {
            if (result.isConfirmed) {
            Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            )
            }
        })
}

// eliminar pedido
function deleteOrder(id){

    showModalDelete()
        .then((result) => {
            if (result.isConfirmed) {
            Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            )
            }
        })
}

// TODO show modal
function showFullModal(typeOpen) {
    const modal = document.getElementById('modal-full')
    modal.style.transform= 'translateY(6.5%)'

    if(typeOpen != undefined) {
        console.log(typeOpen)
    }

}

// TODO close modal
function closeFullModal(){
    const modal = document.getElementById('modal-full')
    modal.style.transform= 'translateY(100%)'
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

// TODO create modal
const inputGeneral = (key, value) => {
    return `
        <div class="flex flex-col m-5">
            <label class="font-medium">${key}</label>
            <input class="md:pl-6 p-2 bg-gray-300 rounded-md focus:outline-none text-gray-600 font-bold shadow" type="text" value="${value}" />
        </div>
    `
}
function createModal(object){
    const container = document.getElementById('container-modal')

    let texto = ''
    for (let key in object) {
        texto+= inputGeneral(key, object[key])
    }
    
    container.innerHTML = texto
}


// function crear producto -> FUNCIONA
function createProduct(){
    
    makePost(URL_CREATE_PRODUCT, {
        'id': 0,
        'nombre': 'Producto 1 modificado',
        'cantidad': 999,
        "precio": 100,
        'fecha_inicio_venta': '2021-01-09',
        'fecha_fin_venta': '2021-01-09',
        'etiquetas': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'],
        'descripcion': 'No hay mucho que poner en un producto ficticio'
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}


function modifyProduct(){
    
    makePost(URL_MODIFY_PRODUCT, {
        'id': 0,
        'nombre': 'Producto 1',
        'cantidad': 999,
        "precio": 100,
        'fecha_inicio_venta': '2021-01-09',
        'fecha_fin_venta': '2021-01-09',
        'etiquetas': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'],
        'descripcion': 'No hay mucho que poner en un producto ficticio'
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function get dato producto -> FUNCIONA
function getDataProduct(){
    
    makePost(URL_GET_PRODUCT, {
        'id': 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}




// function create client -> FUNCTIONA
function createClient(){

    makePost(URL_CREATE_CLIENT, {
        "id": 0,
        "email": "clienteTest1@gmail.com",
        "nombre": "Nombre Cliente",
        "apellido": "Apellido 1",
        "apellido2": "Apellido 2",
        "telefono": "666666666",
        "edad": 99,
        "fecha_nacimiento": new Date().toISOString(),
        "domicilio": "None",
        "sexo": "X"
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function modify client -> FUNCTIONA
function modifyClient(){

    makePost(URL_MODIFY_CLIENT, {
        "id": 0,
        "email": "clienteTest1@gmail.com",
        "nombre": "TU MADRE",
        "apellido": "ELLA",
        "apellido2": "Apellido 2",
        "telefono": "666666666",
        "edad": 99,
        "fecha_nacimiento": new Date().toISOString(),
        "domicilio": "None",
        "sexo": "X"
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function get data client -> FUNCTIONA
function getDataClient(){

    makePost(URL_GET_CLIENT, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function delete client -> FUNCTIONA
function deleteClient(){

    makePost(URL_DELETE_CLIENT, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}



// function create order -> FUNCIONA
function createOrder(){

    makePost(URL_CREATE_ORDER, {
        "id": 0, 
        "id_cliente": 0, 
        "enviar_a_domicilio": true, 
        "id_producto": 0, 
        "fecha_entrega": new Date().toISOString(), 
        "fecha_compra": new Date().toISOString(),
        "fecha_entregado": new Date().toISOString()
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function modify order ->  FUNCTIONA
function modifyOrder(){

    makePost(URL_MODIFY_ORDER, {
        "id": 0, 
        "id_cliente": 0, 
        "enviar_a_domicilio": false, 
        "id_producto": 0, 
        "fecha_entrega": new Date().toISOString(), 
        "fecha_compra": new Date().toISOString(),
        "fecha_entregado": new Date().toISOString()
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function get order ->  FUNCIONA
function getOrder(){

    makePost(URL_GET_ORDER, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function delete order ->  FUNCIONA
function deleteOrder(){

    makePost(URL_DELETE_ORDER, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}




// function create material ->  FUNCIONA
function createMaterial(){

    makePost(URL_CREATE_MATERIAL, {
        "id": 0,
        "tipo_materia": 0,
        "cantidad": 5,
        "registro": {'casa': 'casa'},
        "cantidad_recibida": 1,
        "fecha_llegada": new Date().toISOString()
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function get material ->  FUNCIONA
function getDataMaterial(){

    makePost(URL_GET_MATERIAL, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function delete material ->  FUNCIONA
function deleteMaterial(){

    makePost(URL_DELETE_MATERIAL, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}



// function create personal -> FUNCIONA 
function createPersonal(){

    makePost(URL_CREATE_PERSONAL, {
        "id": 0,

        "email": "me@me.es",
        "nombre": "NameSoy",
        "apellido": "Apellido 1",
        "apellido2": "Apellido 2",
        "telefono": "666666666",
        "edad": 99,
        "fecha_nacimiento": new Date().toISOString(),
        "domicilio": "None",
        "sexo": "X",
        
        "acceso": 2,
        "password": "abc123"
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function modify personal ->  FUNCIONA
function modifyPersonal(){

    makePost(URL_MODIFY_PERSONAL, {
        "id": 1,

        "email": "me@me.es",
        "nombre": "NameSoy",
        "apellido": "Apellido 1",
        "apellido2": "Apellido 2",
        "telefono": "666666666",
        "edad": 99,
        "fecha_nacimiento": new Date().toISOString(),
        "domicilio": "None",
        "sexo": "X",
        
        "acceso": 2,
        "password": "abc123"
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function get data personal ->  FUNCIONA
function getDataPersonal(){

    makePost(URL_GET_PERSONAL, {
        "id": 0
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function delete personal ->  FUNCIONA
function deletePersonal(){

    makePost(URL_DELETE_PERSONAL, {
        "id": 1
    })
        .then(data => {
            console.log(data);
            let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
            printListClients(list)
        })
        .catch(err => console.error)
}

// function imprimir pdf ->  
function imprimirPDF(){

    makePost('imprimir', {
        "id": 1
    })
        .then(data => {
            console.log(data);
        })
        .catch(err => console.error)
}
