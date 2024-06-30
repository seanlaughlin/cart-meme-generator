document.addEventListener('DOMContentLoaded', function () {
    var swiper = new Swiper('.swiper-container', {
        slidesPerView: 4,
        slidesPerGroup: 4,
        spaceBetween: 1,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        loop: false,
    });

    const thumbnails = document.querySelectorAll('.background-thumbnail');

    if (thumbnails.length > 0) {
        // Select the first thumbnail by default
        const firstThumbnail = thumbnails[0];
        firstThumbnail.classList.add('selected');
        document.getElementById('selected-background').value = firstThumbnail.getAttribute('data-background');
        submitForm();
    }

    document.querySelectorAll('.background-thumbnail').forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            document.querySelectorAll('.background-thumbnail').forEach(t => t.classList.remove('selected'));
            this.classList.add('selected');
            document.getElementById('selected-background').value = this.getAttribute('data-background');
            submitForm();
        });
    });

    document.querySelector('input[type="file"]').addEventListener('change', function(event) {
        const fileInput = event.target;
        const file = fileInput.files[0];
        const fileName = document.getElementById('file-name');

        if (file) {
            fileName.textContent = file.name;
            fileName.style.display = 'none';
            submitForm();
        } else {
            fileName.style.display = 'none';
        }
    });
});

function submitForm() {
    var formData = new FormData(document.getElementById('upload-form'));
    document.getElementById('loader').style.display = 'flex';
    document.getElementById('output-image').style.display = 'none';
    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(blob => {
        var url = URL.createObjectURL(blob);
        var outputImage = document.getElementById('output-image');
        outputImage.src = url;
        outputImage.style.display = 'block';
        document.getElementById('loader').style.display = 'none';
        window.scrollTo(0, 0);
    }).catch(() => {
        document.getElementById('loader').style.display = 'none';
        alert('Failed to upload image');
    });
}

document.getElementById('download-button').addEventListener('click', function() {
    var image = document.getElementById('output-image');
    var imageUrl = image.src;
    var link = document.createElement('a');
    link.href = imageUrl;
    link.download = 'output-image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});