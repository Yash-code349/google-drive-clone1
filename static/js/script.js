document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('uploadForm');
    const filesList = document.getElementById('filesList');

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        alert("Uploading your file to S3...");

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (!data.error) {
                // reload page to refresh file list with correct ids and delete buttons
                location.reload();
            }
        })
        .catch(() => alert('Upload failed'));
    });
});

function deleteFile(fileId) {
    fetch(`/delete/${fileId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if (!data.error) {
            location.reload();  // reload after deletion to update list
        }
    })
    .catch(error => {
        alert('Error deleting file');
        console.error(error);
    });
}
