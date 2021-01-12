const LOCATION = document.location;
const subpath = LOCATION.pathname.split('/')[LOCATION.pathname.split('/').length -1];

const URL_GET_LIST_PRODUCT = 'get_lista_productos'
const URL_GET_LIST_CLIENT = 'get_lista_productos'
const URL_GET_LIST_ORDER = 'get_lista_productos'


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
                    let list = [{'name': 'Vino valhueba', 'img': 'vino_valbuena.jpg'}, {'name': 'Vino mujer cañon', 'img': 'vino_mujercanon.jpg'}]
                    printListProducts(list)
                })
                .catch(err => console.error)
            break;
        case 'clientes':
            makePost(URL_GET_LIST_CLIENT, {})
                .then(data => {
                    console.log(data);
                    let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
                    printListClients(list)
                })
                .catch(err => console.error)
            break;
    
        case 'pedidos':
            makePost(URL_GET_LIST_ORDER, {})
                .then(data => {
                    console.log(data);
                    let list = [{'name': 'Martina Casas'}, {'name': 'Marcos Martin'}]
                    printListOrders(list)
                })
                .catch(err => console.error)
            break;

        case 'materias':
            break;

        case 'personal':
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
    return `
        <div class="max-w-md w-full lg:flex shadow cursor-pointer" onclick="viewDetailsProduct(1)">
            <div class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" title="Woman holding a mug">
            <img class="w-full h-full object-cover" src="/static/img/${product.img}" alt="vino">
            </div>
            <div class="bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
            <div class="mb-8">
                <div class="text-black font-bold text-xl mb-2">${product.name}</div>
                <p class="text-grey-darker text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
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
        <tr class="text-gray-700 dark:text-gray-400">
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
                <p class="font-semibold">${client.name}</p>
                </div>
            </div>
            </td>
            <td class="px-4 py-3 text-sm">
            $ 863.45
            </td>
            <td class="px-4 py-3 text-sm">
            6/10/2020
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
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
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
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

    return `
        <tr class="text-gray-700 dark:text-gray-400">
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
                <p class="font-semibold">Hans Burger</p>
                <p class="text-xs text-gray-600 dark:text-gray-400">
                    10x Developer
                </p>
                </div>
            </div>
            </td>
            <td class="px-4 py-3 text-sm">
            $ 863.45
            </td>
            <td class="px-4 py-3 text-xs">
            <span
                class="px-2 py-1 font-semibold leading-tight text-green-700 bg-green-100 rounded-full dark:bg-green-700 dark:text-green-100"
            >
                Approved
            </span>
            </td>
            <td class="px-4 py-3 text-sm">
            6/10/2020
            </td>
            <td class="px-4 py-3">
            <div class="flex items-center space-x-4 text-sm">
                <button
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
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
                class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
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

// view details product
function viewDetailsProduct(id){
    console.log(id)
    showFullModal()
}

// view detail client
function viewDetailsClient(id){
    console.log(id)
    showFullModal()
}

// view detail order
function viewDetailsOrder(id){
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
function showFullModal() {
    const modal = document.getElementById('modal-full')
    modal.style.transform= 'translateY(6.5%)'
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