/* Carousel + Interaction Functionality */
let currentSlide = 0;
let autoPlayInterval;

function initCarousel() {
    const slides = document.querySelectorAll(".carousel-slide");
    if (slides.length === 0) return;
    showSlide(0);
    startAutoPlay();
    document.querySelector(".carousel-btn.prev")?.addEventListener("click", () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide); resetAutoPlay();
    });
    document.querySelector(".carousel-btn.next")?.addEventListener("click", () => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide); resetAutoPlay();
    });
}

function showSlide(index) {
    const slides = document.querySelectorAll(".carousel-slide");
    const dots = document.querySelectorAll(".carousel-dot");
    slides.forEach(s => s.classList.remove("active"));
    dots.forEach(d => d.classList.remove("active"));
    if (slides[index]) slides[index].classList.add("active");
    if (dots[index]) dots[index].classList.add("active");
    currentSlide = index;
}

function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
        const slides = document.querySelectorAll(".carousel-slide");
        if (slides.length === 0) return;
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }, 5000);
}

function resetAutoPlay() { clearInterval(autoPlayInterval); startAutoPlay(); }

document.querySelector(".carousel-main")?.addEventListener("mouseenter", () => clearInterval(autoPlayInterval));
document.querySelector(".carousel-main")?.addEventListener("mouseleave", () => startAutoPlay());

document.addEventListener("DOMContentLoaded", initCarousel);