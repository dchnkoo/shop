lineTh('.put-product-container>div + div > div > .select-category > ul > span',
'.put-product-container>div + div > div > .select-category > ul > li',
'#select-category', '#add-custom')

lineTh('.put-product-container>div + div > div > .select-brand > ul > span',
'.put-product-container>div + div > div > .select-brand > ul > li',
'#select-brand-container', '#add-custom-brand')



function lineTh($el1, $el2, $selector1, $selector2) {
    const line = document.querySelector($el1);
    const li = document.querySelectorAll($el2);
    li.forEach(elem => {
        elem.onclick = e => {
            line.style.left = e.target.offsetLeft + 'px';
            line.style.width = e.target.offsetWidth + 'px';

            li.forEach(elem => {if (elem.classList.contains('active')) {elem.removeAttribute('class')}})
            e.target.classList.add('active');
            
            if (e.target.id === 'select') {
                document.querySelector($selector1).classList.remove('noactive');
                document.querySelector($selector2).classList.add('noactive');
            } else {
                document.querySelector($selector1).classList.add('noactive');
                document.querySelector($selector2).classList.remove('noactive');
            }
        }
    })
}

const filetypes = ['image/jpg', 'image/png', 'image/jpeg'];

function validFile(filetype) {
    for (let key of filetypes) {
        if (filetype === key) {
            return key.substring(6);
        }
    }

    return false;
}

function addPhotos(file, $id) {
    const getDiv = document.querySelector('.put-product-container > div > .show-images');
    var ul;

    if (getDiv.getElementsByTagName('ul').length === 0) {
        ul = document.createElement('ul');
    } else {
        ul = getDiv.getElementsByTagName('ul')[0];
    }

    const li = document.createElement('li');
    const p = document.createElement('p');
    const img = document.createElement('img');

    getDiv.append(ul);
    ul.append(li);

    img.src = window.URL.createObjectURL(file);
    p.innerText = file.name;

    li.id = $id;
    li.append(img);
    li.append(p);

    return $id;
}

const files = [];
const elem = document.querySelector('.put-product-container > div > div > div > label > input');
elem.onchange = e => {
    files.push(e.target.files[0]);
    if (e.target.id === 'title-image') {
        if (files.length === 1) {
            const title = files[0]
            if (validFile(title.type)) {
                addPhotos(title, `tit.${validFile(title.type)}`);
            } else {
                files.splice(0, 1);
            }
        }
        else if (files.length === 2) {
            const stitle = files[1];
            if (validFile(stitle.type)) {
                addPhotos(stitle, `stit.${validFile(stitle.type)}`)
            } else {
                files.splice(1, 1);
            }
        }   
        else if (files.length === 3) {
            const statics = files[2];
            if (validFile(statics.type)) {
                addPhotos(statics, `static1.${validFile(statics.type)}`)
            } else {
                files.splice(2, 1)
            }
        }
        else if (files.length === 4) {
            const static1 = files[3];
            if (validFile(static1.type)) {
                addPhotos(static1, `static2.${validFile(static1.type)}`)
            } else {
                files.splice(3, 1);
            }
        }
    }

    console.log(files)
}

function nmError($elem, txt) {
    const p = document.createElement('p');
    p.style.color = 'red';
    p.style.fontWeight = 'bold';
    p.innerText = txt;

    if ($elem.id === 'title-image') {
        if ($elem.parentElement.parentElement.querySelectorAll('p').length == 1) {
            $elem.parentElement.parentElement.append(p);
        }
    } else {
        if ($elem.parentElement.querySelectorAll('p').length == 1) {
            $elem.parentElement.append(p);
        }
    }

    $elem.onfocus = () => {
        p.remove()
    }
}

function resetPhotos() {
    document.querySelector('.put-product-container>div>.show-images>ul').remove();
    files.length = 0;
}

document.querySelector('.put-product-container>div>.images>#reset').onclick = e => {
    try {
        e.target.style.background = '#919191';
        resetPhotos()
    } catch {
        e.target.style.background = 'red';
    }
}

