document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('docx_file', document.querySelector('input[type="file"]').files[0]);

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'converted.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    });
});
