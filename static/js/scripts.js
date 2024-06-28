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

        document.addEventListener('DOMContentLoaded', function() {
            const firstThumbnail = document.querySelector('.background-thumbnail');
            if (firstThumbnail) {
                firstThumbnail.classList.add('selected');
                document.getElementById('selected-background').value = firstThumbnail.getAttribute('data-background');
                submitForm();
            }
        });

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
            const preview = document.getElementById('upload-preview');
            const fileName = document.getElementById('file-name');

            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    document.getElementById('upload-preview-container').style.display = 'block';
                };
                reader.readAsDataURL(file);

                fileName.textContent = file.name;
                fileName.style.display = 'block';
                submitForm();
            } else {
                preview.style.display = 'none';
                fileName.style.display = 'none';
                document.getElementById('upload-preview-container').style.display = 'none';
            }
        });