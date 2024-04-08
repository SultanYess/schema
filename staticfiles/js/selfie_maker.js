/*# sourceURL=pen.js */

console.clear()


function query(selector) {
    return document.querySelector(selector)
}

const video = query('#video')
const requestMediaStreamBtn = query('#request-media-stream-btn')
const getScreenshotFromMediaStreamBtn = query('#get-screenshot-from-media-stream-btn')

// Buttons

requestMediaStreamBtn.addEventListener('click', event => {
    requestCamAndStreamInVideo(video)
})

getScreenshotFromMediaStreamBtn.addEventListener('click', async event => {
    const blob = await captureScreenshotFromMediaStream(video.srcObject)

    const url = URL.createObjectURL(blob)

    const imageWindow = open(url)

    imageWindow.addEventListener('beforeunload', event => URL.revokeObjectURL(url))
})


// Functions

async function requestCamAndStreamInVideo(video) {
    const mediaStream = await navigator.mediaDevices.getUserMedia({video: true})

    if (video && video instanceof HTMLVideoElement) {
        video.srcObject = mediaStream
    }
}

async function captureScreenshotFromMediaStream(mediaStream) {
    if (!mediaStream || !(mediaStream instanceof MediaStream)) return

    const imageCapture = new ImageCapture(mediaStream.getVideoTracks()[0])
    const blob = await imageCapture.takePhoto()

    return blob
}
