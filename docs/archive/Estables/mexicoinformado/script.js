/* ========================================
   México Informado - JavaScript
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Hide preloader
    const preloader = document.getElementById('preloader');
    setTimeout(() => {
        preloader.classList.add('hidden');
        setTimeout(() => { preloader.style.display = 'none'; }, 500);
    }, 1000);

    // Article cards click handlers
    const articleCards = document.querySelectorAll('.news-card, .card-hero');
    articleCards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Article clicked');
        });
    });

    // Active navigation link
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });

    // Sticky header shadow on scroll
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 100) {
            header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
        } else {
            header.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        }
    });

    console.log('México Informado - Site loaded successfully');
});
