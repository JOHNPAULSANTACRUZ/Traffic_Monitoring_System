
const addCameraButton = document.getElementById('add-camera');
const cameraContainer = document.querySelector('.camera-container');
let cameraCount =0;

addCameraButton.addEventListener('click', () => {
  const newVideo = document.createElement('video');
  newVideo.width = '640';
  newVideo.height = '640';
  newVideo.className = 'video-wrapper';
  newVideo.autoplay = true;
  
  // add CSS rules to position the video element
  //newVideo.style.position = 'relative';
  
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      newVideo.srcObject = stream;
      cameraContainer.appendChild(newVideo);
    })
    .catch(error => {
      console.error(error);
    });
});

// Get elements
const logoutButton = document.getElementById('logoutButton');
const logoutPrompt = document.getElementById('logoutPrompt');
const confirmLogoutButton = document.getElementById('confirmLogoutButton');
const cancelLogoutButton = document.getElementById('cancelLogoutButton');

// Show the logout prompt
logoutButton.addEventListener('click', () => {
logoutPrompt.classList.remove('hidden');
});

// Hide the logout prompt when cancel button is clicked
cancelLogoutButton.addEventListener('click', () => {
logoutPrompt.classList.add('hidden');
});

// Perform logout when confirm button is clicked
confirmLogoutButton.addEventListener('click', () => {
// You can add your logout logic here

alert('Logged out successfully!');
sessionStorage.clear();
window.location.href = 'index.html';

});