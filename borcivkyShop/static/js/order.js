function getName() {
    let getName = Array.from(document.querySelectorAll(".userName")).filter(elem => {
        let name = elem.querySelector('input');
        if (name.value.length >= 1) {
            return name.value;
        }
    })[0];

    try {
        return {name: getName.querySelector('input').value, elem: getName};
    } catch {

    }
}

function getSecondName() {
    let get = Array.from(document.querySelectorAll('.userSecondName')).filter(elem => {
        let second = elem.querySelector('input');

        if (second.value.length >= 1) {
            return second.value;
        }
    })[0];

    try {
        return {secondName: get.querySelector('input').value, elem: get}
    } catch {

    }
}

function getPhone() {
    let get = Array.from(document.querySelectorAll('.userPhone')).filter(elem => {
        let phone = elem.querySelector('input');

        if (phone.value.length >= 1) {
            return phone.value;
        }
    })[0];

    try {
        return {phone: get.querySelector('input').value, elem: get};

    } catch {

    }
}

function getEmail() {
    let get = Array.from(document.querySelectorAll('.userEmail')).filter(elem => {
        let email = elem.querySelector('input');

        if (email.value.length >= 1) {
            return email.value;
        }
    })[0];

    try {
        return {email: get.querySelector('input').value, elem: get};
    } catch {

    }
}

function getCityUser() {
    let get = Array.from(document.querySelectorAll('#choose-city-input')).filter(elem => {
        if (elem.value.length >= 1) {
            return elem.value;
        }
    })[0];

    try {
        return {city: get.value, elem: get}
    } catch {
        document.querySelectorAll('#choose-city-input').forEach(elem => {
            if (document.querySelectorAll('.invalid-city').length < 1) {
                let p = document.createElement('p');
            
                p.setAttribute('class', 'invalid-city');
                p.style.color = 'red';
                p.style.fontWeight = 'bold'
                p.style.position = 'absolute'
                p.style.bottom = '-20px'
                p.style.left = '0'
                p.innerText = `*оберіть місто`;
    
                elem.parentElement.append(p)
            } 
        })
    }
}

function getVidilUser() {
    let get = Array.from(document.querySelectorAll('#choose-vid-input')).filter(elem => {
        if (elem.value.length >= 1) {
            return elem.value;
        }
    })[0];

    try {
        return {vidil: get.value, elem: get}
    } catch {
        document.querySelectorAll('#choose-vid-input').forEach(elem => {
            if (document.querySelectorAll('.invalid-vid').length < 1) {
                let p = document.createElement('p');
            
                p.setAttribute('class', 'invalid-vid');
                p.style.color = 'red';
                p.style.fontWeight = 'bold'
                p.style.position = 'absolute'
                p.style.bottom = '-20px'
                p.style.left = '0'
                p.innerText = `*оберіть місто`;
    
                elem.parentElement.append(p)
            }
        })
    }
}



function getOpl() {
    let getObjects = Array.from(document.querySelectorAll('.orders-opl-elems')).filter(
        elem => elem.getAttributeNames().includes('data'))[0];
        
        
    try {
        return {opl: getObjects.value, elem: getObjects};
    } catch {
        Array.from(document.querySelectorAll('.oplata')).forEach(elem => {
            let span = document.createElement('span');

            span.setAttribute('class', 'invalid-opl');
            span.style.color = 'red';
            span.style.fontWeight = 'bolder';
            span.style.position = 'absolute';
            span.style.top = '2rem';
            span.style.left = '0';
            span.innerHTML = '*оберіть спосіб оплати';

            elem.append(span);

        })   
    }
}

$('.oplata input').click(elem => {
    if (document.querySelectorAll('.invalid-opl')) {
        document.querySelectorAll('.invalid-opl').forEach(elem => elem.remove())
    }

    $('.oplata input').removeAttr('data');
    
    elem.target.setAttribute('data', 'checked');
})




function nameError(name, value, clas) {

    try {
        if (!name.querySelector('.'+clas)) {
            let p = document.createElement('p');
        
            p.setAttribute('class', clas);
            p.style.color = 'red';
            p.style.fontWeight = 'bold'
            p.innerText = `*${value}`;
        
            name.append(p);
        }
        
    } catch {

    }

    try {
        name.querySelector('input').onfocus = () => {
            name.querySelector('.'+clas).remove()
        }
    } catch {

    }
}

$('.submit-bckt').click(sendObject);
function sendObject(e) {
    getData(e, orders)
}

$('.form .submit, .forms .submit').click(getData);


