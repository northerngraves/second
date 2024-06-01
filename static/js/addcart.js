document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            var notification = document.getElementById('cart-notification');
            notification.classList.remove('hidden');
            
            setTimeout(function() {
                notification.classList.add('hidden');
            }, 1000); // Уведомление будет отображаться 3 секунды
        });
    });
});