/* Carousel + Sidebar Functionality */
let currentSlide = 0;
let autoPlayInterval;

function initCarousel() {
    const slides = document.querySelectorAll('.carousel-slide');
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const dots = document.querySelectorAll('.carousel-dot');
    
    if (slides.length === 0) return;
    
    // Show first slide
    showSlide(0);
    
    // Auto-play
    startAutoPlay();
    
    // Event listeners for buttons
    document.querySelector('.carousel-btn.prev')?.addEventListener('click', () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
        resetAutoPlay();
    });
    
    document.querySelector('.carousel-btn.next')?.addEventListener('click', () => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
        resetAutoPlay();
    });
    
    // Event listeners for dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
            resetAutoPlay();
        });
    });
    
    // Event listeners for sidebar items
    sidebarItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
            resetAutoPlay();
        });
    });
}

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-slide');
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const dots = document.querySelectorAll('.carousel-dot');
    
    // Hide all slides
    slides.forEach(slide => slide.classList.remove('active'));
    sidebarItems.forEach(item => item.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    // Show current slide
    if (slides[index]) slides[index].classList.add('active');
    if (sidebarItems[index]) sidebarItems[index].classList.add('active');
    if (dots[index]) dots[index].classList.add('active');
    
    currentSlide = index;
}

function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
        currentSlide = (currentSlide + 1) % document.querySelectorAll('.carousel-slide').length;
        showSlide(currentSlide);
    }, 5000); // Change slide every 5 seconds
}

function resetAutoPlay() {
    clearInterval(autoPlayInterval);
    startAutoPlay();
}

// Pause on hover
document.querySelector('.carousel-main')?.addEventListener('mouseenter', () => {
    clearInterval(autoPlayInterval);
});

document.querySelector('.carousel-main')?.addEventListener('mouseleave', () => {
    startAutoPlay();
});

// Initialize on load
document.addEventListener('DOMContentLoaded', initCarousel);
