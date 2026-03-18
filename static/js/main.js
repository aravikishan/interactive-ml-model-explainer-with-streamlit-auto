document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    const smoothScroll = function(target) {
        document.querySelector(target).scrollIntoView({
            behavior: 'smooth'
        });
    };

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            smoothScroll(this.getAttribute('href'));
        });
    });

    const predictForm = document.getElementById('predict-form');
    if (predictForm) {
        predictForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const feature1 = document.getElementById('feature1').value;
            const feature2 = document.getElementById('feature2').value;
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ feature1: parseInt(feature1), feature2: parseInt(feature2) })
            });
            const data = await response.json();
            document.getElementById('prediction-result').innerHTML = `<p>Prediction: ${data.prediction}</p><p>Explanation: ${data.explanation}</p>`;
        });
    }
});