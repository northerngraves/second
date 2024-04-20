function submitData() {
    const orderType = document.querySelector('input[name="delivery"]:checked').value;
    const address = document.getElementById('textInput').value;
    const paymentType = document.querySelector('input[name="payment"]:checked').value;

    const data = {
        orderType,
        address,
        paymentType
    };

    fetch('/update_checkout/', {  // Замените 'your-url-here' на ваш URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        window.location.replace(completePage)
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}