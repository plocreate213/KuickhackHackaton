function uploadFile() {
    var fileInput = document.getElementById('file-input');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var labelsContainer = document.getElementById('labels-container');
            labelsContainer.innerHTML = '';

            if (response.error) {
                labelsContainer.innerText = 'Error: ' + response.error;
            } else {
                var labels = response.labels;
                if (labels.length > 0) {
                    var ul = document.createElement('ul');
                    labels.forEach(function(label) {
                        var li = document.createElement('li');
                        li.innerText = label;
                        ul.appendChild(li);
                    });
                    labelsContainer.appendChild(ul);
                } else {
                    labelsContainer.innerText = labels;
                }
            }
        } else {
            var errorMessage = document.getElementById('error-message');
            errorMessage.innerText = 'Error: ' + xhr.statusText;
        }
    };
    xhr.send(formData);

    var uploadedImage = document.getElementById('uploaded-image');
    uploadedImage.src = URL.createObjectURL(file);
    uploadedImage.style.display = 'block';
}