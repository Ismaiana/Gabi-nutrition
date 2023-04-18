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