const form = new FormData;
const btnPutProd = document.querySelector('.put-product-container > button#add');
const changeBtn = document.querySelector('#change-prod');

let getCategory = document.querySelector('.put-product-container > div + div > div > #select-category > input');
let getCategoryCustom = document.querySelector('.put-product-container > div + div > div > #add-custom > input');

let getBrand = document.querySelector('.put-product-container > div + div > div + div > #select-brand-container > input');
let getBrandCustom = document.querySelector('.put-product-container > div + div > div + div > #add-custom-brand > input');

const model = document.querySelector('.put-product-container > div + div > div + div + div input#model');
const color = document.querySelector('.put-product-container > div + div > div + div + div input#color');
const price = document.querySelector('.put-product-container > div + div > div + div + div input#price');
const sizes = document.querySelector('.put-product-container > div + div > div + div + div input#sizes');
const much = document.querySelector('.put-product-container > div + div > div + div + div input#much');
const description = document.querySelector('.put-product-container > div + div + div > textarea');



try {
    sendChanges(btnPutProd, sendNewProduct)
} catch {
    sendChanges(changeBtn, sendChangeToProduct)
}


function sendChanges(eventClick, func) {
    eventClick.onclick = () => {
        const regXp = '^[^0-9-_~`₴!@"\'№#$%^\{\}:;&?*()+=\\\\/,<>]*$';
        const regXpM = '^[^_~`₴!@"\'№#$%^\{\}:;&?*()+=\\\,<>]*$';
        const regXpС = '^[^0-9-_~`₴!@"\'№#$%^\{\}:;&?*()+=\\\,<>.]*$';
        const regXpP = '^\\d+$';
        const regXpS = '^[^_~`₴!@"\'№#$%^\{\}:;&?*()+=\\\\/,<>]*$';
    
        // btnPutProd.disabled = true;
        new Promise((r, j) => {
            if (eventClick.id === 'change-prod') {
                r({photos: files});
            }
            else if (files.length > 0) {
                r({photos: files});
            } else {
                j(`No files for product`);
            }
        })
        .catch(e => {
            nmError(elem, e)
            throw Error(e)
        })
        .then(data => {
            return  new Promise((r, j) => {
                const category = document.querySelector('.put-product-container > div + div > div > .select-category > ul li.active').id;
                if (category === 'select') {
                    if (getCategory.value.match(regXp) && getCategory.value.length >= 1) {
                        data = {...data, info: {category: getCategory.value}}
                        r(data)
                    } else (
                        j('Жодна категорія не вибрана або має неправильний формат вводу', getCategory)
                    )
                }
                if (category === 'custom') {
                    if (getCategoryCustom.value.match(regXp) && getCategoryCustom.value.length >= 1) {
                        data = {...data, info: {category: getCategoryCustom.value}}
                        r(data)
                    } else {
                        j('Жодна категорія не вибрана або має неправильний формат вводу', getBrandCustom)
                    }
    
                }
            })
    
        })
        .catch((error, elem) => {
            nmError(elem, error)
            throw new Error(error)
        })
        .then(data => {
            return  new Promise((r, j) => {
                const brand = document.querySelector('.put-product-container>div + div > div + div > .select-brand > ul > li.active').id;
                if (brand === 'select' && getBrand.value.length >= 1) {
                    if (getBrand.value.match(regXp)) {
                        data.info.brand = getBrand.value
                        r(data)
                    } else (
                        j('Жоден Бренд не вибраний або має неправильний формат вводу', getBrand)
                    )
                } 
                if (brand === 'custom') {
                    if (getBrandCustom.value.match(regXp) && getBrandCustom.value.length >= 1) {
                        data.info.brand = getBrandCustom.value;
                        r(data)
                    } else {
                        j('Жоден Бренд не вибраний або має неправильний формат вводу', getBrandCustom)
                    }
    
                }
            })
        })
        .catch((error, elem) => {
            nmError(elem, e)
            throw new Error(error)
        })
        .then(data => {
            return new Promise((r, j) => {
                if (model.value.match(regXpM) && model.value.length >= 1) {
                    data.info.model = model.value;
                    r(data)
                } else {
                    j('Не введена модель вбо неправильний формат вводу');
                }
            })
        })
        .catch(error => {
            nmError(model, error)
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                if (color.value.match(regXpС) && color.value.length >= 1) {
                    data.info.color = color.value;
                    r(data)
                } else {
                    j('Не введений колір вбо неправильний формат вводу');
                }
            })
        })
        .catch(error => {
            nmError(color, error);
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                if (price.value.match(regXpP) && price.value.length >= 1) {
                    data.info.price = price.value;
                    r(data)
                } else {
                    j('Не введена ціна вбо неправильний формат вводу');
                }
            })
        })
        .catch(error => {
            nmError(price, error);
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                if (sizes.value.match(regXpS) && sizes.value.length >= 1) {
                    data.info.sizes = sizes.value;
                    r(data)
                } else {
                    j('Не введені розміри вбо неправильний формат вводу');
                }
            })
        })
        .catch(error => {
            nmError(sizes, error)
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                if (much.value.match(regXpP) && much.value.length >= 1) {
                    data.info.much = much.value;
                    r(data)
                } else {
                    j('Не введені розміри вбо неправильний формат вводу');
                }
            })
        })
        .catch(error => {
            nmError(much, error)
            throw new Error(error);
        })
        .then(data => {
            return new Promise((r, j) => {
                data.info.description = description.value;
                r(data)  
            })
        })
        .then(data => {
            if (eventClick.id === 'change-prod') {
                const id = document.querySelector('.here-id').innerText;
                data.info.id = id;
            } 
            
            func(data.photos, data.info);
        })
        
    }

}


