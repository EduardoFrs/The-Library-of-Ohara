function toggleMangaDropdown() {
    const dropdown = document.getElementById('manga-dropdown');
    dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
}

function filterManga() {
    const input = document.getElementById('search-bar').value.toLowerCase();
    const mangaItems = document.getElementsByClassName('manga-item');

    for (let i = 0; i < mangaItems.length; i++) {
        const mangaTitle = mangaItems[i].getElementsByTagName('h2')[0];
        if (mangaTitle) {
            const textValue = mangaTitle.textContent || mangaTitle.innerText;
            mangaItems[i].style.display = textValue.toLowerCase().indexOf(input) > -1 ? '' : 'none';
        }
    }
}

let selectedMangaId;

function addMangaToCollection(mangaId, mangaTitle, mangaImage) {
    selectedMangaId = mangaId;
    selectedMangaTitle = mangaTitle;
    selectedMangaImage = mangaImage;

    document.getElementById('modal-manga-title').textContent = selectedMangaTitle;
    document.getElementById('modal-manga-image').src = selectedMangaImage;
    document.getElementById('statusModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('statusModal').style.display = 'none';
}

function toggleChapterInput() {
    const status = document.getElementById('manga-status').value;
    const chapterInput = document.getElementById('chapterInput');


    chapterInput.style.display = (status === 'currently' || status === 'pause') ? 'block' : 'none';
}
function confirmAddManga() {
    const mangaId = selectedMangaId;
    const status = document.getElementById('manga-status').value;
    const currentChapter = (status === 'currently' || status === 'pause')
    ? document.getElementById('current-chapter').value
    : null;

    fetch(`/add_manga/${mangaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({manga_id: mangaId, user_status: status, current_chapter: currentChapter })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeModal();
            location.reload();
        } else {
            alert('Failed to add manga. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
}
