document.getElementById('showSignUp').addEventListener('click', function() {
    console.log('Signup trigger clicked');
    document.getElementById('loginSection').style.display = 'none'; // Hide login section
    document.getElementById('signUpSection').style.display = ''; // Show sign-up section
});

document.getElementById('showLogin').addEventListener('click', function() {
    console.log('Login trigger clicked');
    document.getElementById('signUpSection').style.display = 'none'; // Hide sign-up section
    document.getElementById('loginSection').style.display = ''; // Show login section
});

window.addEventListener('DOMContentLoaded', (event) => {
    const urlParams = new URLSearchParams(window.location.search);
    const scrollTo = urlParams.get('scrollTo');

    if (scrollTo) {
        const section = document.getElementById(scrollTo);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }
});
