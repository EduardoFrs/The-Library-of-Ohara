function toggleAnimeDropdown() {
    const dropdown = document.getElementById('anime-dropdown');
    dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
}

function filterAnime() {
    const input = document.getElementById('search-bar').value.toLowerCase();
    const animeItems = document.getElementsByClassName('anime-item');

    for (let i = 0; i < animeItems.length; i++) {
        const animeTitle = animeItems[i].getElementsByTagName('h2')[0];
        if (animeTitle) {
            const textValue = animeTitle.textContent || animeTitle.innerText;
            if (textValue.toLowerCase().indexOf(input) > -1) {
                animeItems[i].style.display = '';
            } else {
                animeItems[i].style.display = 'none';
            }
        }
    }
}

let selectedanimeId;

function addAnimeToCollection(animeId, animeTitle, animeImage) {
    selectedAnimeId = animeId;
    selectedAnimeTitle = animeTitle;
    selectedAnimeImage = animeImage;

    document.getElementById('modal-anime-title').textContent = selectedAnimeTitle;
    document.getElementById('modal-anime-image').src = selectedAnimeImage;
    document.getElementById('statusModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('statusModal').style.display = 'none';
}

function toggleEpisodeInput() {
    const status = document.getElementById('anime-status').value;
    const episodeInput = document.getElementById('episodeInput');

    episodeInput.style.display = (status === 'currently' || status === 'pause') ? 'block' : 'none';
}
function confirmAddAnime() {
    const animeId = selectedAnimeId;
    const status = document.getElementById('anime-status').value;
    const currentEpisode = (status === 'currently' || status === 'pause')
    ? document.getElementById('current-episode').value
    : null;

    fetch(`/add_anime/${animeId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({anime_id: animeId, user_status: status, current_episode: currentEpisode })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeModal();
            location.reload();
        } else {
            alert('Failed to add anime. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
}
