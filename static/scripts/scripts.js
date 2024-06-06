let currentPage = 0;
let userId = '';

document.addEventListener('DOMContentLoaded', () => {
    init();
});

function init() {
    startSession();
    setupEventListeners();
}

function setupEventListeners() {
    document.getElementById('next-btn').addEventListener('click', nextPage);
    document.getElementById('prev-btn').addEventListener('click', prevPage);
    document.addEventListener('keydown', handleKeyPress);
    window.addEventListener('beforeunload', endSession);
}

function handleKeyPress(event) {
    if (event.key === 'ArrowRight') {
        nextPage();
    } else if (event.key === 'ArrowLeft') {
        prevPage();
    }
}

async function startSession() {
    const response = await fetch('/start_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    userId = data.user_id;
    document.getElementById('main').style.display = 'block';
    loadImages();
}

async function endSession() {
    await fetch('/end_session', { method: 'POST' });
}

async function loadImages() {
    const response = await fetch(`/load_images/${currentPage}`);
    const data = await response.json();
    renderImages(data.images);
    updateStatus(data.status);
    updateProgressBar(data.status);
}

function renderImages(images) {
    const grid = document.getElementById('image-grid');
    grid.innerHTML = '';
    images.forEach(({ image_name, is_flicker }) => {
        const tile = createTile(image_name, is_flicker);
        grid.appendChild(tile);
    });
}

function createTile(imageName, isFlicker) {
    const tile = document.createElement('div');
    tile.className = 'tile';
    tile.dataset.imageName = imageName;
    if (isFlicker) {
        tile.classList.add('selected');
    }

    tile.addEventListener('click', () => toggleImageSelection(tile, imageName));

    const img = document.createElement('img');
    img.src = `/static/images/${imageName}`;
    img.alt = imageName;

    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    // overlay.textContent = 'Selected';
    overlay.textContent = 'Flicker!';

    tile.appendChild(img);
    tile.appendChild(overlay);
    return tile;
}

function toggleImageSelection(tile, imageName) {
    const isSelected = tile.classList.toggle('selected');
    updateImageSelection(imageName, isSelected);
}

async function updateImageSelection(imageName, isFlicker) {
    const response = await fetch('/select_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            image_name: imageName,
            is_flicker: isFlicker
        })
    });
    const data = await response.json();
    updateStatus(data.updated_status);
    updateProgressBar(data.updated_status);
}

function updateStatus(status) {
    document.getElementById('total-images').textContent = `Total Images: ${status.total_images}`;
    document.getElementById('remaining-images').textContent = `Images Left: ${status.remaining_images}`;
    document.getElementById('selected-images').textContent = `Selected Images: ${status.flicker_images}`;
    document.getElementById('user-count').innerHTML = `Active Users: ${status.active_users} <span class="green-circle"></span>`;
}

function updateProgressBar(status) {
    const progressBar = document.getElementById('progress-bar-inner');
    const progress = ((status.total_images - status.remaining_images) / status.total_images) * 100;
    progressBar.style.width = `${progress}%`;
}

function nextPage() {
    currentPage++;
    loadImages();
}

function prevPage() {
    if (currentPage > 0) {
        currentPage--;
        loadImages();
    }
}
