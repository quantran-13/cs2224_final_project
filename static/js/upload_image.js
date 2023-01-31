/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */

$("#upload-image").change(function () {
    resetCurrentResult();

    var infoArea = $("#upload-label")[0];

    showFileName(this, infoArea);
    readURL(this);
});

const showFileName = (input, infoArea) => {
    var fileName = input.files[0].name;
    infoArea.textContent = fileName;
};

var canvas = $("#canvas"),
    context = canvas.get(0).getContext("2d");

const readURL = (input) => {
    // var x = document.getElementById("predict-result");
    // x.style.visibility = "hidden";

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (evt) {
            var image = new Image();

            image.onload = function () {
                context.canvas.height = image.height;
                context.canvas.width = image.width;
                context.drawImage(image, 0, 0);

                var cropper = canvas.cropper({
                    // aspectRatio: 1 / 1, // 16/9 ,
                    autoCropArea: 1,
                    zoomOnWheel: false,
                    zoomOnTouch: false,
                    viewMode: 2,
                });
            };

            image.src = evt.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    } else {
        alert("No file(s) selected.");
    }
};

function resetCurrentResult() {
    // var x = document.getElementById("predict-result");
    // x.style.visibility = "hidden";

    $currentCropper = canvas.data("cropper");
    $currentCropper.destroy();
    canvas.data("cropper", null);
}

$("#buttonSearch").click(function () {
    // Get a string base 64 data url
    var croppedImageDataURL = canvas
        .cropper("getCroppedCanvas")
        .toDataURL("image/png");

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/v2/search");
    // xhr.open("POST", "http://20.78.62.44:8000/v2/search");
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const body = JSON.stringify({
        session: "test",
        base64_image: croppedImageDataURL.split(",")[1],
        index_name: "oxford5k_clip",
        top_results: 50,
    });

    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var result_predict = JSON.parse(xhr.responseText)["content"];

            var result = document.getElementById("predict-result");
            result.innerHTML = result_predict;
            result.style.visibility = "show";
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
    xhr.send(body);
});
