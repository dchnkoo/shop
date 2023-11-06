const urlParams = new URLSearchParams(window.location.search);

const idurl = urlParams.get('id');
const nameUrl = urlParams.get('name')
const imgUrl = urlParams.get('imgUrl');
const priceurl = urlParams.get('price');
let discountUrl = urlParams.get('discount');
const sizes = [];

document.querySelectorAll('.product-size').forEach(elem => {
    sizes.push(elem.innerText)
}) 

if (discountUrl === 'null') {
    discountUrl = null;
}

const Product = new Card({
    idProduct: idurl,
    name: nameUrl,
    image: imgUrl,
    price: priceurl,
    discount: discountUrl,
    sizes: sizes
})



function dlAnim() {
    document.getElementById('invalid').style.animation = 'none'
}

function createElemP() {
    let crP = document.createElement('p');
    crP.setAttribute('id', 'invalid')
    crP.innerText = 'Спочатку оберіть розмір';
    crP.style.color = 'red';
    crP.style.fontWeight = 'bolder';
    crP.style.marginBottom = '0.3rem'

    document.querySelector('.product-sizes')
        .append(crP)
}

function setPAniamtion() {
    document.getElementById('invalid').style.animation = 'invalid 0.4s ease-in'

    setTimeout(dlAnim, 500)
}

function setDopObj() {
    Product.ordersize = document.querySelector('.active-size').innerHTML;
    Product.value = parseInt(document.querySelector('.number-btns > span').innerHTML);
}

function buyBtn() {
    if (document.querySelector('.active-size')) {
        setDopObj()
        console.log(Product)
        showOrderWindow(Product)
    } else {
        if (document.getElementById('invalid')) {
            setPAniamtion()
        } else {
            createElemP()
        }
    }
}

function bcktBtn() {
    if (document.querySelector('.active-size')) {
        setDopObj()
        appendToBckt(proxyObjCreator(JSON.parse(JSON.stringify(Product)), {
            set(t, p, v) {
                if (p !== 'value') {
                    throw new Error('Please do not touch(((')
                } else {
                    t[p] = v
                }
            }
        }))
    } else {
        if (document.getElementById('invalid')) {
            setPAniamtion()
        } else {
            createElemP()
        }
    }
}