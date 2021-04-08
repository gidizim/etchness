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

}
