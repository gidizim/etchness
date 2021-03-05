const login = () => {
    location.href = "home.html";
}

const edit = () => {
    const profileFeatures = document.getElementsByName('profile');
    if (document.getElementById('edit-btn').value == "Save changes") {
        document.getElementById('edit-btn').value = "Edit profile";
    } else {
        document.getElementById('edit-btn').value = "Save changes";
    }
    for (let i = 0; i < profileFeatures.length; i++) {
        profileFeatures[i].disabled = !profileFeatures[i].disabled;
    }
}