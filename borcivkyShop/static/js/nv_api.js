const getInp = document.querySelector('datalist#choose-city');
const [getInput, ge] = document.querySelectorAll('#choose-city-input');

const dataObl = {
        "apiKey": "11fcc66be04919e9b17d3744d6f7c8fc",
        "modelName": "Address",
        "calledMethod": "getSettlements",
        "methodProperties": { "FindByString": "", "Limit" : '10' }
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
    "methodProperties": { "FindByString": "", "Limit" : '15' }
}

const cityObj = {
    'method' : 'POST',
    'headers' : {
        'Content-type' : 'application/json'
    },
    'body' : JSON.stringify(getCities)
}

function requestsApi(value) {
    getCities.methodProperties.FindByString = value;
    dataObl.methodProperties.FindByString = value;

    console.log(getCities.methodProperties.FindByString,
        dataObl.methodProperties.FindByString)

    Promise.all([
        fetch('https://api.novaposhta.ua/v2.0/json/', oblObj),
        fetch('https://api.novaposhta.ua/v2.0/json/', cityObj)
    ])
    .then(data => data.forEach(d => d.json()))
    .then(r => r.forEach(v => v.then(d => {
        console.log(d)
        d.data.forEach(v => {
            if (v.Description.toLowerCase().substring(0, value.length).startsWith(value.toLowerCase())) {
                let option = document.createElement('option');
                option.value = v.Description;
        
                getInp.appendChild(option);
            } else if (v.AreaDescription.toLowerCase().substring(0, value.length).startsWith(value.toLowerCase())) {
                let op = document.createElement('option');
                op.value = v.AreaDescription;
        
                getInp.appendChild(op);
            }
        })
    })))
} 

getInput.onkeydown = e => {
    requestsApi(e.target.value)  
}

ge.onkeydown = e => {
    requestsApi(e.target.value)  
}


function showWarHouses(t) {
    console.log(t.value)
}
    