$(document).ready(function() {
    ProfileUpdateInformation();
});

function ProfileUpdateInformation() {
    $.ajax({
        url: '/get_session_data',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            // Update the <p> tags with the session data
            console.log(response);
            $('#intro .highlight:eq(1) p').text(response.readiness);
            $('#intro .highlight:eq(2) p').text(response.accuracy);
            $('#intro .highlight:eq(3) p').text(response.challenge);
            $('#intro .highlight:eq(4) p').text(response.impact);
            // Scroll to the information section
            // $('html, body').animate({
            //     scrollTop: $("section.resutls").first().offset().top
            // }, 1000);
            
        },
        error: function(xhr, status, error) {
            console.error("Error fetching session data:", error);
        }
    });
}