function getData(e,obj) {
    const form = new FormData()
    
    const regName = '^[^0-9-_~`₴!@"\'№#$%^\{\}:;&?*()+=\\\\/,<>. ]*$';
    const phoneReg = '^(\\+38|38)?(039|050|063|066|067|068|073|089|091|092|093|094|095|096|097|098|099)([0-9]{7})$';
    // const emailRegxp = new RegExp('^([\\w0-9_-]+)([\\.\\w0-9_-]+)?@(\\w+)\\.(\\w{2,})(\\.\\w{2,})?$')
    const emailRegp = '^(\\w+)\\.?((\\w+|\\w+\\.\\w+(\\.\\w+)?))?@([a-zA-Z]+)\\.([a-zA-Z]{2,})(\\.[a-zA-Z]{2,})?$'
    
    try {
        new Promise((r, j) => {
            const name = getName();
            if (name.name.match(regName)) {
                r(name.name);
            } else {
                j(name.elem)
            }
        })
        .catch(error => {
            nameError(error, 'Ім\'я повинно містити літери від А-я або A-z без спеціальних символів, цифр та пробілів', 'invalid-name');
            throw new Error(error);
        })
        .then(userName => {
            return new Promise((r, j) => {
                const secondName = getSecondName();
                if (secondName.secondName.match(regName)) {
                    r({name: userName, secondName: secondName.secondName});
                } else {
                    j(secondName.elem)
                }
            })
        })
        .catch(error => {
            nameError(error, 'Прізвище повинно містити літери від А-я або A-z без спеціальних символів, цифр та пробілів', 'invalid-second-name');
            throw new Error(error);
        })
        .then(value => {
            return new Promise((r, j) => {
                const phone = getPhone() 
                if (phone.phone.match(phoneReg)) {
                    let userPhone = phone.phone;
                    r({...value, userPhone});
                } else {
                    j(phone.elem)
                }        
            })
        })
        .catch(error => {
            nameError(error, 'Неправильний формат номеру або недійсний оператор будь ласка перевірте правильність вводу', 'invalid-phone');
            throw new Error(error);
        })
        .then(obj => {
            return new Promise((r, j) => {
                const email = getEmail()
                if (email.email.match(emailRegp)) {
                    let userEmail = email.email;
                    r({...obj, userEmail});
                } else {
                    j(email.elem);
                }
            })
        })
        .catch(error => {
            nameError(error, 'Неправильний формат електроноЇ пошти. Приклад nospace@between.mailids.in', 'invalid-email');
            throw new Error(error);
        })
        .then(obj => {
            return new Promise((r, j) => {
                try{
                    let size = document.querySelector('.active-size').innerHTML;;

                    r({...obj, size})
                } catch {
                    j(document.querySelector('.sizes > div'))
                }
            })       
        })
        .catch(error => {
            nameError(error, 'оберіть розмір', 'no-active-size');
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                const getCity = getCityUser();
                if (getCity !== undefined) {
                    let City = getCity.city 
                    r({...data, City})
                } else {
                    j(getCity.elem)
                }
            })
        })
        .catch(() => {
            throw new Error('city error')
        })
        .then(data => {
            return new Promise((r, j) => {
                const getVidil = getVidilUser();
                if (getVidil !== undefined) {
                    let vidil = getVidil.vidil;
                    r({...data, vidil});
                } else {
                    j(getVidil.elem);
                }
        })})
        .catch(() => {
            throw new Error("vidil error");
        })
        .then(data => {
            return new Promise((r, j) => {
                const getoplata = getOpl();
                if (getoplata) {
                    let opl = getoplata.opl
                    r({...data, opl})
                } else {
                    j('oplata error')
                }
            })
        })
        .catch(error => {
            throw new Error(error);
        })
        .then(data => {
            console.log(obj)
            if (obj) {
                form.append('data', JSON.stringify({...data, ...obj}))
                sendData(form)
            } else {
                try {
                    let idProduct = document.querySelector('.form').querySelector('.info-inputs').querySelector('input').value;
                    let value = 1
                    let object = [{...data, idProduct, value}] 
                    form.append('data', JSON.stringify(object));
                    sendData(form)
                    
                } catch {
    
                    let idProduct = document.querySelector('.forms').querySelector('.info-inputs').querySelector('input').value;
                    let value = 1
                    let obj = [{...data, idProduct, value}] 
                    form.append('data', JSON.stringify(obj));
                    sendData(form)
                }    
            }
        })
    } catch {

    }
}


function sendData(form) {
    fetch(
        '/fastOrder', {
            'method' : 'POST',
            'body' : form
    })
    .catch(err => {throw new Error(err)})
    .then(status => status.json())
    .then(data => {
        document.querySelectorAll('.order-form').forEach(elem => {
            elem.classList.add('op-animation'); 
        });

        setTimeout(succesTime, 1000)
    })
}

function succesTime() {
    document.querySelector('.succes-order').style.display = 'block';
}