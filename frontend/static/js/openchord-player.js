(function () {
    const playlistsListNode = document.getElementById("playlists-list");
    const loadedPlaylistNode = document.getElementById("currently-loaded-playlist");
    const playerContainer = document.getElementById("aplayer0");
    const PLAYER_STATE_KEY = "openchord.playerState";

    if (!playerContainer || typeof APlayer === "undefined") {
        return;
    }

    const player = new APlayer({
        container: playerContainer,
        lrcType: 1,
        preload: "metadata",
        audio: [],
    });

    let currentPlaylistId = null;
    let currentPlaylistName = null;

    function setPlaylistLabel(name) {
        if (loadedPlaylistNode) {
            loadedPlaylistNode.textContent = name || "None selected";
        }
    }

    function normalizeAudioItems(items) {
        return items.filter(function (item) {
            return Boolean(item.url);
        }).map(function (item) {
            return {
                name: item.name,
                artist: item.artist,
                url: item.url,
                lrc: item.lrc || "",
                cover: item.cover || window.OPENCHORD_ASSETS.playlistPlaceholder,
                type: "normal",
            };
        });
    }

    function getPlayerState() {
        if (!window.OPENCHORD_USER_IS_AUTHENTICATED || !currentPlaylistId || !player.list.audios.length) {
            return null;
        }

        return {
            playlistId: currentPlaylistId,
            playlistName: currentPlaylistName || "",
            trackIndex: player.list.index || 0,
            currentTime: Number(player.audio.currentTime || 0),
            paused: Boolean(player.audio.paused),
        };
    }

    function persistPlayerState() {
        const state = getPlayerState();
        if (!state) {
            return;
        }

        window.localStorage.setItem(PLAYER_STATE_KEY, JSON.stringify(state));
    }

    function clearStoredPlayerState() {
        window.localStorage.removeItem(PLAYER_STATE_KEY);
    }

    function readStoredPlayerState() {
        try {
            const rawState = window.localStorage.getItem(PLAYER_STATE_KEY);
            return rawState ? JSON.parse(rawState) : null;
        } catch (error) {
            clearStoredPlayerState();
            return null;
        }
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

    function restorePlaybackPosition(timeToRestore, shouldResumePlayback) {
        function applyPosition() {
            if (timeToRestore > 0) {
                player.audio.currentTime = timeToRestore;
            }

            if (shouldResumePlayback) {
                player.play();
            } else {
                player.pause();
            }
        }

        if (player.audio.readyState >= 1) {
            applyPosition();
            return;
        }

        const onLoadedMetadata = function () {
            player.audio.removeEventListener("loadedmetadata", onLoadedMetadata);
            applyPosition();
        };

        player.audio.addEventListener("loadedmetadata", onLoadedMetadata);
    }

    async function loadPlaylistToPlayer(playlistId, playlistName, options) {
        const settings = options || {};
        const response = await fetch("/api/me/playlists/" + playlistId + "/player/", {
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Could not load playlist tracks.");
        }

        const tracks = normalizeAudioItems(await response.json());

        player.list.clear();
        currentPlaylistId = playlistId;
        currentPlaylistName = playlistName;

        if (tracks.length) {
            player.list.add(tracks);

            const trackIndex = Math.min(
                Math.max(Number(settings.trackIndex || 0), 0),
                tracks.length - 1
            );

            player.list.switch(trackIndex);

            if (settings.restorePosition) {
                restorePlaybackPosition(Number(settings.currentTime || 0), !settings.paused);
            } else if (settings.autoPlay) {
                player.play();
            } else {
                player.pause();
            }
        } else {
            currentPlaylistId = null;
            currentPlaylistName = null;
        }

        setPlaylistLabel(playlistName);
        persistPlayerState();
    }

    async function loadPlaylistsBar() {
        if (!window.OPENCHORD_USER_IS_AUTHENTICATED) {
            clearStoredPlayerState();
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

        const savedState = readStoredPlayerState();
        if (savedState && playlists.some(function (playlist) { return String(playlist.id) === String(savedState.playlistId); })) {
            await loadPlaylistToPlayer(savedState.playlistId, savedState.playlistName, {
                restorePosition: true,
                trackIndex: savedState.trackIndex,
                currentTime: savedState.currentTime,
                paused: savedState.paused,
            });
            return;
        }

        if (playlists.length) {
            await loadPlaylistToPlayer(playlists[0].id, playlists[0].name, {
                autoPlay: false,
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

            loadPlaylistToPlayer(playlistId, playlistName, {
                autoPlay: true,
            }).catch(function () {
                setPlaylistLabel("Failed to load");
            });
        });
    }

    player.audio.addEventListener("play", persistPlayerState);
    player.audio.addEventListener("pause", persistPlayerState);
    player.audio.addEventListener("timeupdate", persistPlayerState);
    player.audio.addEventListener("ended", persistPlayerState);
    player.on("listswitch", persistPlayerState);
    window.addEventListener("beforeunload", persistPlayerState);

    loadPlaylistsBar().catch(function () {
        setPlaylistLabel("None selected");
    });
})();
