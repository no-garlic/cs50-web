document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    const quizForm = document.getElementById('quiz-form');
    
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect all answers
            const answers = {};
            const questionForms = document.querySelectorAll('.question-options');
            
            questionForms.forEach(form => {
                const radioButtons = form.querySelectorAll('input[type="radio"]');
                
                for (const radio of radioButtons) {
                    if (radio.checked) {
                        // Extract the question ID from the name (question_X)
                        const questionId = radio.name.split('_')[1];
                        answers[questionId] = radio.value;
                        break;
                    }
                }
            });
            
            // Set the answers data in the hidden input
            document.getElementById('answers-data').value = JSON.stringify(answers);
            
            // Submit the form
            this.submit();
        });
    }
    
    // Handle radio button clicks to update the visual state
    const radioLabels = document.querySelectorAll('.option-label');
    
    radioLabels.forEach(label => {
        label.addEventListener('click', function() {
            // Find the associated radio input
            const radioInput = document.getElementById(this.getAttribute('for'));
            
            // Get all radio buttons in this question group
            const questionOptions = this.closest('.question-options');
            const allRadioButtons = questionOptions.querySelectorAll('.radio-button');
            
            // Remove the selected class from all radio buttons
            allRadioButtons.forEach(rb => rb.classList.remove('selected'));
            
            // Add the selected class to the clicked radio button
            const clickedRadioButton = this.querySelector('.radio-button');
            clickedRadioButton.classList.add('selected');
        });
    });
});