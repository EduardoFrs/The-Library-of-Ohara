let selectedserieTitle;
let selectedserieImage;

function toggleSerieDropdown() {
    const dropdown = document.getElementById('serie-dropdown');
    dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
}

function filterSerie() {
    const input = document.getElementById('search-bar').value.toLowerCase();
    const serieItems = document.getElementsByClassName('serie-item');

    for (let i = 0; i < serieItems.length; i++) {
        const serieTitle = serieItems[i].getElementsByTagName('h2')[0];
        if (serieTitle) {
            const textValue = serieTitle.textContent || serieTitle.innerText;
            serieItems[i].style.display = textValue.toLowerCase().indexOf(input) > -1 ? '' : 'none';
        }
    }
}

let selectedserieId;

function addSerieToCollection(serieId, serieTitle, serieImage) {
    selectedSerieId = serieId;
    selectedSerieTitle = serieTitle;
    selectedSerieImage = serieImage;

    document.getElementById('modal-serie-title').textContent = selectedserieTitle;
    document.getElementById('modal-serie-image').src = selectedserieImage;
    document.getElementById('statusModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('statusModal').style.display = 'none';
}

function toggleEpisodeInput() {
    const status = document.getElementById('serie-status').value;
    const episodeInput = document.getElementById('episodeInput');

    episodeInput.style.display = (status === 'currently' || status === 'pause') ? 'block' : 'none';
}

function confirmAddSerie() {
    const serieId = selectedSerieId;
    const status = document.getElementById('serie-status').value;
    const currentEpisode = (status === 'currently' || status === 'pause') ? document.getElementById('current-episode').value : null;

    fetch(`/add_serie/${serieId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({ user_status: status, current_episode: currentEpisode })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeModal();
            location.reload();
        } else {
            alert('Failed to add serie. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
}
