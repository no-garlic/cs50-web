
document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#follow-button').onclick = () => {        
        const follow_button = document.querySelector('#follow-button');
        const id = follow_button.dataset.user;

        fetch('/follow/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
        })
        .then(response => response.json())
        .then(json_data => {
            follow_button.innerHTML = json_data.label;
        })
        .catch(error => {
            console.error('Error updating the following status:', error);
        });
    }
});
