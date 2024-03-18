document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const songList = document.getElementById('songList');
    const audioPlayer = document.getElementById('audioPlayer');
    const prevButton = document.getElementById('prevButton');
    const playPauseButton = document.getElementById('playPauseButton');
    const nextButton = document.getElementById('nextButton');
    const volumeButton = document.getElementById('volumeButton');
    const modeButton = document.getElementById('modeButton');
    const playlist = document.getElementById('playlist');
    const playlistButton = document.getElementById('playlistButton');
    const currentSongName = document.getElementById('currentSongName'); // 获取当前播放音乐名的元素

    let currentSongIndex = 0;
    let songs = [];
    let isPlaying = false;
    let playbackMode = 'loop';

    function fetchSongs() {
        fetch('/get_songs')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch songs.');
                }
                return response.json();
            })
            .then(data => {
                songs = data.songs;
                displaySongs();
            })
            .catch(error => console.error('Error fetching songs:', error));
    }

    function displaySongs(filteredSongs) {
        songList.innerHTML = '';
        const songsToDisplay = filteredSongs || songs;
        songsToDisplay.forEach((song, index) => {
            const songItem = document.createElement('div');
            const songIndex = index + 1;
            songItem.textContent = `${songIndex}. ${song}`;
            songItem.addEventListener('click', () => {
                playSong(songsToDisplay, index);
            });
            songList.appendChild(songItem);
        });
    }

    function playSong(songsToPlay, index) {
        if (index >= 0 && index < songsToPlay.length) {
            currentSongIndex = index;
            fetch(`/play_song?song=${encodeURIComponent(songsToPlay[index])}`)
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    audioPlayer.src = url;
                    audioPlayer.play();
                    isPlaying = true;
                    updatePlayPauseButton();
                    // 更新页面标题
                    document.title = songsToPlay[index];
                    console.log('播放音乐：', songsToPlay[index]);
                })
                .catch(error => console.error('Error playing song:', error));
        }
    }


    function updatePlayPauseButton() {
        if (isPlaying) {
            playPauseButton.textContent = '暂停';
        } else {
            playPauseButton.textContent = '播放';
        }
    }

    searchButton.addEventListener('click', performSearch);

    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const filteredSongs = songs.filter(song => song.toLowerCase().includes(searchTerm));
        displaySongs(filteredSongs);
    }

    prevButton.addEventListener('click', () => {
        currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
        playSong(songs, currentSongIndex);
    });

    playPauseButton.addEventListener('click', () => {
        if (isPlaying) {
            audioPlayer.pause();
        } else {
            audioPlayer.play();
        }
        isPlaying = !isPlaying;
        updatePlayPauseButton();
    });

    nextButton.addEventListener('click', () => {
        currentSongIndex = (currentSongIndex + 1) % songs.length;
        playSong(songs, currentSongIndex);
    });

    volumeButton.addEventListener('click', () => {
        audioPlayer.muted = !audioPlayer.muted;
        volumeButton.textContent = audioPlayer.muted ? 'Mute' : 'Volume';
    });

    modeButton.addEventListener('click', togglePlaybackMode);

    function togglePlaybackMode() {
        const modes = ['loop', 'shuffle', 'repeat'];
        playbackMode = modes[(modes.indexOf(playbackMode) + 1) % modes.length];
        modeButton.textContent = playbackMode.charAt(0).toUpperCase() + playbackMode.slice(1);
    }


    function togglePlaylist() {
        playlist.style.display = playlist.style.display === 'block' ? 'none' : 'block';
    }

    fetchSongs();
});
