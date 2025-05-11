document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('checkout-form');

    if (!form) {
        console.error("Checkout form not found!");
        return;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const street = document.getElementById('street')?.value || "";
        const apartment = document.getElementById('apartment')?.value || "";
        const fullLocation = document.getElementById('full_location')?.value || "";
        const paymentMethod = document.getElementById('paymentMethod')?.value || "";

        const cart = JSON.parse(localStorage.getItem('cart')) || {};

        if (Object.keys(cart).length === 0) {
            alert("Cart is empty!");
            return;
        }

        const cartItems = Object.values(cart);

        const orderData = {
            street,
            apartment,
            fullLocation,
            paymentMethod,
            cartItems,
            orderTime: new Date().toLocaleString()
        };

        let orders = JSON.parse(localStorage.getItem('orders')) || [];
        orders.push(orderData);
        localStorage.setItem('orders', JSON.stringify(orders));

        localStorage.removeItem('cart');

        window.location.href = orderConfirmationUrl;
    });
});
