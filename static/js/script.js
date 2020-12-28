const LOCATION = document.location;

const URL_DOLOGIN = 'doLogin'

// your page initialization code here
// the DOM will be available here

const makeGet = async(url) => {

    fetch(`${LOCATION.protocol}//${LOCATION.hostname}:${LOCATION.port}/${url}`)
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

})();

const inputFree = (listInput) => {

    if(!Array.isArray(listInput)){
        return;
    }

    for(let i = 0; i < listInput.length; i++) {
        if(listInput[i].value === '')
            return false;
    }

    return true;
}

function doLogin(){
   
    const inputUser = document.getElementById('input-login-email');
    const inputPass = document.getElementById('input-login-password');

    if(!inputFree([inputUser, inputPass])){
        console.log('Salio')
        return;    
    }

    makePost(URL_DOLOGIN, {'username': inputUser.value, 'password': inputPass.value})
        .then(data => {
            console.log(data)
            // document.write(data)
        })
        .catch(error => console.log(error))
}
