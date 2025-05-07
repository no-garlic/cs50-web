
document.addEventListener('DOMContentLoaded', function() {
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (isAuthenticated) {
        load();
    }
});


function load() {
    document.querySelector('#follow-button')?.addEventListener('click', follow);

    document.querySelectorAll('[id^="post-edit-button-"]')
        .forEach(button => button.onclick = () => edit_post(button));

    document.querySelectorAll('[id^="post-likes-"]')
        .forEach(div => div.onclick = () => like(div))
}


function follow() {
    const follow_button = document.querySelector('#follow-button');
    const user_id = follow_button.dataset.user;

    fetch('/follow', {
        method: 'PUT',
        body: JSON.stringify({
            user_id: user_id
        })
    })
    .then(response => response.json())
    .then(json_data => {
        follow_button.innerHTML = json_data.label;
        document.querySelector('#followers-count').innerHTML = `Followers: ${json_data.followers_count}`;
    })
    .catch(error => {
        console.error('Error updating the following status:', error);
    });
}


function like(div) {
    const post_id = div.dataset.id;
    const post_heart = div.querySelector('.heart');
    const post_count = div.querySelector('.like-count')

    fetch('/like', {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => response.json())
    .then(json_data => {
        console.log(json_data.does_like)
        post_count.innerHTML = json_data.likes_count;
        div.classList.toggle('liked', json_data.does_like)
    })
    .catch(error => {
        console.error('Error updating the like status:', error);
    });
}


function edit_post(button) {
    const post_id = button.dataset.id;

    const post_view = document.querySelector('#post-view-' + post_id);
    const post_edit = document.querySelector('#post-edit-' + post_id);
    const post_edit_button = document.querySelector('#post-edit-button-' + post_id);
    const post_save_button = document.querySelector('#post-save-button-' + post_id);
    const post_cancel_button = document.querySelector('#post-cancel-button-' + post_id);
    const post_edit_textarea = post_edit.children[0];

    post_view.style.display = 'none';
    post_edit.style.display = 'block';
    post_edit_button.style.display = 'none';
    post_save_button.style.display = 'inline-block';
    post_cancel_button.style.display = 'inline-block';
    post_edit_textarea.value = post_view.innerHTML;

    post_cancel_button.onclick = () => {
        post_view.style.display = 'block';
        post_edit.style.display = 'none';
        post_edit_button.style.display = 'inline-block';
        post_save_button.style.display = 'none';
        post_cancel_button.style.display = 'none';
        post_edit_textarea.value = '';
    }

    post_save_button.onclick = () => {
        fetch('/update', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: post_id,
                content: post_edit_textarea.value
            })
        })
        .then(response => response.json())
        .then(json_data => {
            post_view.style.display = 'block';
            post_edit.style.display = 'none';
            post_edit_button.style.display = 'inline-block';
            post_save_button.style.display = 'none';
            post_cancel_button.style.display = 'none';
            post_view.innerHTML = post_edit_textarea.value;
        })
        .catch(error => {
            console.error('Error saving the post:', error);
        });
    }
}

