document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
        const jsonData = JSON.stringify(formObject);

        try {
            const csrfToken = document.querySelector(
                '[name=csrfmiddlewaretoken]',
            ).value;
            const response = await fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: jsonData,
            });

            if (!response.ok) {
                const errorMessage = await response.json();
                alert(errorMessage.message);
                return;
            }
            window.location.href = '/';
        } catch (error) {
            alert('Something went wrong');
        }
    });
});
