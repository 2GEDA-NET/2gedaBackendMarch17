console.log("hello world");

var mapPeers = {};

var labelusername = document.querySelector("#label-username");
var usernameInput = document.querySelector("#username");
var btnJoin = document.querySelector("#btn-join");

var username;
var webSocket;

function webSocketOnMessage(event) {
  var parsedData = JSON.parse(event.data);
  var peerUsername = parsedData["peer"];
  var action = parsedData["action"];

  if (username == peerUsername) {
    return;
  }

  var receiver_channel_name = parsedData["message"]["receiver_channel_name"];

  if (action == "new-peer") {
    createOfferer(peerUsername, receiver_channel_name);
  }

  if (action == "new-offer") {
    var offer = parsedData["message"][sdp];
    createAnswerer(offer, peerUsername, receiver_channel_name);

    return;
  }

  if (action == "new-answer") {
    var answer = parsedData["message"]["sdp"];

    var peer = mapPeers[peerUsername][0];

    peer.setRemoteDescription(answer);
    return;
  }
}

btnJoin.addEventListener("click", () => {
  username = usernameInput.value;
  console.log("username");

  if (username == "") {
    return;
  }
  usernameInput.value = "";
  usernameInput.disabled = true;
  usernameInput.style.visibility = "hidden";

  btnJoin.disabled = true;
  btnJoin.style.visibility = "hidden";

  var labelusername = document.querySelector("#label-username");
  labelusername.innerHTML = username;

  var loc = window.location;
  var wsStart = "ws://";

  if (loc.protocol == "https:") {
    wsStart = "wss://";
  }

  //   ws://127.0.0.1:8000/chat/chats/
  var endPoint = wsStart + loc.host + loc.pathname;

  console.log("endpoint; ", endPoint);

  webSocket = new WebSocket(endPoint);

  webSocket.addEventListener("open", (e) => {
    console.log("connection Opened");
    sendSignal("new-peer", {});
  });
  webSocket.addEventListener("message", webSocketOnMessage);
  webSocket.addEventListener("close", (e) => {
    console.log("connection Closed");
  });
  webSocket.addEventListener("error", (e) => {});
});

var localStream = new MediaStream();

const constraints = {
  video: true,
  audio: true,
};

const localVideo = document.querySelector("#local-video");

const btnToggleAudio = document.querySelector("#btn-toggle-audio");
const btnToggleVideo = document.querySelector("#btn-toggle-video");

var userMedia = navigator.mediaDevices
  .getUserMedia(constraints)
  .then((stream) => {
    localStream = stream;
    localVideo.srcObject = localStream;
    localVideo.muted = true;

    var audioTracks = stream.getAudioTracks();
    var videoTracks = stream.getVideoTracks();

    audioTracks[0].enabled = true;
    videoTracks[0].enabled = true;

    btnToggleAudio.addEventListener("click", () => {
      audioTracks[0].enabled = !audioTracks[0].enabled;
      if (audioTracks[0].enabled) {
        btnToggleAudio.innerHTML = "Audio Mute";

        return;
      }
      btnToggleAudio.innerHTML = "Audio unmute";
    });

    btnToggleVideo.addEventListener("click", () => {
      videoTracks[0].enabled = !videoTracks[0].enabled;
      if (videoTracks[0].enabled) {
        btnToggleVideo.innerHTML = "Video Off";

        return;
      }
      btnToggleVideo.innerHTML = "Video unmute";
    });
  })
  .catch((error) => {
    console.log("Error Accessing media devicess", error);
  });

function sendSignal(action, message) {
  var jsonStr = JSON.stringify({
    peer: username,
    action: action,
    message: message,
  });
  webSocket.send(jsonStr);
}

