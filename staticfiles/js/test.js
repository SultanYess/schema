(() => {
    let streaming = false;
    let video = null;
    let canvas = null;
    let photo = null;
    let startbutton = null;

    function startup() {
        video = document.getElementById("video");
        canvas = document.getElementById("canvas");
        photo = document.getElementById("photo");
        startbutton = document.getElementById("startbutton");
        original_image = document.getElementById('id_original_image');
        cardBody = document.getElementById('cardBody');
        restart = document.getElementById('restart')
        submit = document.getElementById('submit');


        canvas.style.display = 'none'
        restart.style.display = 'none'
        submit.style.display = 'none'

        navigator.mediaDevices
            .getUserMedia({video: true, audio: false})
            .then((stream) => {
                video.srcObject = stream;
                video.play();
            })
            .catch((err) => {
                console.error(`An error occurred: ${err}`);
            });

        video.addEventListener(
            "canplay",
            (ev) => {
                if (!streaming) {
                    streaming = true;
                }
            },
            false,
        );
        startbutton.addEventListener(
            "click",
            (ev) => {
                restart.style.display = 'inline'
                submit.style.display = 'inline'
                navigator.mediaDevices
                    .getUserMedia({video: true, audio: false})
                    .then((stream) => {
                        video.srcObject = stream;
                        video.stop();
                    })
                takepicture();
                ev.preventDefault();
            },
            false,
        );
        clearphoto();
        canvas.style.display = 'none';
    }

    function clearphoto() {
        const context = canvas.getContext("2d");
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);
    }

    function takepicture() {
        const context = canvas.getContext("2d");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        const data = canvas.toDataURL("image/png");
        photo.setAttribute("src", data);
        let blob = (dataURItoBlob(data));
        let file = new File([blob], "img.png", {type: "image/png", lastModified: new Date().getTime()});
        let input_image = document.querySelector("input#id_original_image")
        let container = new DataTransfer();
        container.items.add(file);
        input_image.files = container.files;

        deleteVideo()
        canvas.style.display = 'block';
        startbutton.style.display = 'none'
        input_image.style.display = 'block'
    }

    function deleteVideo() {
        const video = document.getElementById('video')
        video.remove()
    }

    function dataURItoBlob(dataURI) {
        var binary = atob(dataURI.split(',')[1]);
        var array = [];
        for (i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }
        return new Blob([new Uint8Array(array)], {type: 'image/png'});
    }


    window.addEventListener("load", startup, false);
})();
