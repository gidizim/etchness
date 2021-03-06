const login = () => {
    const formDetails = document.querySelectorAll('[required]');
    for (let i = 0; i < formDetails.length; i++) {
        if (formDetails[i].value == "") {
            alert("Please fill in all the fields");
            return;
        };
    }
    
    location.href = "home.html";

}

const edit = () => {
    const profileFeatures = document.getElementsByName('profile');
    const button = document.getElementById('edit-btn');
    if (button.value == "Save changes") {
        button.value = "Edit profile";
        button.style.backgroundColor = "#332e2e";
    } else {
        button.value = "Save changes";
        button.style.backgroundColor = "rgb(128, 39, 39)";
    }
    for (let i = 0; i < profileFeatures.length; i++) {
        profileFeatures[i].disabled = !profileFeatures[i].disabled;
    }
}
const addToWatchlist = () => {
    const button = document.getElementById('add');
    if (button.value == "Add to watchlist") {
        button.value = "Remove from watchlist";
    } else {
        button.value = "Add to watchlist";
    }
}
// gotta fix this code later
// const like = () => {
//     const button = document.getElementsByClassName('fav-btn')[0];
//     if (button.value == "unliked") {
//         button.value = "liked";
//         button.style.color = "red";
//     } else {
//         button.value = "unliked";
//         button.style.color = "grey";
//     }
// }