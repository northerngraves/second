var updateButtons = document.getElementsByClassName('cart-button')
console.log(window.location.pathname)

for (var i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId, action)

        console.log(user)
        if (user === 'AnonymousUser'){
            console.log('Not logged in')
        } else {
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({
            'productId': productId,
            'action': action
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log(data)
        // Проверяем, находится ли пользователь на конкретной странице, например /about
        if (window.location.pathname === '/cart/') {
            location.reload()
        }
    })
}