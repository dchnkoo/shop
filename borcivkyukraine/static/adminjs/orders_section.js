function showElem($el, $el2) {
    $el.scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'})
    $el.style.background = 'yellow';
    $el2.value = '';

    $el.onclick = () => {
        $el.style.background = '#fff';
    }
}

searching('.orders-container > div > .search-order > div button',
        '.orders-container > div > .search-order > div input',
        '.orders-container > table > tbody > tr');
        
searching('.products-container > div > .search-product > div button',
        '.products-container > div > .search-product > div input',
        '.products-container > table > tbody > tr');


function searching($sel1, $sel2, $sel3) {
    document.querySelector($sel1).onclick = elem => {
        const text = document.querySelector($sel2);

        document.querySelectorAll($sel3).forEach(elem => {
            Array.from(elem.getElementsByTagName('td')).forEach(el => {
                if (el.getElementsByTagName('abbr').length > 0) {
                    if (text.value === el.getElementsByTagName('abbr')[0].innerHTML) {
                        showElem(elem,text)
                    } 
                }
                if (el.getElementsByTagName('a').length > 0) {
                    if (text.value === el.getElementsByTagName('a')[0].innerText) {
                        showElem(elem, text)
                    }
                }

                if (text.value === el.innerHTML) {
                    showElem(elem, text);
                }
            })
        })
    }
}