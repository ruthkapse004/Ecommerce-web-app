let updateCartButtons = document.getElementsByClassName("update-cart")

for(let i = 0; i < updateCartButtons.length; i++) {
    updateCartButtons[i].addEventListener("click", function(){
        let productId = this.dataset.product
        let action = this.dataset.action

        console.log("USER", user)
        if(anonymousUser) {
            updateCookieItem(productId, action)
        }
        else {
            updateUserCart(productId, action)
        }
    })
}

// When user is AnonymousUser we use the cookies to get the cart.
function updateCookieItem(productId, action) {
    
    if(action == "add") {
        // cart[productId]["quantity"] = cart[productId]["quantity"] ?? 0 + 1
        if(!cart[productId]) {
            cart[productId] = {"quantity": 1}
        }
        else {
            cart[productId]["quantity"] += 1
        }
    }
    else if(action == "remove") {
        cart[productId]["quantity"] -= 1
    }

    if(action == "delete" || cart[productId]["quantity"] <= 0 ) {
        delete cart[productId]
    }

    // console.log("addcookie", cart)
    setCookie("cart", cart)
    location.reload()
}

// When user is Authorized update cart in database.
function updateUserCart(productId, action){
    console.log("User is Logged In.", productId, action)

    const url = "/update_cart_item/"

    fetch(url, {
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            "productId": productId, "action": action,
        })
    })
    
    // Promise
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log("data:", data)
        location.reload()
    })
    .catch(error => {
        console.error('Error updating cart:', error);
    })
}
