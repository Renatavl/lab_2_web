document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registration-form');
    registrationForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(registrationForm);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        try {
            const csrfToken = document.querySelector(
                '[name=csrfmiddlewaretoken]',
            ).value;
            const response = await fetch('/register/', {
                // код 15-22 робить запит до сетвера
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(formObject),
            });

            if (!response.ok) {
                const errorMessage = await response.json(); // зчитуємо помилку з респонсу
                alert(errorMessage.message);
                return;
            }

            window.location.href = '/login/'; // переспрямування на сторінуку, після успішного виконання
        } catch (error) {
            alert('Something went wrong');
        }
    });
});
