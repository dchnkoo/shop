const cards = [];
const orders = [];
const getDate = new Date();
const LCSTORAGE = 'user_trash';

let setPosition;
let cardSetter = 11;

class Card {
    constructor(options) {
        this.productId = options.productId
        this.image = options.image
        this.name = options.name
        this.price = options.price
        this.discount = options.discount
        this.sizes = options.sizes
        this.element = options.element
    }
}


class Cards {

    NotFoundWindow(value) {
        $('.not-found').css('display', value)
    }

    #checkCardsLength() {
        $('.cards-con-cont').length < 1 ? (
            $('.more-cards').css({'display' : 'none'}),
            this.NotFoundWindow('block')
        ) : null;
    }

    #baseUrl(url) {
        return window.location.origin + url;
    }


    #showProductPage = (e) => {
        let getObj;

        e.target.id !== null ? (
            getObj = cards.filter(v => (v.productId === e.target.id))[0],
            location.href = this.#baseUrl(`/ProductPage?id=${getObj.productId}&imgUrl=${getObj.image}&price=${getObj.price}&discount=${getObj.discount}&name=${getObj.name}&sizes=${getObj.sizes}`)
        ) :
            location.href = this.#baseUrl('/');
    }

    showMoreBtn() {
        cardSetter = cardSetter + 10;

        $('.cards-con-cont').each((index, element) => {
            index < cardSetter && element.getAttribute('class') === 'cards-con-cont noactive' ? 
                element.setAttribute('class', 'cards-con-cont') : $('.more-cards').css({'display' : 'none'})
        })
    }

    getCardsInformationAndParse() {
        let prodId;
        let img;
        let nameProduct;
        let priceProd;
        let discountPrice;
        let sizesProd;

        this.#checkCardsLength();
        $('.cards-con-cont').each((index, element) => {
            let getCard = element.getElementsByClassName('card-container')[0];
            prodId = getCard.getAttribute('id');

            // //////////////////// images /////////////////////////////////////  
            let getImgContainer = getCard.getElementsByClassName('card-image')[0];
            let getImgElement = getImgContainer.getElementsByTagName('img');

            let getArr = Array.from(getImgElement);

            getArr.length === 1 ? (
                getArr[0].setAttribute('class', 'title activated'),
                getArr[0].addEventListener('click', this.#showProductPage),
                img = getArr[0].alt
            ) : getArr.forEach(el => {
                el.addEventListener('click', this.#showProductPage);
                
                let getLengthName = 
                    el.src.substring(el.src.indexOf('/', el.src.length - 10) + 1).length;

                getLengthName <= 7 ? (
                    el.setAttribute('class', 'title activated_opacity'),
                    img = el.alt
                ) : el.setAttribute('class', 'title_two opacity');
            })

            // //////////////// name ///////////////////////////////////////////

            let getCardName = getCard.getElementsByClassName('card-name')[0];
            getCardName.addEventListener('click', this.#showProductPage);
            nameProduct = getCardName.innerHTML;

            // //////////////// price /////////////////////////////////////////
            try {
                 priceProd = getCard.querySelector('.discountPrice').innerHTML;
                 discountPrice = getCard.getElementsByClassName('card-price-without-discount')[0].innerHTML;
            } catch {
                priceProd = getCard.getElementsByClassName('card-price')[0].innerHTML;
                discountPrice = null;
            }

            // /////////////// sizes //////////////////////////////////////////
            let tmSizeArr = [];
            Array.from(getCard.getElementsByClassName('size noactive')).forEach(s => {
                tmSizeArr.push(s.innerHTML);
            })
            sizesProd = tmSizeArr;

            cards.push(new Card({
                productId: prodId,
                image: img,
                name: nameProduct,
                price: priceProd,
                discount: discountPrice,
                sizes: sizesProd,
                element: element
            }))
    
    
            index > cardSetter ? (
                element.setAttribute('class', element.getAttribute('class') + ' noactive'),
                $('.more-cards').css({
                    'display' : 'flex',
                    'justify-content' : 'center'
                })
            ) : $('.more-cards').css({
                        'display' : 'none'
                })
        })

    }
}


function BGblur() {
    $('.page-container, .header').css({
        'filter' : 'blur(3px)'
    })
}

function BGreBlur() {
    $('.page-container, .header').css({
        'filter' : 'blur(0px)'
    })
}

function setSizes(obj) {
    const block = $('.sizes > div');
    block.empty()
    obj.sizes.map(e => {
        if (obj.ordersize && e === obj.ordersize) {
            block.append("<span class='product-size active-size'>" + e + "</span>");
        } else {
            block.append("<span class='product-size'>" + e + "</span>");
        }
        
        $('.product-size').click(function(e) {
            $('.product-size').css({
                'border-color' : '#33333326',
                'color' : '#3333337a'
            }).removeClass('active-size')
            if (document.querySelector('.invalid-size')) {

                document.querySelector('.invalid-size').style.display = 'none';
            }
    
    
            $(this).css({
                'border-color' : '#46A358',
                'color' : '#46A358'
            }).addClass('active-size');
        })
    })

}


function showOrderWindow(obj) {
    let getOrederWindow = document.querySelector('.show-order-block');
    let orderBlock = $('.order-block')
    
    try {
        getOrederWindow.getElementsByClassName('bkt-btn')[0].setAttribute('id', obj.productId)
    } catch {

    }

    Array.from(getOrederWindow.getElementsByTagName('input')).forEach(elem => {
        if (elem.name === 'prodcutId') {
            elem.setAttribute('value', obj.productId);
        }
    })

    Array.from(getOrederWindow.getElementsByTagName('div')).forEach(elem => {

        if (elem.getAttribute('class') === 'order-img') {
            elem.getElementsByTagName('img')[0].src = obj.image;
        }  else if (elem.getAttribute('class') == 'order-name_price') {
            elem.getElementsByClassName('order-name')[0].innerHTML = obj.name

            if (obj.discount !== null) {
                let Withoutprice = elem.getElementsByClassName('order-price');
                Withoutprice[0].style.textDecoration = 'line-through';
                Withoutprice[0].style.opacity = 0.6;
                Withoutprice[0].style.color = '#333';
                Withoutprice[0].innerHTML = obj.discount; 

                let dics_price = elem.getElementsByClassName('order-discount');
                dics_price[0].style.display = 'block';
                dics_price[0].style.fontWeight = 600;
                dics_price[0].style.color = '#973F3F';
                dics_price[0].innerHTML = obj.price
            } else {
                let dics_price = elem.getElementsByClassName('order-discount');
                dics_price[0].style.display = 'none';

                var price = elem.getElementsByClassName('order-price');
                price[0].style.textDecoration = 'none';
                price[0].style.opacity = 1;
                price[0].style.color = '#46A358';
                price[0].innerHTML = obj.price;
            }
        }
    })

    setSizes(obj);
    BGblur();

    getOrederWindow.onclick = e => {
        if (Array.from(e.target.classList).includes('show-order-block')) {
            closeOrderWindow()
        }
    }


    getOrederWindow.style.height = document.documentElement.offsetHeight + 'px';
    getOrederWindow.classList.remove('noactive')
    getOrederWindow.classList.add('show')
    orderBlock.removeClass('noactive').addClass('show').css({'top' : setPosition + 'px'});
    orderBlock[0].scrollIntoView();
}

function getScroll() {
    let display = $('#btn-to_top');

    if (scrollY < 700) {
        display.css({
            'display' : 'none'
        })
    } else {
        display.css({
            'display' : 'block'
        })
    }
}

function descriptionTxt() {
    const description = $('.description');
    let timeTXt;

    let txtLength = 200;

    if (description.text().length > txtLength) {
        timeTXt = description.text();

        description.text(description.text().substring(0, txtLength));

        $('.desc-btn').show().click(function() {
            description.text(timeTXt);
            $(this).hide()
        })
    }
}

function getCardOrder(e) {
    let c = cards.filter(v => (v.productId == e.target.id) || (v.productId == e.productId))[0];
    return c;
}

function closeOrderWindow() {
    let getOrederWindow = document.querySelector('.show-order-block');
    let showOrder = $('.order-block');
    
    BGreBlur()

    getOrederWindow.classList.add('noactive')
    getOrederWindow.classList.remove('show')

    showOrder.removeClass('show').addClass('noactive');

    showOrder.find('.form').css({
        'display' : 'none'
    });

    showOrder.find('div').each((index, elem) => {
        elem.getAttribute('class') === 'order-pre-form-btns' ? elem.style.display = 'flex' : null;    
    })
}

function sumBcktPrice() {
    if (orders.length < 1) {
        document.querySelector('.total-sum span.sum').innerHTML = 0;
        document.getElementById('counter-cards').style.display = 'none';
    } else {
        document.getElementById('counter-cards').innerText = orders.length;
        document.getElementById('counter-cards').style.display = 'flex';

        document.querySelector('.total-sum span.sum').innerHTML = orders.reduce((e, v) => e + (parseInt(v.price) * parseInt(v.value)), 0)
    }
}

function checkLocalStorage() {
    let getObjects = JSON.parse(localStorage.getItem(LCSTORAGE));

    if (getObjects) {
        for (let obj in getObjects) {
            appendToBckt(getObjects[obj])
        }
    }
}

function appendToBckt(obj) {
    if (orders.findIndex(v => v.productId === obj.productId && v.ordersize === obj.ordersize) !== -1) {
            let getObj = orders.findIndex(v => v.productId === obj.productId && v.ordersize === obj.ordersize);

            orders[getObj].value += obj.value;
            document.querySelector('.products-bckt-container')
                .querySelector(`div[id="${orders[getObj].ordersize + orders[getObj].productId}"]`).querySelector(`input`).value = orders[getObj].value;
            sumBcktPrice()
            localStorage.setItem(LCSTORAGE, JSON.stringify(orders))
    } else {
        orders.push(obj);
        localStorage.setItem(LCSTORAGE, JSON.stringify(orders))
    
        if (document.querySelector('.bckt-orders .empty')) {
            document.querySelector('.bckt-orders .empty').style.display = 'none'
            document.querySelector('.go-form-btn-order').style.display = 'block'
            document.querySelector('.total-sum').style.display = 'block';
        }
        
        sumBcktPrice()
    
        if (obj.discount !== null) {
            $('.bckt-orders').append(`<div id='${obj.ordersize + obj.productId}' class="order"><div class="bckt-img-container"><img src="${obj.image}"></div><div class="bckt-name_price"><div class="container"><p class="order-name">${obj.name} - ${obj.ordersize}</p><span class="card-price-without-discount">${obj.discount}</span><span class="discountPrice">${obj.price}</span></div><div class="btn-del"><input onchange='vlChange(this, this.parentElement.parentElement.parentElement)' id='${obj.productId}' type="number" min="1" value="${obj.value}"><button id='${obj.productId}' onclick='remElem(this)' class="del">Прибрати з корзини</button></div></div><span class="prodcutId-bckt noactive">${obj.productId}</span></div>`)
        } else {
            $('.bckt-orders').append(`<div id='${obj.ordersize + obj.productId}' class="order"><div class="bckt-img-container"><img src="${obj.image}"></div><div class="bckt-name_price"><div class="container"><p class="order-name">${obj.name} - ${obj.ordersize}</p><p class="order-price">${obj.price}</p></div><div class="btn-del"><input onchange='vlChange(this, this.parentElement.parentElement.parentElement)' id='${obj.productId}' type="number" min="1" value="${obj.value}"><button onclick='remElem(this)' id='${obj.productId}' class="del">Прибрати з корзини</button></div></div><span class="prodcutId-bckt noactive">${obj.productId}</span></div>`)
        }
    }
}


function vlChange(elem, parent) {
    let getOrd = orders.findIndex(v => v.productId === elem.id);

    orders[getOrd].value = document.querySelector(`div[id="${parent.id}"]`).querySelector(`input[id="${elem.id}"]`).value;
    sumBcktPrice()
    localStorage.setItem(LCSTORAGE, JSON.stringify(orders))
}


function remElem(e) {
    let getElem = orders.findIndex(obj => obj.productId === e.id);
    e.parentElement.parentElement.parentElement.remove();
    orders.splice(getElem, 1)
    localStorage.setItem(LCSTORAGE, JSON.stringify(orders))

    sumBcktPrice();
    
    if (orders.length < 1) {
        document.querySelector('.bckt-orders .empty').style.display = 'flex';
        document.querySelector('.go-form-btn-order').style.display = 'none';
        document.querySelector('.form-order').style.display = 'none';
        document.querySelector('.total-sum').style.display = 'none';
    } 
}

function setOrdersClose() {
    BGreBlur()
    $('.products-bckt-window').css('display', 'none');
    $('.products-bckt .form-order').css('display', 'none');
    $('.btn-container').css('display', 'block');
}





// //////////////////////////////////////////////////////////////
//                                                             //
//                  page functions initialization              // 
//                                                             // 
// //////////////////////////////////////////////////////////////
let c = new Cards()
window.onload = () => {
    c.getCardsInformationAndParse()
    checkLocalStorage()

    $('.more-cards').click(c.showMoreBtn);
    
    $('.copyright p > span').html(getDate.getFullYear());
    
    $('#menu-slide').click(() => $('#slide-menu').removeClass('disable').addClass('active'))
    $('#crosser').click(() => $('#slide-menu').removeClass('active').addClass('disable'))
    


    setInterval(getScroll, 500);

    $('#btn-to_top').click(function() {
        window.scrollTo(0, 0)
    })

    
    $('.card-btn_buy_one_click, .card-btn_buy_one_click img').click(e => {
        setPosition = (e.screenY + screen.availHeight) / 2;
        
        console.log(e)
        new Promise(r => {
            let card = getCardOrder(e);
            r(card)
        })
        .then(data =>{
            showOrderWindow(data)
        })
    })
    
    
    $('.order-info-header').click(closeOrderWindow)

    $('.go-form-btn').click(() => {
        let getElem = $('.order-block');

        getElem.find('div').each((index, elem) => {
            elem.getAttribute('class') === 'order-pre-form-btns' ? elem.style.display = 'none' : null
            }
        )

        getElem.find('.form').css({
            'display' : 'block'
        })
    })


    $('.product-size, .product-sizes label').click(function(e) {

        if (document.getElementById('invalid')) {
            document.getElementById('invalid').style.display = 'none'
        }

        $('.product-size').css({
            'border-color' : '#33333326',
            'color' : '#3333337a'
        }).removeClass('active-size')


        $(this).css({
            'border-color' : '#46A358',
            'color' : '#46A358'
        }).addClass('active-size');
    })

    $('.product-page-image-container img').click(function(e) {
        const src = e.target.getAttribute('alt');

        const bigImage = $('.prodcut-page-big-image img');

        if (bigImage.attr('src') !== src) {
            bigImage.attr('src', src);
            $('.product-page-image-container img').css('opacity', '1')
            $(this).css('opacity', '0.7');
        }
    })

    $('.plus').click(function(e) {
        const num = $('.number-btns span');
        const NumberProduct = $('.number-btns p');

        if (parseInt(num.text()) < NumberProduct.text()) {
            num.text(parseInt(num.text()) + 1)
        }
    })


    $('.minus').click(function(e) {
        const num = $('.number-btns span');

        if (num.text() > 1) {
            num.text(parseInt(num.text()) - 1)
        }
    })

    descriptionTxt();

    $('.form .submit').click(() => {
        const form = new FormData()
 
        fetch('/fastOrder', {
         'method' : 'POST',
         'body' : form
        })
        .then(status => status.json())
        .then(data => console.log(data))
        .catch(err => console.log(err))
    })


    $('.btn-container .go-form-btn-order').click(() => {
        $('.btn-container').css('display', 'none');

        $('.products-bckt .form-order').css('display', 'block');
    })


    $('#order-bckt-crosser').click(() => {
        setOrdersClose()

    })

    
    $('.header-nav-backet_btn').click(() => {
        BGblur()

        document.querySelector('.products-bckt-window').style.height = document.documentElement.offsetHeight + 'px'

        $('.products-bckt-window').fadeIn();

    })

    document.querySelector('.window-bckt-container').onclick = e => {
        console.log(e.target.classList)
        if (e.target.classList.value === 'window-bckt-container') {
            setOrdersClose()

        }
    }


    $('.bkt-btn').click((e) => {
        let getObj = JSON.parse(JSON.stringify(getCardOrder(e)));

        if (document.querySelector('.active-size')) {
            orderSize = document.querySelector('.active-size').innerHTML;

            getObj.ordersize = orderSize;
            getObj.value = 1;   
            appendToBckt(getObj);

            closeOrderWindow()
        } else if (!document.querySelector('.invalid-size')) {
            $('.order-templates-container').append('<span class="invalid-size">Для додавання товару в корзину оберіть розмір</span>');
        } else {
            document.querySelector('.invalid-size').style.display = 'block';
        }
    })

}
