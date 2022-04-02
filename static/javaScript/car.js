var updateBtn = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('prodcutId: ', productId, 'action: ', action)

        console.log('USER:', user)

        if (user == 'AnonymousUser'){
            console.log("User is not authenticated")
        }else{
            console.log("prodcutId:", productId)
            console.log("action:", action)
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data..')

    var url = 'update-item'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            
        },
        mode: 'same-origin',
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((reponse)=>{
        return reponse.json()
    })

    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}