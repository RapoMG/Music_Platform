(function () {
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

    function showError(message) {
        window.alert(message);
    }

    function updatePlaylistPositions(list) {
        const rows = list.querySelectorAll(".list-row[data-item-id]");

        rows.forEach((row, index) => {
            const position = index + 1;
            row.dataset.position = String(position);

            const positionLabel = row.querySelector(".playlist-item-position");
            if (positionLabel) {
                positionLabel.textContent = String(position);
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

    async function moveItem(button, direction) {
        const playlistSection = document.querySelector("[data-playlist-id]");
        const list = document.querySelector("[data-playlist-items]");
        const row = button.closest(".list-row[data-item-id]");

        if (!playlistSection || !list || !row) {
            showError("Playlist item could not be found.");
            return;
        }

        const playlistId = Number(playlistSection.dataset.playlistId);
        const itemId = Number(row.dataset.itemId);
        const currentPosition = Number(row.dataset.position);
        const rows = Array.from(list.querySelectorAll(".list-row[data-item-id]"));
        const newPosition = currentPosition + (direction === "up" ? -1 : 1);

        if (!Number.isInteger(playlistId) || !Number.isInteger(itemId) || !Number.isInteger(currentPosition)) {
            showError("Missing playlist data.");
            return;
        }

        if (newPosition < 1 || newPosition > rows.length) {
            return;
        }

        const sibling = direction === "up" ? row.previousElementSibling : row.nextElementSibling;
        if (!sibling || !sibling.matches(".list-row[data-item-id]")) {
            return;
        }

        button.disabled = true;

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

            if (direction === "up") {
                list.insertBefore(row, sibling);
            } else {
                list.insertBefore(sibling, row);
            }

            updatePlaylistPositions(list);
        } catch (error) {
            showError(error.message || "Could not move song in playlist.");
        } finally {
            updatePlaylistPositions(list);
        }
    }

    async function deletePlaylistItem(button) {
        const playlistId = Number(button.dataset.playlistId);
        const playlistItemId = Number(button.dataset.itemId);
        const playlistItemName = button.dataset.itemName || "this song";
        const list = document.querySelector("[data-playlist-items]");
        const row = button.closest(".list-row[data-item-id]");

        if (!Number.isInteger(playlistId) || !Number.isInteger(playlistItemId) || !list || !row) {
            showError("Playlist item could not be found.");
            return;
        }

        if (!window.confirm(`Remove "${playlistItemName}" from playlist?`)) {
            return;
        }

        button.disabled = true;

        try {
            const response = await fetch(`/api/me/playlists/${playlistId}/items/${playlistItemId}/remove/`, {
                method: "DELETE",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                },
            });

            const payload = await response.json().catch(() => ({}));
            if (!response.ok) {
                throw new Error(payload.message || "Could not remove song from playlist.");
            }

            row.remove();
            updatePlaylistPositions(list);
        } catch (error) {
            button.disabled = false;
            showError(error.message || "Could not remove song from playlist.");
        }
    }

    function initPlaylistEditor() {
        const playlistList = document.querySelector("[data-playlist-items]");
        const editButton = document.getElementById("edit-playlist-btn");
        const closeButton = document.getElementById("close-playlist-btn");

        if (editButton) {
            editButton.addEventListener("click", function (event) {
                event.preventDefault();
                openPlaylistFormModal();
            });
        }

        if (closeButton) {
            closeButton.addEventListener("click", function () {
                closePlaylistFormModal();
            });
        }

        if (!playlistList) {
            return;
        }

        updatePlaylistPositions(playlistList);

        playlistList.querySelectorAll(".move-up-btn").forEach(function (button) {
            button.addEventListener("click", function () {
                moveItem(button, "up");
            });
        });

        playlistList.querySelectorAll(".move-down-btn").forEach(function (button) {
            button.addEventListener("click", function () {
                moveItem(button, "down");
            });
        });

        playlistList.querySelectorAll(".delete-item-btn").forEach(function (button) {
            button.addEventListener("click", function (event) {
                event.preventDefault();
                deletePlaylistItem(button);
            });
        });
    }

    /* Playlist Form Modal */
    function setUpdateModalVisible(isVisible) {
        const modalDisp = document.getElementById("playlist-data-display");
        const modalEdit = document.getElementById("playlist-data-edit");
        if (!modalEdit || !modalDisp) {
            return;
        }
        modalDisp.style.display = isVisible ? "none" : "block";
        modalEdit.style.display = isVisible ? "block" : "none";
    }

    function closePlaylistFormModal() {
        setUpdateModalVisible(false);
    }

    function openPlaylistFormModal() {
        setUpdateModalVisible(true);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initPlaylistEditor);
    } else {
        initPlaylistEditor();
    }
})();
