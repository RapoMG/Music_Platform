let selectedSongId = null;
let isSubmitting = false;

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }

    return "";
}

function setModalVisible(isVisible) {
    const modal = document.getElementById("playlist-modal");
    if (!modal) {
        return;
    }
    modal.style.display = isVisible ? "block" : "none";
}

function closePlaylistModal() {
    setModalVisible(false);
}

function showError(message) {
    window.alert(message);
}

async function openPlaylistModal(songId) {
    const parsedSongId = Number(songId);
    if (!Number.isInteger(parsedSongId) || parsedSongId <= 0) {
        showError("Invalid song id.");
        return;
    }

    selectedSongId = parsedSongId;
    const list = document.getElementById("playlist-list");
    if (!list) {
        return;
    }

    list.innerHTML = "<li>Loading playlists...</li>";
    setModalVisible(true);

    try {
        const response = await fetch("/api/me/playlists/", {
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error("Could not load playlists.");
        }

        const playlists = await response.json();
        list.innerHTML = "";

        if (!Array.isArray(playlists) || playlists.length === 0) {
            list.innerHTML = "<li>No playlists available.</li>";
            return;
        }

        playlists.forEach((playlist) => {
            const li = document.createElement("li");
            li.textContent = playlist.name;
            li.style.cursor = "pointer";
            li.addEventListener("click", () => {
                addSongToPlaylist(playlist.id);
            });
            list.appendChild(li);
        });
    } catch (error) {
        list.innerHTML = "<li>Failed to load playlists.</li>";
        showError(error.message || "Failed to load playlists.");
    }
}

async function addSongToPlaylist(playlistId) {
    if (isSubmitting) {
        return;
    }

    if (!Number.isInteger(selectedSongId) || selectedSongId <= 0) {
        showError("Missing song id.");
        return;
    }

    isSubmitting = true;

    try {
        const response = await fetch(`/api/me/playlists/${playlistId}/items/add/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                song_id: selectedSongId,
            }),
        });

        const payload = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(payload.message || "Could not add song to playlist.");
        }

        closePlaylistModal();
    } catch (error) {
        showError(error.message || "Could not add song to playlist.");
    } finally {
        isSubmitting = false;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".add-to-playlist-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            openPlaylistModal(btn.dataset.songId);
        });
    });
});
