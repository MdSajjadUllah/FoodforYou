document.addEventListener('DOMContentLoaded', () => {
    const orderList = document.getElementById('order-list');
    const orders = JSON.parse(localStorage.getItem('orders')) || [];

    if (orders.length === 0) {
        orderList.innerHTML = "<p>No previous orders found.</p>";
        return;
    }

    orders.reverse().forEach((order, index) => {
        const div = document.createElement('div');
        div.className = 'order-item';

        let totalPrice = 0;
        order.cartItems.forEach(item => {
            totalPrice += item.price * item.quantity;
        });

        div.innerHTML = `
            <h3>Order-${index + 1}</h3>
            <p><strong>Time:</strong> ${order.orderTime}</p>
            <p><strong>Address:</strong> ${order.street}, Apt: ${order.apartment}, ${order.fullLocation}</p>
            <p><strong>Payment:</strong> ${order.paymentMethod}</p>
            <p><strong>Items:</strong></p>
            <ul>
                ${order.cartItems.map(item => `<li>${item.name} x${item.quantity} - ৳${item.price}</li>`).join('')}
            </ul>
            <p><strong>Total:</strong> ৳${totalPrice.toFixed(2)}</p>
        `;
        orderList.appendChild(div);
    });
});
