// Expenso Slide Deck Interactive Controller with Directional Transitions
const PresentationDeck = (() => {
  let currentSlide = 0;
  let slides = [];
  let indicator = null;
  let prevBtn = null;
  let nextBtn = null;

  function init() {
    slides = document.querySelectorAll(".slide");
    indicator = document.getElementById("slideIndicator");
    prevBtn = document.getElementById("prevBtn");
    nextBtn = document.getElementById("nextBtn");

    window.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
        e.preventDefault(); nextSlide();
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault(); prevSlide();
      } else if (e.key === "f" || e.key === "F") {
        toggleFullScreen();
      }
    });

    updateSlide("none");
  }

  function updateSlide(direction = "next") {
    if (!slides.length) return;
    slides.forEach((s, idx) => {
      s.classList.remove("active", "slide-next", "slide-prev");
      if (idx === currentSlide) {
        s.classList.add("active");
        if (direction === "next") s.classList.add("slide-next");
        else if (direction === "prev") s.classList.add("slide-prev");
      }
    });
    if (indicator) indicator.innerText = `Slide ${currentSlide + 1} of ${slides.length}`;
    if (prevBtn) prevBtn.disabled = currentSlide === 0;
    if (nextBtn) nextBtn.disabled = currentSlide === slides.length - 1;
  }

  function nextSlide() {
    if (currentSlide < slides.length - 1) {
      currentSlide++;
      updateSlide("next");
    }
  }

  function prevSlide() {
    if (currentSlide > 0) {
      currentSlide--;
      updateSlide("prev");
    }
  }

  function toggleFullScreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  return { init, nextSlide, prevSlide, toggleFullScreen };
})();

document.addEventListener("DOMContentLoaded", () => PresentationDeck.init());
