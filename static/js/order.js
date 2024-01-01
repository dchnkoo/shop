function getValueOrder($selector) {
    let getName = Array.from(document.querySelectorAll($selector)).filter(elem => {
        let name = elem.querySelector('input');
        if (name.value.length >= 1) {
            return name.value;
        }
    })[0];

    try {
        return {name: getName.querySelector('input').value, elem: getName};
    } catch {
        console.log('ne ok')
    }
}

function getCityUser($selector) {
    let get = Array.from(document.querySelectorAll($selector)).filter(elem => {
        if (elem.value.length >= 1) {
            return elem.value;
        }
    })[0];

    try {
        return {city: get.value, elem: get}
    } catch {
        document.querySelectorAll($selector).forEach(elem => {
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

function getVidilUser($selector) {
    let get = Array.from(document.querySelectorAll($selector)).filter(elem => {
        if (elem.value.length >= 1) {
            return elem.value;
        }
    })[0];

    try {
        return {vidil: get.value, elem: get}
    } catch {
        document.querySelectorAll($selector).forEach(elem => {
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



function getOpl($selector, $sele) {
    let getObjects = Array.from(document.querySelectorAll($selector)).filter(
        elem => elem.getAttributeNames().includes('data'))[0]
        
    try {
        return {opl: getObjects.value, elem: getObjects};
    } catch {
        Array.from(document.querySelectorAll($sele)).forEach(elem => {
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

$('.oplata input, .oplatab input').click(elem => {
    if (document.querySelectorAll('.invalid-opl')) {
        document.querySelectorAll('.invalid-opl').forEach(elem => elem.remove())
    }

    $('.oplata input, .oplatab input').removeAttr('data');
    
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

function formsReset(e) {
    document.querySelector('.userName').querySelector('input').value = '';
    document.querySelector('.userNameb').querySelector('input').value = '';
    document.querySelector('.userSecondName').querySelector('input').value = '';
    document.querySelector('.userSecondNameb').querySelector('input').value = '';
    document.querySelector('.userPhoneb').querySelector('input').value = '';
    document.querySelector('.userPhone').querySelector('input').value = '';
    document.querySelector('.userEmail').querySelector('input').value = '';
    document.querySelector('.userEmailb').querySelector('input').value = '';
    document.querySelectorAll('#choose-city-input').forEach(elem => elem.value = '')
    document.querySelectorAll('#choose-vid-input').forEach(elem => {elem.value = ''; elem.style.display = 'none'})
    document.querySelectorAll('#choose-vid').forEach(elem => elem.style.display = 'none')

    let ord = document.querySelector('.bckt-orders');
    let get = Array.from(ord.getElementsByTagName('div'));

    if (e.target.getAttribute('class') === 'submit-bckt') {
        if (get.length > 1) {
            get.forEach(elem => {
                if (elem.classList.contains('order')) {
                    elem.remove()
                }
            })
            orders.length = 0;
            localStorage.setItem(LCSTORAGE, '[]')
            sumBcktPrice();
        }
    }
}


$('.submit-bckt').click(bData);

function bData(e) {
    getData(e, orders,'.userNameb', '.userSecondNameb', '.userPhoneb',
            '.userEmailb', '#choose-city-input', '#choose-vid-input', ['.orders-opl-elemsb', '.oplatab'], '.submit-bckt')
}

$('.form .submit').click(sData);


function sData(e) {
    getData(e, null, '.userName', '.userSecondName', '.userPhone',
            '.userEmail', '#choose-city-input', '#choose-vid-input', ['.orders-opl-elems', '.oplata'], '.form .submit')
}

$('.forms .submit').click(hData)
function hData(e) {
    getData(e, null, '.userName', '.userSecondName', '.userPhone',
            '.userEmail', '#choose-city-input', '#choose-vid-input', ['.orders-opl-elems', '.oplata'], '.forms .submit')
}

function disabledBtn($selector, undisable = false) {
    if (undisable) {
        document.querySelector($selector).removeAttribute('disabled')
    } else {
        document.querySelector($selector).setAttribute('disabled', 'disabled');
    }

}


function getData(e, obj, $name, $secName, $phone, $email, $city, $vidil, opl, btn) {
    const form = new FormData()

    
    const regName = '^[^0-9-_~`₴!@"\'№#$%^\{\}:;&?*()+=\\\\/,<>. ]*$';
    const phoneReg = '^(\\+38|38)?(039|050|063|066|067|068|073|089|091|092|093|094|095|096|097|098|099)([0-9]{7})$';
    // const emailRegxp = new RegExp('^([\\w0-9_-]+)([\\.\\w0-9_-]+)?@(\\w+)\\.(\\w{2,})(\\.\\w{2,})?$')
    const emailRegp = '^(\\w+)\\.?((\\w+|\\w+\\.\\w+(\\.\\w+)?))?@([a-zA-Z]+)\\.([a-zA-Z]{2,})(\\.[a-zA-Z]{2,})?$'
    


    try {
        disabledBtn(btn)
        new Promise((r, j) => {
            const name = getValueOrder($name);
            if (name && name.name.match(regName)) {
                let userName = name.name
                r(userName);
            } else {
                j('Ім\'я повинно містити літери від А-я або A-z без спеціальних символів, цифр та пробілів', 'invalid-name')
            }
        })
        .catch(error => {
            disabledBtn(btn, true)
            console.log(error)
            nameError(error, 'Ім\'я повинно містити літери від А-я або A-z без спеціальних символів, цифр та пробілів', 'invalid-name');
            throw new Error(error);
        })
        .then(userName => {
            return new Promise((r, j) => {
                const secondName = getValueOrder($secName);
                if (secondName.name.match(regName)) {
                    r({userName: userName, secondName: secondName.name});
                } else {
                    j(secondName.elem)
                }
            })
        })
        .catch(error => {
            disabledBtn(btn, true)
            nameError(error, 'Прізвище повинно містити літери від А-я або A-z без спеціальних символів, цифр та пробілів', 'invalid-second-name');
            throw new Error(error);
        })
        .then(value => {
            return new Promise((r, j) => {
                const phone = getValueOrder($phone) 
                if (phone.name.match(phoneReg)) {
                    let userPhone = phone.name;
                    r({...value, userPhone});
                } else {
                    j(phone.elem)
                }        
            })
        })
        .catch(error => {
            disabledBtn(btn, true)

            nameError(error, 'Неправильний формат номеру або недійсний оператор будь ласка перевірте правильність вводу', 'invalid-phone');
            throw new Error(error);
        })
        .then(obj => {
            return new Promise((r, j) => {
                const email = getValueOrder($email)
                if (email.name.match(emailRegp)) {
                    let userEmail = email.name;
                    r({...obj, userEmail});
                } else {
                    j(email.elem);
                }
            })
        })
        .catch(error => {
            disabledBtn(btn, true)

            nameError(error, 'Неправильний формат електроноЇ пошти. Приклад nospace@between.mailids.in', 'invalid-email');
            throw new Error(error);
        })
        .then(object => {
            return new Promise((r, j) => {
                if (obj) {
                    r({...object, ...obj})
                } else {
                    try{
                        let ordersize = document.querySelector('.active-size').innerHTML;;
    
                        r({...object, ordersize})
                    } catch {
                        j(document.querySelector('.sizes > div'))
                    }
                }
            })       
        })
        .catch(error => {
            disabledBtn(btn, true)

            nameError(error, 'оберіть розмір', 'no-active-size');
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                const getCity = getCityUser($city);
                if (getCity !== undefined) {
                    let City = getCity.city 
                    r({...data, City})
                } else {
                    j(getCity.elem)
                }
            })
        })
        .catch(() => {
            disabledBtn(btn, true)

            throw new Error('city error')
        })
        .then(data => {
            return new Promise((r, j) => {
                const getVidil = getVidilUser($vidil);
                if (getVidil !== undefined) {
                    let vidil = getVidil.vidil;
                    r({...data, vidil});
                } else {
                    j(getVidil.elem);
                }
        })})
        .catch((error) => {
            disabledBtn(btn, true)
            throw new Error("vidil error");
        })
        .then(data => {
            return new Promise((r, j) => {
                const getoplata = getOpl(...opl);
                if (getoplata) {
                    let opls = getoplata.opl
                    r({...data, opls})
                } else {
                    j('oplata error')
                }
            })
        })
        .catch(error => {
            disabledBtn(btn, true)

            throw new Error(error);
        })
        .then(data => {
            if (obj !== null) {
                let ord = []
                obj.forEach(elem => ord.push({...data, ...elem}))

                form.append('data', JSON.stringify(ord))
                sendData(form, e, btn)
            } else {
                try {
                    let idProduct = document.querySelector('.form').querySelector('.info-inputs').querySelector('input').value;
                    let value = 1
                    let object = [{...data, idProduct, value}]
                    form.append('data', JSON.stringify(object));
                    sendData(form, e, btn)
                    
                } catch {
                    let idProduct = document.querySelector('.forms').querySelector('.info-inputs').querySelector('input').value;
                    let value = 1
                    let obj = [{...data, idProduct, value}] 
                    form.append('data', JSON.stringify(obj));
                    sendData(form, e, btn)
                }    
            }
    })
    } catch {

    }
}


function sendData(form, e, b) {
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

        disabledBtn(b, true)
        formsReset(e);
        setTimeout(succesTime, 1000)
    })
}

function succesTime() {
    document.querySelectorAll('.succes-order').forEach(elem => elem.style.display = 'block')
}