function sendChangeToProduct(photos, obj) {
    photos.forEach((elem, i) => {
        form.append(`file${i}`, elem)
    })
    form.append('data', JSON.stringify(obj))
    fetch(window.location.pathname.replace('/product', '') + '/change', {
        'method' : 'PUT',
        'body' : form
    })
    .then(data => data.json())
    .then(data => {
        if (data.code === 200) {
            window.reload()
        } else {
            console.log(data)
        }
    })
}



function sendNewProduct(photos, obj) {
    photos.forEach((elem, i) => {
        form.append(`file${i}`, elem);
    })
    form.append('data', JSON.stringify(obj))
    fetch(window.location + '/change', {
        'method' : 'POST',
        'body' : form
    })
    .then(data => data.json())
    .then(d => {
        if (d.code === 200) {
            files.length = 0;
            getCategory.value = '';
            getCategoryCustom.value = '';
            getBrand.value = '';
            getBrandCustom.value = '';
            model.value = '';
            color.value = '';
            price.value = '';
            sizes.value = '';
            much.value = '';
            description.value = '';
            resetPhotos()
            succesWindow()
            setTimeout(reload, 1800)
        } else if (d.code >= 400) {
            document.querySelectorAll('.delete-ptoduct').forEach(elem => {
                elem.onclick = e => {
                    const windowModal = document.querySelector('.modal-window');
                    const p = document.createElement('p');
                    const infoElem = windowModal.querySelector('.info');
        
                    p.innerText = d.msg;
                    infoElem.append(p);
        
                    windowModal.style.display = 'grid';
                    windowModal.style.placeContent = 'center';
        
                    const cancelBtn = windowModal.querySelector('#cancel');
                    const okBtn = windowModal.querySelector('#ok');
                    okBtn.innerHTML = 'ок';
        
                    cancelBtn.onclick = () => {
                        windowModal.style.display = 'none';
                        p.remove()
                    }
                    
                    okBtn.onclick = () => {
                        windowModal.style.display = 'none';
                        p.remove()
                    }
                }
            })
        }
    })
}

function reload() {
    window.location.reload()
}