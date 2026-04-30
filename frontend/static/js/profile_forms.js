function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

function setUpdateProfileVisible(isVisible) {
    const modalProfile = document.getElementById("edit-user-form-container");  
    if (!modalProfile) {
        return;
    }
    modalProfile.style.display = isVisible ? "block" : "none"; // Show the profile form
    
}

function setCreatePlaylistVisible(isVisible) {
    const modalPlaylist = document.getElementById("new-playlist-form-container");
    if (!modalPlaylist) {
        return;
    }
    modalPlaylist.style.display = isVisible ? "block" : "none"; // Show the playlist form
}

function initFormsDisplay() {
    const updateProfile = document.getElementById("edit-user-btn");
    const createPlaylist = document.getElementById("create-playlist-btn");

    // Add event listeners
    if (updateProfile) {
        updateProfile.addEventListener("click", openUpdateProfile);
    }

    if (createPlaylist) {
        createPlaylist.addEventListener("click", openCreatePlaylist);
    }
    
    document.querySelectorAll(".close-form-btn").forEach(btn => {
        btn.addEventListener("click", closeBothForms);
    });
}


// Switch between forms
function openUpdateProfile() {
    setUpdateProfileVisible(true);
    setCreatePlaylistVisible(false);
}

function openCreatePlaylist() {
    setUpdateProfileVisible(false);
    setCreatePlaylistVisible(true);
}

function closeBothForms() {
    setUpdateProfileVisible(false);
    setCreatePlaylistVisible(false);
}

// Start the forms machine
if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initFormsDisplay);
    } else {
        initFormsDisplay();
    }


document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-playlist-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const playlistId = this.dataset.playlistId;
            const playlistName = this.dataset.playlistName || "this";
            deletePlaylist(playlistId, playlistName, this);
        });
    });
});

