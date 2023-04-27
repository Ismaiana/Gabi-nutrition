// Photo slider in homepage

const slider = document.querySelector('.slider');
const prevSlideBtn = document.querySelector('.prev-slide');
const nextSlideBtn = document.querySelector('.next-slide');
let slideIndex = 0;

function moveSlider() {
  slider.style.transform = `translateX(-${slideIndex * 100 / 5}%)`;
}

function nextSlide() {
  if (slideIndex === 4) {
    slideIndex = 0;
  } else {
    slideIndex++;
  }
  moveSlider();
}

function prevSlide() {
  if (slideIndex === 0) {
    slideIndex = 4;
  } else {
    slideIndex--;
  }
  moveSlider();
}

nextSlideBtn.addEventListener('click', nextSlide);
prevSlideBtn.addEventListener('click', prevSlide);
setInterval(nextSlide, 5000);





// show hidden pictures in results page

const showMoreBtn = document.getElementById('show-more-btn');
const photosClients = document.querySelector('.photos-clients');
const photoClients = document.querySelectorAll('.photo-clients');
const numPhotosToShow = 4;

for (let i = numPhotosToShow; i < photoClients.length; i++) {
  photoClients[i].classList.add('hidden');
}

showMoreBtn.addEventListener('click', () => {
  const numVisiblePhotos = document.querySelectorAll('.photo-clients:not(.hidden)').length;

  for (let i = numVisiblePhotos; i < numVisiblePhotos + numPhotosToShow && i < photoClients.length; i++) {
    photoClients[i].classList.remove('hidden');
  }
 
  if (document.querySelectorAll('.photo-clients.hidden').length === 0) {
    showMoreBtn.classList.add('hidden');
  }
});