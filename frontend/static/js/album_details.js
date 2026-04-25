function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

const csrfToken = getCSRFToken();


// ADD SONG
document.querySelectorAll(".add-song-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const songId = this.dataset.songId;

        fetch(`/api/consumers/library/songs/${songId}/add/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            }
        })
        .then(res => {
            if (res.ok) {
                this.textContent = "Added";
                this.disabled = true;
                return;
            }
            if (res.status === 401 || res.status === 403) {
                this.textContent = "Sign in required";
                return;
            }
            this.textContent = "Already added";
        })
        .catch(() => {
            this.textContent = "Error";
        });
    });
});


// ADD ALBUM
document.querySelectorAll(".add-album-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const albumId = this.dataset.albumId;

        fetch(`/api/consumers/library/albums/${albumId}/add/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            }
        })
        .then(res => {
            if (res.ok) {
                this.textContent = "Added";
                this.disabled = true;
                return;
            }
            if (res.status === 401 || res.status === 403) {
                this.textContent = "Sign in required";
                return;
            }
            this.textContent = "Already added";
        })
        .catch(() => {
            this.textContent = "Error";
        });
    });
});
