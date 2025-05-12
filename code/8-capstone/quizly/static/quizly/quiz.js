document.addEventListener('DOMContentLoaded', function() {
    // Initialize rating popup functionality
    initRatingSystem();
    
    // Initialize save for later functionality
    initSaveForLater();
});

function initRatingSystem() {
    const rateButton = document.querySelector('.quiz-btn:has(i.bi-star)');
    if (!rateButton)
        return;
    
    rateButton.addEventListener('click', function() {
        // Get user's previous rating if it exists
        const userRating = parseInt(this.dataset.userRating) || 0;
        
        // Create and show the rating popup
        showRatingPopup(userRating);
    });
}

function initSaveForLater() {
    const saveButton = document.getElementById('save-for-later');
    if (!saveButton)
        return;
    
    saveButton.addEventListener('click', function() {
        // Get the quiz ID from the URL
        const path = window.location.pathname;
        const quizId = path.split('/').pop();
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Send the save for later request
        fetch('/save_for_later', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `quiz_id=${quizId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update the button appearance and text
                const icon = saveButton.querySelector('i');
                const isSaved = data.is_saved;
                
                if (isSaved) {
                    icon.classList.remove('bi-bookmark');
                    icon.classList.add('bi-bookmark-fill');
                    saveButton.textContent = '';
                    saveButton.appendChild(icon);
                    saveButton.appendChild(document.createTextNode('Saved For Later'));
                    saveButton.dataset.saved = 'true';
                } else {
                    icon.classList.remove('bi-bookmark-fill');
                    icon.classList.add('bi-bookmark');
                    saveButton.textContent = '';
                    saveButton.appendChild(icon);
                    saveButton.appendChild(document.createTextNode('Save For Later'));
                    saveButton.dataset.saved = 'false';
                }
            }
        })
        .catch(error => {
            console.error('Error saving quiz for later:', error);
        });
    });
}

function showRatingPopup(userRating = 0) {
    // Create the popup container
    const popup = document.createElement('div');
    popup.classList.add('rating-popup');
    
    // Create popup content
    popup.innerHTML = `
        <div class="rating-popup-content">
            <h3>Rate</h3>
            <div class="stars-container">
                ${Array(5).fill().map((_, i) => 
                    `<i class="bi bi-star star-rating" data-rating="${i+1}"></i>`
                ).join('')}
            </div>
        </div>
    `;
    
    // Add popup to the body
    document.body.appendChild(popup);
    
    // Add event listeners to stars
    const stars = popup.querySelectorAll('.star-rating');
    
    // Initialize with user's previous rating if available
    if (userRating > 0) {
        updateStars(stars, userRating);
    }
    
    stars.forEach(star => {
        // Hover effect
        star.addEventListener('mouseenter', function() {
            const rating = parseInt(this.dataset.rating);
            updateStars(stars, rating);
        });
        
        // Click to rate
        star.addEventListener('click', function() {
            const rating = parseInt(this.dataset.rating);
            submitRating(rating);
            
            // Update the button's data attribute with the new rating
            document.querySelector('.quiz-btn:has(i.bi-star)').dataset.userRating = rating;
            
            // Close popup after delay
            setTimeout(() => {
                popup.classList.add('fade-out');
                setTimeout(() => {
                    popup.remove();
                }, 300);
            }, 500);
        });
    });
    
    // Reset stars when mouse leaves the container, but only if no rating was previously selected
    const starsContainer = popup.querySelector('.stars-container');
    starsContainer.addEventListener('mouseleave', function() {
        if (userRating > 0) {
            updateStars(stars, userRating);
        } else {
            resetStars(stars);
        }
    });
    
    // Close popup when clicking outside
    popup.addEventListener('click', function(e) {
        if (e.target === popup) {
            popup.remove();
        }
    });
    
    // Animation to show popup
    setTimeout(() => {
        popup.classList.add('active');
    }, 10);
}

// Update stars visual based on selected rating
function updateStars(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('bi-star');
            star.classList.add('bi-star-fill');
        } else {
            star.classList.remove('bi-star-fill');
            star.classList.add('bi-star');
        }
    });
}

// Reset all stars to empty
function resetStars(stars) {
    stars.forEach(star => {
        star.classList.remove('bi-star-fill');
        star.classList.add('bi-star');
    });
}

// Submit the rating via AJAX
function submitRating(rating) {
    // Get the quiz ID from the URL
    const path = window.location.pathname;
    const quizId = path.split('/').pop();
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Send the rating
    fetch('/rate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `quiz_id=${quizId}&rating=${rating}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Could add a success notification here
            console.log('Rating submitted successfully');
            
            // Optionally refresh the page to show updated average rating
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error submitting rating:', error);
    });
}