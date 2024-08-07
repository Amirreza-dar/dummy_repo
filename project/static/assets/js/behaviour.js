document.getElementById('toGame').addEventListener('click', function(e) {
    e.preventDefault();  // Prevent the default action

    // Select all radio inputs within the form
    var radioInputs = document.querySelectorAll('#userChoicesForm input[type="radio"]');

    // Check if any radio input is checked
    var isOptionSelected = Array.from(radioInputs).some(radio => radio.checked);

    if (!isOptionSelected) {
        alert("Please select an option before proceeding.");  // Notify the user
        return;  // Do not proceed with form submission
    }

    // If an option is selected, proceed with form submission
    var formData = new FormData(document.getElementById('userChoicesForm'));
    
    // Perform the AJAX call
    fetch('/save-user-choices', {
        method: 'POST',
        body: formData
    }).then(response => {
        // Handle response
        if(response.ok) {
            // Option to redirect or perform other actions after successful submission
            console.log('Form submitted successfully');
            // window.location.href = '/next-page';  // Redirect if needed
        }
    }).catch(error => {
        console.error('Error submitting form:', error);
    });

    document.getElementById('highlights').scrollIntoView({behavior: 'smooth'});
});



document.getElementById('gameSelectionForm').addEventListener('submit', function(e) {

    e.preventDefault(); // Prevent form from submitting normally

    var selectedGame = document.querySelector('#gameSelectionForm input[type="radio"]:checked');

    // If no game is selected, alert the user and stop the submission process
    if (!selectedGame) {
        alert("Please select a game before submitting.");
        return;  // Exit the function, preventing form submission
    }

    var gameData = new FormData(this);
    // AJAX call to send gameData to server
    fetch('/save-game-selection', {
        method: 'POST',
        body: gameData
    }).then(response => {
        if(response.ok) {
            // window.location.href = '/footer'; // Redirect to play page if successful
            document.getElementById('summary').scrollIntoView({behavior: 'smooth'});
            
        }
    });
    
    console.log("Selected game:", selectedGame.value);

});



// a:link { color: #FF0000; } /* Unvisited links */
// a:visited { color: #00FF00; } /* Visited links */
// a:hover { color: #0000FF; } /* Links when mouse hovers over them */
// a:active { color: #FFFF00; } /* Links at the moment they are clicked */
