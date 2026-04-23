(function () {
    const playlistsListNode = document.getElementById("playlists-list");
    const loadedPlaylistNode = document.getElementById("currently-loaded-playlist");
    const playerContainer = document.getElementById("aplayer0");

    if (!playerContainer || typeof APlayer === "undefined") {
        return;
    }

    const player = new APlayer({
        container: playerContainer,
        lrcType: 3,
        preload: "metadata",
        audio: [],
    });

    function setPlaylistLabel(name) {
        if (loadedPlaylistNode) {
            loadedPlaylistNode.textContent = name || "None selected";
        }
    }

    function normalizeAudioItems(items) {
        return items.map(function (item) {
            return {
                name: item.name,
                artist: item.artist,
                url: item.url,
                lrc: item.lrc || "",
                cover: item.cover || window.OPENCHORD_ASSETS.playlistPlaceholder,
            };
        });
    }

    function renderPlaylistRows(playlists) {
        if (!playlistsListNode) {
            return;
        }

        if (!playlists.length) {
            playlistsListNode.innerHTML = '<p class="muted">No playlists yet.</p>';
            return;
        }

        playlistsListNode.innerHTML = "";

        playlists.forEach(function (playlist) {
            const row = document.createElement("div");
            row.className = "playlist-row";

            const button = document.createElement("button");
            button.type = "button";
            button.setAttribute("data-playlist-id", String(playlist.id));
            button.setAttribute("data-playlist-name", String(playlist.name));
            button.textContent = "Play";

            const image = document.createElement("img");
            image.src = window.OPENCHORD_ASSETS.playlistPlaceholder;
            image.alt = "Playlist cover";

            const label = document.createElement("span");
            label.textContent = playlist.name;

            row.appendChild(button);
            row.appendChild(image);
            row.appendChild(label);
            playlistsListNode.appendChild(row);
        });
    }

    async function loadPlaylistToPlayer(playlistId, playlistName, autoPlay) {
        const response = await fetch("/api/me/playlists/" + playlistId + "/player/", {
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Could not load playlist tracks.");
        }

        const tracks = normalizeAudioItems(await response.json());

        player.list.clear();
        if (tracks.length) {
            player.list.add(tracks);
            if (autoPlay) {
                player.list.switch(0);
                player.play();
            }
        }

        setPlaylistLabel(playlistName);
    }

    async function loadPlaylistsBar() {
        if (!window.OPENCHORD_USER_IS_AUTHENTICATED) {
            return;
        }

        const response = await fetch("/api/me/playlists/", {
            credentials: "include",
        });

        if (!response.ok) {
            renderPlaylistRows([]);
            return;
        }

        const playlists = await response.json();
        playlists.sort(function (a, b) {
            return b.id - a.id;
        });
        renderPlaylistRows(playlists);

        if (playlists.length) {
            loadPlaylistToPlayer(playlists[0].id, playlists[0].name, false).catch(function () {
                setPlaylistLabel("None selected");
            });
        }
    }

    if (playlistsListNode) {
        playlistsListNode.addEventListener("click", function (event) {
            const target = event.target;
            if (!target || target.tagName !== "BUTTON") {
                return;
            }

            const playlistId = target.getAttribute("data-playlist-id");
            const playlistName = target.getAttribute("data-playlist-name");

            loadPlaylistToPlayer(playlistId, playlistName, true).catch(function () {
                setPlaylistLabel("Failed to load");
            });
        });
    }

    loadPlaylistsBar().catch(function () {
        setPlaylistLabel("None selected");
    });
})();
