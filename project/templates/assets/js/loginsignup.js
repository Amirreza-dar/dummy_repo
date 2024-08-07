document.getElementById('showSignUp').addEventListener('click', function() {
    document.getElementById('loginSection').style.display = 'none'; // Hide login section
    document.getElementById('signUpSection').style.display = ''; // Show sign-up section
});

document.getElementById('showLogin').addEventListener('click', function() {
    document.getElementById('signUpSection').style.display = 'none'; // Hide sign-up section
    document.getElementById('loginSection').style.display = ''; // Show login section
});
