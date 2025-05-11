let cart = {};

function addToCart(id, name, price) {
    if (!cart[id]) {
        cart[id] = { name: name, price: price, quantity: 1 };
    } else {
        cart[id].quantity++;
    }
    updateCart();
}

function removeFromCart(id) {
    delete cart[id];
    updateCart();
}

function updateCart() {
    const cartList = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    cartList.innerHTML = '';
    let total = 0;

    Object.keys(cart).forEach(id => {
        const item = cart[id];
        const li = document.createElement('li');
        li.innerHTML = `${item.name} (x${item.quantity}) - ৳${item.price * item.quantity} 
            <button onclick="removeFromCart(${id})">🗑️</button>`;
        cartList.appendChild(li);
        total += item.price * item.quantity;
    });

    cartTotal.textContent = total.toFixed(2);
}

function goToCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    window.location.href = "/cart/";
}
