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

function updatePlaylistPositions(list) {
    const rows = list.querySelectorAll(".list-row[data-item-id]");
    rows.forEach((row, index) => {
        const position = index + 1;
        row.dataset.position = String(position);

        const label = row.querySelector(".playlist-item-position");
        if (label) {
            label.textContent = String(position);
        }

        const moveUpButton = row.querySelector(".move-up-btn");
        const moveDownButton = row.querySelector(".move-down-btn");

        if (moveUpButton) {
            moveUpButton.disabled = index === 0;
        }

        if (moveDownButton) {
            moveDownButton.disabled = index === rows.length - 1;
        }
    });
}

async function moveItem(itemId, direction) {
    if (isSubmitting) {
        return;
    }

    const playlistSection = document.querySelector("[data-playlist-id]");
    const list = document.querySelector("[data-playlist-items]");
    const row = document.querySelector(`.list-row[data-item-id="${itemId}"]`);

    if (!playlistSection || !list || !row) {
        showError("Playlist item could not be found.");
        return;
    }

    const playlistId = Number(playlistSection.dataset.playlistId);
    const currentPosition = Number(row.dataset.position);
    const positionChange = direction === "up" ? -1 : 1;
    const newPosition = currentPosition + positionChange;
    const rows = Array.from(list.querySelectorAll(".list-row[data-item-id]"));

    if (!Number.isInteger(playlistId) || !Number.isInteger(currentPosition)) {
        showError("Missing playlist data.");
        return;
    }

    if (newPosition < 1 || newPosition > rows.length) {
        return;
    }

    isSubmitting = true;

    try {
        const response = await fetch(`/api/me/playlists/${playlistId}/items/${itemId}/reorder/`, {
            method: "PATCH",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                position: newPosition,
            }),
        });

        const payload = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(payload.message || "Could not move song in playlist.");
        }

        const sibling = direction === "up" ? row.previousElementSibling : row.nextElementSibling;
        if (sibling) {
            if (direction === "up") {
                list.insertBefore(row, sibling);
            } else {
                list.insertBefore(sibling, row);
            }
        }

        updatePlaylistPositions(list);
    } catch (error) {
        showError(error.message || "Could not move song in playlist.");
    } finally {
        isSubmitting = false;
    }
}


document.addEventListener("DOMContentLoaded", () => {
    const playlistList = document.querySelector("[data-playlist-items]");
    if (playlistList) {
        updatePlaylistPositions(playlistList);

        playlistList.addEventListener("click", (event) => {
            const moveUpButton = event.target.closest(".move-up-btn");
            const moveDownButton = event.target.closest(".move-down-btn");

            if (moveUpButton) {
                moveItem(moveUpButton.dataset.itemId, "up");
                return;
            }

            if (moveDownButton) {
                moveItem(moveDownButton.dataset.itemId, "down");
            }
        });
    }

    document.querySelectorAll(".add-to-playlist-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            openPlaylistModal(btn.dataset.songId);
        });
    });
});
