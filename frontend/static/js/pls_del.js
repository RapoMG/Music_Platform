function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}


function deletePlaylist(playlistId, playlistName, element) {
    if (!confirm(`Delete "${playlistName}" playlist?`)) return;

    fetch(`/api/me/playlists/${playlistId}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(response => {
        if (response.status === 204) {
            // Remove from DOM (no full reload needed)
            element.closest('.list-row').remove();
            return;
        }

        throw new Error("Delete failed");
    })
    .catch(err => {
        console.error(err);
        alert("Error deleting playlist");
    });
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