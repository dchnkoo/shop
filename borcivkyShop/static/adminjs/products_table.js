document.querySelectorAll('.products-container table > tbody > tr > td:not(td#input)').forEach(elem => 
    {
        elem.onclick = e => {
            console.log(e.target.getAttribute('class'))
            location.href = window.location + '/product?id=' + e.target.getAttribute('class')
    }
    })


    document.querySelectorAll('.products-container table > tbody > tr > td > input').forEach(elem => {
        elem.onchange = e => {
            fetch(window.location + '/change', {
                'method' : 'POST',
                'headers' : {'Content-type' : 'application/json'},
                'body' : JSON.stringify({
                    'type' : e.target.id,
                    'id' : e.target.classList[0],
                    'value' : e.target.value
                })
            }).then(data => data.json())
            .then(obj => {
                if (obj.code === 200) {
                    succesWindow()
                } else if (obj.code === 400) {
                    let msg = `Код помилки: ${obj.code}. Товар id: ${obj.id}. Повідомлення: ${obj.msg}`;
                    createErrorMsg(msg);
                }
            })
        }
    })
    

    function succesWindow() {
        document.querySelector('#success-add-container').style.animation = 'sc 0.2s ease-in forwards';
        document.querySelector('#success-add-container').style.top = (scrollY + 200) + 'px';
        document.querySelector('#success-add-container').style.left = '45%';
        document.querySelector('#success-add-container').style.display = 'grid';

        setTimeout(hide, 1800);
    }

    function createErrorMsg(msg) {
        pr = document.querySelector('.products-container > div');

        if (pr.querySelector('.error-msg')) {
            pr.querySelector('.error-msg').innerText = msg
        } else {
            let p = document.createElement('p');
            p.classList.add('error-msg');
            p.style.color = 'red';
            p.style.fontWeight = 'bold';
            p.innerText = msg;

            pr.append(p)
        }

        setTimeout(deleteElem, 10000, ['.error-msg'])
    }

    function deleteElem($selector) {
        document.querySelector($selector).remove()
    }

    function hide() {
        document.querySelector('#success-add-container').style.animation = 'sr 0.2s ease-in forwards';
    }


    document.querySelectorAll('.delete-ptoduct').forEach(elem => {
        elem.onclick = e => {
            const windowModal = document.querySelector('.modal-window');
            const p = document.createElement('p');
            const infoElem = windowModal.querySelector('.info');

            p.innerText = `Видалити товар з id ${e.target.id} ?`
            infoElem.append(p);

            windowModal.style.display = 'grid';
            windowModal.style.placeContent = 'center';

            const cancelBtn = windowModal.querySelector('#cancel');
            const okBtn = windowModal.querySelector('#ok');

            cancelBtn.onclick = () => {
                windowModal.style.display = 'none';
                p.remove()
            }

            okBtn.onclick = () => {
                fetch(window.location + '/change', {
                    'method' : 'DELETE',
                    'headers' : {'Content-type' : 'application/json'},
                    'body' : JSON.stringify({
                        'id' : e.target.id
                    })
                })
                .then(data => data.json())
                .then(d => {
                    if (d.code === 200) {
                        windowModal.style.display = 'none';
                        p.remove()
                        succesWindow();

                        document.querySelector(`.products-container > table > tbody`).querySelectorAll('tr').forEach(elem => {
                            if (elem.classList[0] === e.target.id) {
                                elem.remove()
                            }
                        });
                    } else {
                        p.innerText = d.msg;
                    }
                })
            }
        }
    })