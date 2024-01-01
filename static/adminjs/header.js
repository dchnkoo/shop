window.onload = () => {

    function beforeUnloadHandler(e) {
        e.returnValue = 'Не збережені дані можуть бути втрачені.';
    }

    function overHandler() {
        window.removeEventListener('beforeunload', beforeUnloadHandler);
    }
    
    function leaveHandler() {
        window.addEventListener('beforeunload', beforeUnloadHandler);
    }
    
    try {
        document.querySelector('#panel').addEventListener('mouseover', overHandler);
        document.querySelector('#panel').addEventListener('mouseleave', leaveHandler);
        window.addEventListener('beforeunload', beforeUnloadHandler);
    } catch {

    }


    try {
        const toSite = document.querySelector('#load_data_to_site');
        const toServer = document.querySelector('#load_data');
    
    
        toSite.onclick = async function(e) {
    
            toSite.disabled = true;
            toServer.disabled = true;
    
            toSite.style.background = '#919191';
            toSite.classList.add('loading');
    
            const post = await fetch(window.location + '/change', {
                'method': "POST",
                'body': JSON.stringify({
                    'type': 'load_data_to_site'
                })
            });
    
            const response = await post.json();
    
            if (response.status === 200) {
                toSite.disabled = false;
                toServer.disabled = false;
    
                toSite.style.background = '#6FFF57';
                toSite.classList.remove('loading');
                succesWindow()
                
            } else {
                toSite.disabled = false;
                toServer.disabled = false;
    
                toSite.style.background = '#6FFF57';
                toSite.classList.remove('loading');
    
                const windowModal = document.querySelector('.modal-window');
                const p = document.createElement('p');
                const infoElem = windowModal.querySelector('.info');
    
                p.innerText = response.load
                infoElem.append(p);
    
                windowModal.style.display = 'grid';
                windowModal.style.placeContent = 'center';
    
                const cancelBtn = windowModal.querySelector('#cancel');
                const okBtn = windowModal.querySelector('#ok');
    
                okBtn.innerText = 'OK';
                cancelBtn.style.display = 'none';
                
                okBtn.onclick = () => {
                    windowModal.style.display = 'none';
                    cancelBtn.style.display = 'block';
                    p.remove()
                }
            }
        }
    
        toServer.onclick = async function(e) {
    
            toServer.disabled = true;
            toSite.disabled = true;
    
            toServer.style.background = '#919191';
            toServer.classList.add('loading');
    
            const post = await fetch(window.location + '/change', {
                'method': "POST",
                'body': JSON.stringify({
                    'type': 'load_data'
                })
            });
    
            const response = await post.json();
    
            if (response.status === 200) {
                toServer.disabled = false;
                toSite.disabled = false;
    
                toServer.style.background = 'deepskyblue';
                toServer.classList.remove('loading');
                succesWindow()
                
            } else {
                toServer.disabled = false;
                toSite.disabled = false;
    
                toServer.style.background = 'deepskyblue';
                toServer.classList.remove('loading');
    
                const windowModal = document.querySelector('.modal-window');
                const p = document.createElement('p');
                const infoElem = windowModal.querySelector('.info');
    
                p.innerText = response.load
                infoElem.append(p);
    
                windowModal.style.display = 'grid';
                windowModal.style.placeContent = 'center';
    
                const cancelBtn = windowModal.querySelector('#cancel');
                const okBtn = windowModal.querySelector('#ok');
    
                okBtn.innerText = 'OK';
                cancelBtn.style.display = 'none';
                
                okBtn.onclick = () => {
                    windowModal.style.display = 'none';
                    cancelBtn.style.display = 'block';
                    p.remove()
                }
            }
        }
    } catch {


    }


    document.querySelectorAll('header > nav > ul > li').forEach(elem => {
        elem.onclick = e => {
            console.log(e.target)
            if (e.target.id === 'site') {
                window.open(window.location.origin)
            }
            if (e.target.id === 'panel') {
                const href = location.pathname;

                const url = href.replace(href.split('/')[href.split('/').length - 1], '')

                location.href = url.substring(0, url.length - 1)
            }
            
            if (e.target.id === 'orders') {
                document.querySelector('div#orders').scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'}) 
            }
            if (e.target.id === 'products') {
                document.querySelector('div#products').scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'}) 
            }
            if (e.target.id === 'addpr') {
                document.querySelector('div#add-product').scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'}) 
            }
        }
    })
}

function succesWindow() {
    document.querySelector('#success-add-container').style.animation = 'sc 0.2s ease-in forwards';
    document.querySelector('#success-add-container').style.top = (scrollY + 200) + 'px';
    document.querySelector('#success-add-container').style.left = '45%';
    document.querySelector('#success-add-container').style.display = 'grid';

    setTimeout(hide, 1800);
}

function hide() {
    document.querySelector('#success-add-container').style.animation = 'sr 0.2s ease-in forwards';
}