const getInp = document.querySelector('datalist#choose-city');
const getInput = document.querySelector('#choose-city-input');

const dataObl = {
        "apiKey": "11fcc66be04919e9b17d3744d6f7c8fc",
        "modelName": "Address",
        "calledMethod": "getSettlements",
}

const oblObj = {
    'method' : 'POST',
    'headers' : {
        'Content-type' : 'application/json'
    },
    'body' : JSON.stringify(dataObl)
}

const getCities = {
    "apiKey": "11fcc66be04919e9b17d3744d6f7c8fc",
    "modelName": "Address",
    "calledMethod": "getCities",
    "methodProperties": { "FindByString": "", "Limit" : '10' }
}




fetch('https://api.novaposhta.ua/v2.0/json/', oblObj)
.then(data => data.json())
.then(d => {
    d.data.forEach(element => {
        let option = document.createElement('option');
        option.value = element.AreaDescription;

        getInp.appendChild(option);
    });

})

getInput.onkeydown = e => {
    let gIn = getInput.value;
    getCities.methodProperties.FindByString = gIn;

    fetch('https://api.novaposhta.ua/v2.0/json/', {
        'method' : 'POST',
        'headers' : {
            'Content-type' : 'application/json'
        },
        'body' : JSON.stringify(getCities)
    })
    .then(data => data.json())
    .then(d => {
        const getInp = document.querySelector('datalist#choose-city');

        d.data.map(e => {
            console.log(e.Description.toLowerCase().substring(0, gIn.length))
            if (e.Description.toLowerCase().substring(0, gIn.length).startsWith(gIn.toLowerCase())) {
                let option = document.createElement('option');
                option.value = e.Description;
        
                getInp.appendChild(option);
            }
        })
    })
    
}




function showWarHouses(t) {
    console.log(t.value)
}
    