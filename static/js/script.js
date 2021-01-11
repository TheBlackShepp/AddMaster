const LOCATION = document.location;
const subpath = LOCATION.pathname.split('/')[LOCATION.pathname.split('/').length -1];

const URL_DOLOGIN = 'doLogin'


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
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: data
    })

    return respone.json();
}

(function() {

    switch (subpath) {
        case 'productos':
            console.log("PRODUCTOS")
            break;
        case 'clientes':
            break;
    
        case 'pedidos':
            break;

        case 'materias':
            break;

        case 'personal':
            break;

        default:
            break;
    }

    document.getElementById(`span-${subpath}`).classList.remove('hidden');
    document.getElementById(`main-${subpath}`).classList.remove('hidden');

})();
