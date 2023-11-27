window.onload = () => {
    document.querySelectorAll('header > nav > ul > li').forEach(elem => {
        elem.onclick = e => {
            console.log(e)
            if (e.target.id === 'orders') {
                document.querySelector('div#orders').scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'}) 
            }
            if (e.target.id === 'products') {
                document.querySelector('div#products').scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'}) 
            }
            if (e.target.id === 'add-pr') {
                document.querySelector('div#add-product').scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'}) 
            }
        }
    })
}