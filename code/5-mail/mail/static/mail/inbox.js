
document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email(null));

    // Submit the email
    document.querySelector('form').onsubmit = submit_email;

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(email = null) { 
    // Show compose view and hide other views
    document.querySelector('#mailbox-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Check if we are replying to an email
    if (email) {
        // Pre-fill composition fields for reply
        document.querySelector('#compose-recipients').value = email.sender;
        
        // Check if subject already starts with "Re: ", if not then prepend it
        let subject = email.subject;
        if (!subject.startsWith('Re: ')) {
            subject = `Re: ${subject}`;
        }
        document.querySelector('#compose-subject').value = subject;

        // Pre-fill body with quoted original email
        document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;

        // Place cursor at the beginning of the body
        document.querySelector('#compose-body').focus();
        document.querySelector('#compose-body').setSelectionRange(0, 0);
    } else {
        // Clear out composition fields for new email
        document.querySelector('#compose-recipients').value = '';
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
    }
}

function submit_email() {
    // Get the email content
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
      })
      .then(response => response.json())
      .then(result => {
          // Load the sent mailbox after sending the email
          load_mailbox('sent')
      })
      .catch(error => {
          // Show the error message in the email view
          console.error('Error sending email:', error);
          const emailView = document.querySelector('#email-view');
          emailView.innerHTML = '<p>Error sending email.</p>';
      });

      // Prevent the form from submitting
    return false;
}

function load_mailbox(mailbox) {  
    // Show the mailbox and hide other views
    document.querySelector('#mailbox-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#mailbox-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Fetch the mailbox items
    fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
        // Iterate over the emails and create an item for each
        emails.forEach(contents => show_mailbox_item(contents, mailbox)); 
    })
    .catch(error => {
        // Show the error message in the mailbox view
        console.error('Error loading mailbox:', error);
        document.querySelector('#mailbox-view').innerHTML = '<p>Error loading mailbox.</p>';
    });
}

function show_mailbox_item(contents, mailbox) { 
    // Create a div for the email item
    const email = document.createElement('div');
    email.classList.add('email-item');
    
    // Set background color based on read status
    if (!contents.read) {
        email.classList.add('email-item-unread');
    }

    // Add click event listener to the email div
    email.addEventListener('click', () => show_email(contents.id, mailbox)); 

    // Create container for sender and subject
    const leftContainer = document.createElement('div');
    leftContainer.classList.add('email-left-container');

    // Create sender element (bold)
    const senderSpan = document.createElement('span');
    senderSpan.classList.add('email-sender');
    senderSpan.textContent = contents.sender;

    // Create subject element
    const subjectSpan = document.createElement('span');
    subjectSpan.classList.add('email-subject');
    subjectSpan.textContent = contents.subject;

    // Append sender and subject to the left container
    leftContainer.append(senderSpan);
    leftContainer.append(subjectSpan);

    // Create timestamp element
    const timestampSpan = document.createElement('span');
    timestampSpan.classList.add('email-timestamp');
    timestampSpan.textContent = contents.timestamp;

    // Add the content to the div
    email.append(leftContainer);
    email.append(timestampSpan);

    // Add the div to the view
    document.querySelector('#mailbox-view').append(email);
}

function show_email(id, mailbox) { // Accept mailbox here
    // Show the email view and hide other views
    document.querySelector('#mailbox-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Mark the email as read
    fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {
        // Mark the email as read
        mark_email_read(id);

        // Get the email view and clear it
        emailView = document.querySelector('#email-view')
        emailView.innerHTML = '';

        // Display the email header
        const headerDiv = document.createElement('div');
        headerDiv.innerHTML = `
            <div class="email-header-line"><strong class="email-header-label">From:</strong> ${email.sender}</div>
            <div class="email-header-line"><strong class="email-header-label">To:</strong> ${email.recipients.join(', ')}</div>
            <div class="email-header-line"><strong class="email-header-label">Subject:</strong> ${email.subject}</div>
            <div class="email-header-line"><strong class="email-header-label">Timestamp:</strong> ${email.timestamp}</div>
        `;
        emailView.append(headerDiv);

        // Add Reply button
        const replyButton = document.createElement('button');
        replyButton.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'email-button');
        replyButton.textContent = 'Reply';
        replyButton.addEventListener('click', () => reply_to_email(email));
        emailView.append(replyButton);

        // Add Archive/Unarchive button only if not in 'sent' mailbox
        if (mailbox !== 'sent') {
            if (email.archived === false) {
                const archiveButton = document.createElement('button');
                archiveButton.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'email-button');
                archiveButton.textContent = 'Archive';
                archiveButton.addEventListener('click', () => archive_email(email.id));
                emailView.append(archiveButton);
            } else {
                const archiveButton = document.createElement('button');
                archiveButton.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'email-button');
                archiveButton.textContent = 'Unarchive';
                archiveButton.addEventListener('click', () => unarchive_email(email.id));
                emailView.append(archiveButton);
            }
        }

        // Add horizontal line
        const hr = document.createElement('hr');
        emailView.append(hr);

        // Display email body
        const bodyDiv = document.createElement('div');
        bodyDiv.classList.add('email-body-content');
        bodyDiv.textContent = email.body;
        emailView.append(bodyDiv);
    })
    .catch(error => {
        // Show the error message in the email view
        console.error('Error fetching email:', error);
        emailView.innerHTML = '<p>Error loading email.</p>';
    });
}

function mark_email_read(id) {
    console.log('marking email [' + id + '] as read');
    fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
    .catch(error => {
        // Show the error message in the email view
        console.error('Error marking email as read:', error);
    });
}

function archive_email(id) {
    console.log('archiving email [' + id + ']');
    fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    })
    .then(email => {
        // Load the inbox after archiving
        load_mailbox('inbox');
    })    
    .catch(error => {
        // Show the error message in the email view
        console.error('Error archiving email:', error);
    });
}

function unarchive_email(id) {
    console.log('unarchiving email [' + id + ']');
    fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
    })
    .then(email => {
        // Load the inbox after unarchiving
        load_mailbox('inbox');
    })
    .catch(error => {
        // Show the error message in the email view
        console.error('Error unarchiving email:', error);
    });
}

function reply_to_email(email) { 
    // Compose a new email using the original email's details
    compose_email(email);
}