// will only connect devices inside the same network e.g wifi, for different network it will take a dictionary
function createOfferer(peerUsername, receiver_channel_name) {
  var peer = new RTCPeerConnection(null);

  addLocalTracks(peer);

  var dc = peer.createDataChannel("channel");
  dc.addEventListener("open", () => {
    console.log("Connection Open");
  });
  dc.addEventListener("message", dcOnMessage);

  var remoteVideo = createVideo(peerUsername);
  setOnTrack(peer, remoteVideo);
  mapPeers[peerUsername] = [peer, dc];

  peer.addEventListener("iceconnectionstatechange", () => {
    var iceconnectionstate = peer.iceConnectionState;

    if (
      iceconnectionstate === "failed" ||
      iceconnectionstate === "disconnected" ||
      iceconnectionstate === "closed"
    ) {
      delete mapPeers[peerUsername];

      if (iceconnectionstate != "closed") {
        peer.close();
      }

      removeVideo(remoteVideo);
    }
  });
  peer.addEventListener("icecandidate", (event) => {
    if (event.candidate) {
      console.log("New ice candidate ", JSON.stringify(peer.localDescription));

      return;
    }

    sendSignal("new-offer", {
      sdp: peer.localDescription,
      receiver_channel_name: receiver_channel_name,
    });
  });
  peer
    .createOffer((e) => peer.setLocalDescription(e))
    .then(() => {
      console.log("local description set Successfully");
    });
}

function addLocalTracks(peer) {
  localStream.getTracks().forEach((track) => {
    peer.addTrack(track, localStream);
  });
}

var messageList = document.querySelector("message-list");

function dcOnMessage(event) {
  var message = event.data;

  var li = document.createElement("li");
  li.appendChild(document.createTextNode(message));
  messageList.appendChild(li);
}

function createVideo(peerUsername) {
  var videoContainer = document.querySelector("#video-container");

  var remoteVideo = document.createElement("video");
  remoteVideo.id = peerUsername + "-video";
  remoteVideo.autoplay = true;
  remoteVideo.playsInline = true;

  var videowrapper = document.createElement("div");
  videoContainer.appendChild(videowrapper);

  return remoteVideo;
}

function setOnTrack(peer, remoteVideo) {
  var remoteStream = new MediaStream();

  remoteVideo.srcObject = remoteStream;
  peer.addEventListener("track", async (event) => {
    remoteStream.addTrack(event.track, remoteStream);
  });
}

function removeVideo(remoteVideo) {
  var videoWrapper = video.parentNode;

  videoWrapper.parentNode.removeChild(videoWrapper);
}

function createAnswerer(offer, peerUsername, receiver_channel_name) {
  var peer = new RTCPeerConnection(null);

  addLocalTracks(peer);

  var dc = peer.createDataChannel("channel");
  dc.addEventListener("open", () => {
    console.log("Connection Open");
  });
  dc.addEventListener("message", dcOnMessage);

  var remoteVideo = createVideo(peerUsername);
  setOnTrack(peer, remoteVideo);

  peer.addEventListener("datachannel", (e) => {
    peer.dc = e.channel;
    dc.addEventListener("open", () => {
      console.log("Connection Open");
    });
    peer.dc.addEventListener("message", dcOnMessage);
    mapPeers[peerUsername] = [peer, peer.dc];
  });

  peer.addEventListener("iceconnectionstatechange", () => {
    var iceconnectionstate = peer.iceConnectionState;

    if (
      iceconnectionstate === "failed" ||
      iceconnectionstate === "disconnected" ||
      iceconnectionstate === "closed"
    ) {
      delete mapPeers[peerUsername];

      if (iceconnectionstate != "closed") {
        peer.close();
      }

      removeVideo(remoteVideo);
    }
  });
  peer.addEventListener("icecandidate", (event) => {
    if (event.candidate) {
      console.log("New ice candidate ", JSON.stringify(peer.localDescription));

      return;
    }

    sendSignal("new-answer", {
      sdp: peer.localDescription,
      receiver_channel_name: receiver_channel_name,
    });
  });
  peer
    .setRemoteDescription(offer)
    .then(() => {
      console.log("remote description set", peerUsername);
      return peer.createAnswer();
    })
    .then((a) => {
      console.log("Answer Created");

      peer.setLocalDescription(a);
    });
}
