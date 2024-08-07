// answer to questions:
// console.log('it"s working')
document.addEventListener('DOMContentLoaded', function() {
    // console.log('page loaded!')
    let selectedAnswers = {};

    // Handle answer option clicks
    document.querySelectorAll('.answer-option').forEach(item => {
        // console.log('page loaded!')
        item.addEventListener('click', function(e) {
            e.preventDefault();

            // Store the selected answer
            // const questionId = this.closest('section').id;
            const questionId = this.closest('.wrapper').id; 
            const answer = this.dataset.answer;
            selectedAnswers[questionId] = answer;
            console.log('Button clicked!', answer, questionId)
            // Optionally, visually indicate the selected option
        });
    });

    // Handle the Next button click
    document.querySelectorAll('.next-question').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            // Send the selected answer for the current question to the server
            const questionId = this.closest('section').id;
            const answer = selectedAnswers[questionId];
            console.log(questionId, selectedAnswers[questionId])

            if (!answer) {
                alert('Please select an option before proceeding.');
                return;
            }

            fetch('/save-answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ questionId, answer })
            }).then(response => {
                if (response.ok) {

                    console.log('Answer submitted')
                    // Scroll to the next section
                    const nextSection = document.querySelector(this.getAttribute('href'));
                    
                    if (nextSection) {
                        // console.log('been here', nextSection)
                        if (questionId == 'q3'){
                            console.log('last question submitted!')
                            updateInformation();
                        }
                        else{
                            nextSection.scrollIntoView({ behavior: 'smooth' });
                        }
                    }
                } else {
                    // Handle errors
                    console.error('Failed to save answer');
                }
            });
        });
    });
});

// $(document).ready(function() {
//     updateInformation();
// });

function updateInformation() {
    $.ajax({
        url: '/get_session_data',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            // Update the <p> tags with the session data
            console.log(response);
            $('#results .highlight:eq(1) p').text(response.readiness);
            $('#results .highlight:eq(2) p').text(response.accuracy);
            $('#results .highlight:eq(3) p').text(response.challenge);
            $('#results .highlight:eq(4) p').text(response.impact);
            // Scroll to the information section
            // $('html, body').animate({
            //     scrollTop: $("section.resutls").first().offset().top
            // }, 1000);
            $('html, body').animate({
                scrollTop: $("#results").offset().top
            }, 1000);
            
        },
        error: function(xhr, status, error) {
            console.error("Error fetching session data:", error);
        }
    });
}

