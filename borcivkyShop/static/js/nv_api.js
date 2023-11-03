const getInpCity = document.querySelectorAll('ul#choose-city');
const getInputCity = document.querySelectorAll('#choose-city-input');
let interval;

const k = '11fcc66be04919e9b17d3744d6f7c8fc'
const keys = [32, 17, 13, 8, 18, 91, 16, 20, 9];

function requestsApiCity(e) {
    if (!keys.includes(e.which)) {
        fetch('https://api.novaposhta.ua/v2.0/json/', {
            'method' : 'POST',
            'headers' : {
                'Content-type' : 'application/json'
            },
    
            'body' : JSON.stringify({
                "apiKey": k,
                "modelName": "Address",
                "calledMethod": "getCities",
                "methodProperties": {
                    "FindByString" : e.value,
                    "Limit" : "1"
                }
            })
        })
        .then(data => data.json())
        .then(obj => {
            obj.data.every(value => {
                if (value.Description.toLowerCase().startsWith(e.value.toLowerCase()) && value.SettlementTypeDescription !== 'село') {
                    getInpCity.forEach(el => {
                        let li = document.createElement('li');
                        li.setAttribute('data', value.Ref);
                        li.setAttribute('id', 'city');
                        li.addEventListener('click', showWarHouses);
                        li.innerText = value.Description;

                        el.appendChild(li)
                    })
                }
            })
        })
    }
} 

getInputCity.forEach(elem => {
    elem.onfocus = e => {
        getInpCity.forEach(el => el.style.display = 'block');
        e.target.onkeydown = wrapper;
    }
})

function wrapper(цяХуйня) {
    let сюди = цяХуйня.target;

    requestsApiCity(сюди);
    checkInput(сюди);
}


function checkInput(e) {
    document.querySelectorAll("#"+document.querySelector('#'+e.id + ' + ul').id).forEach(el => {
        Array.from(el.getElementsByTagName('li')).find(element => {
           if (element.innerHTML.toLowerCase().includes(e.value.toLowerCase())) {
                el.getElementsByTagName('li')[0].before(element)
           } 
        }) 
    })
}


function showWarHouses(t) {
    clearInterval(interval)
    getInpCity.forEach(e => e.style.display = 'none');
    getInputCity.forEach(e => e.value = t.target.innerHTML)

    fetch('https://api.novaposhta.ua/v2.0/json/', {
            'method' : 'POST',
            'headers' : {
                'Content-type' : 'application/json'
            },
            'body' : JSON.stringify({
                "apiKey": k,
                "modelName": "Address",
                "calledMethod": "getWarehouses",
                "methodProperties" : {
                    'CityRef' : t.target.getAttribute('data'),
                }
                    
            })
        })
        .then(data => data.json())
        .then(value => {
            if (value.data.length > 0) {
                document.querySelectorAll("input[id='choose-vid-input']").forEach(v => {
                    v.style.display = 'block';
                    v.onfocus = () => {
                        document.querySelectorAll('#choose-vid').forEach(e => e.style.display = 'block');
                        v.onkeydown = () => {
                            checkInput(v)
                        };
                    }

                });
                document.querySelectorAll('#choose-vid').forEach(el => {
                    if (el.innerHTML.length > 0) {
                        el.innerHTML = '';

                    }
                    value.data.forEach(v => {    
                        if (v.Description.startsWith('Відділення') || v.Description.startsWith('Поштомат')) {
                            let elem = document.createElement('li');
                            elem.addEventListener('click', setterVid);
                            elem.innerHTML = v.Description;

                            el.appendChild(elem);
                        }
                    })

                });
                
            }
        })

}   

function setterVid(e) {
    document.querySelectorAll("input[id='choose-vid-input']").forEach(el => {
        el.value = e.target.innerHTML;
    })
    e.target.parentElement.style.display = 'none';
}
    