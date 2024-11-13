let selectedmovieTitle;
let selectedmovieImage;

function toggleMovieDropdown() {
    const dropdown = document.getElementById('movie-dropdown');
    dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
}

function filterMovie() {
    const input = document.getElementById('search-bar').value.toLowerCase();
    const movieItems = document.getElementsByClassName('movie-item');

    for (let i = 0; i < movieItems.length; i++) {
        const movieTitle = movieItems[i].getElementsByTagName('h2')[0];
        if (movieTitle) {
            const textValue = movieTitle.textContent || movieTitle.innerText;
            movieItems[i].style.display = textValue.toLowerCase().indexOf(input) > -1 ? '' : 'none';
        }
    }
}

let selectedmovieId;

function addMovieToCollection(movieId, movieTitle, movieImage) {
    selectedMovieId = movieId;
    selectedMovieTitle = movieTitle;
    selectedMovieImage = movieImage;

    document.getElementById('modal-movie-title').textContent = selectedmovieTitle;
    document.getElementById('modal-movie-image').src = selectedmovieImage;
    document.getElementById('statusModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('statusModal').style.display = 'none';
}

function toggleEpisodeInput() {
    const status = document.getElementById('movie-status').value;
    const episodeInput = document.getElementById('episodeInput');

    episodeInput.style.display = (status === 'currently' || status === 'pause') ? 'block' : 'none';
}

function confirmAddMovie() {
    const movieId = selectedmovieId;
    const status = document.getElementById('movie-status').value;
    const currentEpisode = (status === 'currently' || status === 'pause') ? document.getElementById('current-episode').value : null;

    fetch(`/add_movie/${movieId}/`, {
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
            alert('Failed to add movie. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
}
