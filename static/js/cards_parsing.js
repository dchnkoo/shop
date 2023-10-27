let cardSetters = 11
let setPosition;

let Product = {
    size: []
}


$(document).ready(function() {

    // init
    const moonLanding = new Date();
    $('.copyright p > span').html(moonLanding.getFullYear());


    $('.card-name').click(e => ShowProductPage(e));

    $('.more-cards').click(showMoreBtn);
    
    setInterval(getScroll, 500);

    // functions
    $('#menu-slide').click(() => $('#slide-menu').removeClass('disable').addClass('active'))
    $('#crosser').click(() => $('#slide-menu').removeClass('active').addClass('disable'))


    $('.cards-con-cont').length < 1 ? ($('.more-cards').css('display', 'none'), $('.not-found').css('display', 'block')) : null;
    $('.cards-con-cont').each(
        (index, element) => {
            let setArr = Array.from(element.getElementsByClassName('card-image'))
            setArr.forEach(elem => {
                let cardContainer = elem.getElementsByTagName('img');
                let getArray = Array.from(cardContainer);

                cardContainer.length === 1 ?
                    (cardContainer[0].setAttribute('class', 'title activated'), cardContainer[0].onclick = ShowProductPage) : getArray.forEach(elem => {
                    let getLenght = elem.src.substring(elem.src.indexOf('/', elem.src.length - 10) + 1).length;
                    
                    elem.onclick = ShowProductPage;
                    getLenght <= 7 ? elem.setAttribute('class', 'title activated_opacity') : elem.setAttribute('class', 'title_two opacity');
                })
        })

        index > cardSetters ? moreCardsBtn(element) : $('.more-cards').css('display', 'none')
    })

    function moreCardsBtn(elem) {
        let getAtr = elem.getAttribute('class');
        elem.setAttribute('class', getAtr + ' noactive');
        
        $('.more-cards').css({
            'display' : 'flex',
            'justify-content' : 'center'
        })
    }



    function ShowProductPage(event) {
        let ProductId = event.target.id

        ProductId !== null ? location.href = window.location.origin + '/ProductPage?id=' + ProductId : location.href = window.location.origin + '/';
    }

    function showMoreBtn() {
        cardSetters = cardSetters + 10; 

        let elemIndex;

        $('.cards-con-cont').each((index, element) => {
            elemIndex = index;

            index < cardSetters && element.getAttribute('class') == 'cards-con-cont noactive' ? 
                element.setAttribute('class', 'cards-con-cont') : $('.more-cards').hide();
        })
    }

    $('.card-btn_buy_one_click').click(e => {
        setPosition = (e.screenY + screen.availHeight) / 2;
        let getCard = getCardInfo(e, Product);
        showOrderWindow(getCard);
    })
    $('.card-btn_buy_one_click svg').click(e => {
    
        setPosition = (e.screenY + screen.availHeight) / 2;
        let getCard = getCardInfo(e, Product);
        showOrderWindow(getCard);
    })

    $('.order-info-header').click(() => {
        let showOrder = $('.order-block');

        reblur()

        showOrder.removeClass('show').addClass('noactive');

        showOrder.find('.form').css({
            'display' : 'none'
        });

        showOrder.find('div').each((index, elem) => {
            elem.getAttribute('class') === 'order-pre-form-btns' ? elem.style.display = 'flex' : null;    
        })

    })

    function reblur() {
        $('.page-container').css({
            'filter' : 'blur(0px)'
        });
        
        $('.header').css({
            'filter' : 'blur(0px)'
        });
    }


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


    function getCardInfo(e, obj) {
        let constructor = obj 

        let card = $('#'+e.target.id);

        card.find('div').each(function(index, elem) {
            if (elem.getAttribute('class') == 'card-image') {
                $(this).find('img').each(function(index, element) {
                    if (element.getAttribute('class') === 'title activated_opacity' || element.getAttribute('class') === 'title activated') {
                        constructor.image = element.alt
                    }
                })
                
            } else if (elem.getAttribute('class') === 'card-name-and-buybtn') {
                constructor.name = $(this).find('.card-name').text()

                $(this).find('span').each(function(ind, em) {
                    if (em.getAttribute('class') === 'discountPrice') {
                        constructor.price = em.innerHTML;
                    } else if (em.getAttribute('class') === 'card-price-without-discount') {
                        constructor.WithoutDiscount = em.innerHTML;
                    } else if (em.getAttribute('class') === 'card-price') {
                        constructor.price = em.innerHTML;
                        constructor.WithoutDiscount = null;
                    }
                })
            }

        })
        
        constructor.size = []
        card.find('span').each(function(i, e) {
            if (e.id == 'productId') {
                constructor.id = e.innerHTML;
            } else if (e.getAttribute('class') == 'size noactive') {
                constructor.size.push(e.innerHTML)
            }
        });

        return constructor;
    }

    function showOrderWindow(obj) {
        let getOrderWindow = $('.show-order-block');

        getOrderWindow.find('input').each(function(index, element) {
            if (element.name === 'prodcutId') {
                console.log(element)
                element.setAttribute('value', obj.id);
            }
        })

        getOrderWindow.find('div').each(function(index, element) {
            if (element.getAttribute('class') === 'order-img') {
                element.getElementsByTagName('img')[0].src = obj.image;
            }  else if (element.getAttribute('class') == 'order-name_price') {
                element.getElementsByClassName('order-name')[0].innerHTML = obj.name

                if (obj.WithoutDiscount !== null) {
                    let Withoutprice = element.getElementsByClassName('order-price');
                    Withoutprice[0].style.textDecoration = 'line-through';
                    Withoutprice[0].style.opacity = 0.6;
                    Withoutprice[0].style.color = '#333';
                    Withoutprice[0].innerHTML = obj.WithoutDiscount; 

                    let dics_price = element.getElementsByClassName('order-discount');
                    dics_price[0].style.display = 'block';
                    dics_price[0].style.fontWeight = 600;
                    dics_price[0].style.color = '#973F3F';
                    dics_price[0].innerHTML = obj.price
                } else {
                    let dics_price = element.getElementsByClassName('order-discount');
                    dics_price[0].style.display = 'none';

                    var price = element.getElementsByClassName('order-price');
                    price[0].style.textDecoration = 'none';
                    price[0].style.opacity = 1;
                    price[0].style.color = '#46A358';
                    price[0].innerHTML = obj.price;
                }
            }

            
        })
        
        const block = $('.sizes > div');
        block.empty()
        obj.size.map(e => {
            block.append("<span class='product-size'>" + e + "</span>");
            
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

        blur()

        let orderBlock = $('.order-block')

        orderBlock.removeClass('noactive').addClass('show').css({'top' : setPosition + 'px'});
        orderBlock[0].scrollIntoView();
        
    }

    $('.product-size').click(function(e) {

        $('.product-size').css({
            'border-color' : '#33333326',
            'color' : '#3333337a'
        }).removeClass('active-size')


        $(this).css({
            'border-color' : '#46A358',
            'color' : '#46A358'
        }).addClass('active-size');
    })

    function blur() {
        $('.page-container').css({
            'filter' : 'blur(2px)'
        });
        
        $('.header').css({
            'filter' : 'blur(2px)'
        });
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

    $('#btn-to_top').click(function() {
        window.scrollTo(0, 0)
    })

    $('.product-sizes label').click(function(e) {
        $('.product-sizes label').css({
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

    descriptionTxt()


    $('.form .submit').click(() => {
       const form = new FormData()

       form.append('name', 'Valerii');
       form.append('second_name', 'Diachenko');
       form.append('phone', '0962688640');
       form.append('userEmail', 'valera.dchn@gmail.com');
       form.append('productId', '8');

       fetch('/fastOrder', {
        'method' : 'POST',
        'body' : form
       })
       .then(status => console.log(status))
       .catch(err => console.log(err))
    })


    $('.btn-container .go-form-btn-order').click((e) => {
        $('.btn-container').css('display', 'none');

        $('.products-bckt .form-order').css('display', 'block');
    })

    $('#order-bckt-crosser').click(e => {
        reblur()

        $('.products-bckt-container').css('display', 'none');
        $('.products-bckt .form-order').css('display', 'none');
        $('.btn-container').css('display', 'block');

    })

    $('.header-nav-backet_btn').click(() => {
        blur()

        $('.products-bckt-container').fadeIn();

    })


    $('.bkt-btn').click(() => {
        
        if (document.querySelector('.active-size')) {
            Product.orderSize = document.querySelector('.active-size').innerHTML;
            console.log(Product)
            
            if (Product.WithoutDiscount !== null) {
                $('.bckt-orders').append(`<div class="order"><div class="bckt-img-container"><img src="${Product.image}"></div><div class="bckt-name_price"><div class="container"><p class="order-name">${Product.name} - ${Product.orderSize}</p><p class="order-price">${Product.price}</p></div><div class="btn-del"><button id="del">Прибрати з корзини</button></div></div><span class="prodcutId-bckt noactive">${Product.id}</span></div>`)
            } else {
                $('.bckt-orders').append(`<div class="order"><div class="bckt-img-container"><img src="${Product.image}"></div><div class="bckt-name_price"><div class="container"><p class="order-name">${Product.name} - ${Product.orderSize}</p><p class="order-price">${Product.price}</p></div><div class="btn-del"><button id="del">Прибрати з корзини</button></div></div><span class="prodcutId-bckt noactive">${Product.id}</span></div>`)
            }


        } else if (!document.querySelector('.invalid-size')) {
            $('.order-templates-container').append('<span class="invalid-size">Для додавання товару в корзину оберіть розмір</span>');
        } else {
            document.querySelector('.invalid-size').style.display = 'block';
        }
    })
  
});