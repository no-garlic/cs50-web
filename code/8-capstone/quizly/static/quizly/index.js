document.addEventListener('DOMContentLoaded', function() {
    // Set up the hero button click handler
    const heroButton = document.querySelector('.hero-btn');
    if (heroButton) {
        heroButton.addEventListener('click', function() {
            window.location.href = '/browse';
        });
    }
});