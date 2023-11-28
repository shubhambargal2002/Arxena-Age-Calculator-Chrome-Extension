// This code runs on every page matching the specified patterns

// For example, you can insert a red border around all images on the page
const images = document.getElementsByTagName('img');
for (const img of images) {
  img.style.border = '2px solid red';
}

// You can add more code here depending on what you want to achieve on the web pages.
