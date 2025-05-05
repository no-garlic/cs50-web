document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // Submit the email
    document.querySelector('form').onsubmit = submit_email;

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function submit_email() {
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
          console.log(result);
          load_mailbox('sent')
      });
    return false;
}

function load_mailbox(mailbox) {
  
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Fetch the mailbox items
    fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
        console.log(emails);
        emails.forEach(show_email);
    });
}

function show_email(contents) {
    const email = document.createElement('div');

    // Add styles for border, padding, and flex display for columns
    email.style.border = '1px solid black';
    email.style.padding = '10px 5px';
    email.style.display = 'flex';
    email.style.justifyContent = 'space-between';
    email.style.alignItems = 'center';

    // Create container for sender and subject
    const leftContainer = document.createElement('div');
    leftContainer.style.display = 'flex';
    leftContainer.style.alignItems = 'center';

    // Create sender element (bold)
    const senderSpan = document.createElement('span');
    senderSpan.style.fontWeight = 'bold';
    senderSpan.textContent = contents.sender;
    senderSpan.style.width = '220px'; 

    // Create subject element
    const subjectSpan = document.createElement('span');
    subjectSpan.style.marginLeft = '10px';
    subjectSpan.textContent = contents.subject;

    // Append sender and subject to the left container
    leftContainer.append(senderSpan);
    leftContainer.append(subjectSpan);

    // Create timestamp element
    const timestampSpan = document.createElement('span');
    timestampSpan.style.color = 'gray';
    timestampSpan.style.fontSize = '0.9em';
    timestampSpan.textContent = contents.timestamp;

    // Add the content to the div
    email.append(leftContainer);
    email.append(timestampSpan);

    // Add the div to the view
    document.querySelector('#emails-view').append(email);
}