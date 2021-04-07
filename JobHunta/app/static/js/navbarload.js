/* Function to run once navbar has loaded */
function navLoaded()
{
    var path = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1);
    if (path == 'home')
        $('#home').addClass('active');
    else if (path == 'login')
        $('#login').addClass('active');
    else if (path == 'signup')
        $('#signup').addClass('active');
    else if (path == 'watchlist')
        $('#watchlist').addClass('active');
    else if (path == 'profile')
        $('#profile').addClass('active');
    else if (path == 'newsfeed')
        $('#newsfeed').addClass('active');
}


/* loads the header component*/
$(function(){
    $("#nav").load("components/navbar.html", navLoaded);
});

/* loads the footer component*/
$(function(){
    $("#footer").load("components/footer.html");
});


$("#nav")