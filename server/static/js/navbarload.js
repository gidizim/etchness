/* Function to run once navbar has loaded */
function navLoaded()
{
    var path = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1);
    if (path == 'home.html')
        $('#home').addClass('active');
    else if (path == 'login.html')
        $('#login').addClass('active');
    else if (path == 'watchlist.html')
        $('#watchlist').addClass('active');
    else if (path == 'profile.html')
        $('#profile').addClass('active');
    else if (path == 'newsfeed.html')
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