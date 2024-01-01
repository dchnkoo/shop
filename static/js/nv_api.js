const getInpCity = document.querySelectorAll('ul#choose-city');
const getInputCity = document.querySelectorAll('#choose-city-input');

const k = '11fcc66be04919e9b17d3744d6f7c8fc'

const cities = [];

function requestsApiCity() {
    fetch('https://api.novaposhta.ua/v2.0/json/', {
        'method' : 'POST',
        'headers' : {
            'Content-type' : 'application/json'
        },

        'body' : JSON.stringify({
            "apiKey": k,
            "modelName": "Address",
            "calledMethod": "getCities",
        })
    })
    .then(data => data.json())
    .then(obj => {
        obj.data.every(el => cities.push({city: el.Description, cityRu: el.DescriptionRu, Ref: el.Ref}))
    })
}


getInputCity.forEach(elem => {
    elem.onfocus = e => {
        requestsApiCity()
        getInpCity.forEach(el => el.style.display = 'block');
        e.target.oninput = checkInput;
    }
})



const liElements = [];
function checkInput(e) {
    
    const parent = e.target.parentElement.querySelector('ul');
    let getCityFilter = cities.filter(elem => elem.city.toLowerCase().startsWith(e.target.value.toLowerCase()) ||
                                        elem.cityRu.toLowerCase().startsWith(e.target.value.toLowerCase()))


    getCityFilter.every(elem => {
        if (!liElements.includes(elem.city)) {
            if (elem.city.toLowerCase().startsWith(e.target.value.toLowerCase())) {
                const li = document.createElement('li');
                li.setAttribute('data', elem.Ref)
                li.innerText = elem.city;

                li.onclick = showWarHouses;

                
    
                parent.append(li);
                liElements.push(elem.city);
            }
        } else {
            const arr = parent.querySelectorAll('li');
        
            arr.forEach(elem => {
                if (!elem.innerText.toLowerCase().includes(e.target.value.toLowerCase())) {
                    
                    const index = liElements.indexOf(elem.city);
                    liElements.splice(index, 1);
        
                    elem.remove()
                } else {
                    let child = parent.firstChild;

                    
                    parent.insertBefore(elem, child);
                     
                }
            })
        }
    })
}





const WarH = [];
function showWarHouses(t) {
    WarH.length = 0;
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
                        v.oninput = () => {
                            filterVidil(v)
                        };
                    }

                });
                document.querySelectorAll('#choose-vid').forEach(el => {
                    if (el.innerHTML.length > 0) {
                        el.innerHTML = '';

                    }
                    value.data.forEach(v => {    
                        if (v.Description.startsWith('Відділення') || v.Description.startsWith('Поштомат')) {
                            WarH.push(v.Description);
                        }
                    })
                });         
            }
        })
}





const inputElems = [];
function filterVidil(str) {
    if (str.value.length > 0) {
        let f = WarH.filter(elems => elems.toLowerCase().includes(str.value.toLowerCase()));
        
        
        const parent = str.parentElement.querySelector('ul');
        f.every(elem => {
            if (!inputElems.includes(elem)) {
                inputElems.push(elem)

                const li = document.createElement('li');
                li.innerHTML = elem.replace(str.value, `<span id="span" style='background: yellow;' >${str.value}</span>`);
    
                li.onclick = e => {

                    if (e.target.id === 'span') {
                        parent.parentElement.querySelector('input').value = e.target.parentElement.innerText;
                    } else {
                        parent.parentElement.querySelector('input').value = e.target.innerText;
                    }

                    parent.style.display = 'none';
                }

                parent.append(li);
            }
            parent.querySelectorAll('li').forEach(element => {
                
                if (element.innerText.toLowerCase().includes(str.value.toLowerCase())) {
                    const ch = element;

                    ch.remove();
                    
                    let child = parent.firstChild;
                    let elemTxt = element.innerText;
                    let index = elemTxt.indexOf(str.value)

                    if (index >= 0) {
                        let st = elemTxt.substring(index, index + str.value.length)
                        
                        element.innerHTML = elemTxt.replace(st, `<span id="span" style='background: yellow;' >${st}</span>`)
                    }
                    
                    parent.insertBefore(ch, child);
                } else {
                    let index = inputElems.indexOf(element.innerText);

                    inputElems.splice(index, 1);
                    element.remove();
                }
            });
        })
    }
}






function setterVid(e) {
    document.querySelectorAll("input[id='choose-vid-input']").forEach(el => {
        el.value = e.target.innerHTML;
    })
    e.target.parentElement.style.display = 'none';
}
    