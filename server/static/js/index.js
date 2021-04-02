const edit = () => {
    const profileFeatures = document.getElementsByName('profile');
    const button = document.getElementById('edit-btn');
    if (button.value == "Save changes") {
        button.value = "Edit profile";
        button.style.backgroundColor = "rgb(252, 76, 56)";
    } else {
        button.value = "Save changes";
        button.style.backgroundColor = "rgb(168, 24, 8)";
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