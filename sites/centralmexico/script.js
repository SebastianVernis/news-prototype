document.addEventListener('DOMContentLoaded', function() {
    const preloader = document.getElementById('preloader');
    setTimeout(() => { preloader.classList.add('hidden'); setTimeout(() => { preloader.style.display = 'none'; }, 500); }, 1000);

    const cards = document.querySelectorAll('.mag-card, .news-card, .mag-hero');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Article clicked');
        });
    });

    const navLinks = document.querySelectorAll('.nav-link');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    navLinks.forEach(link => { if (link.getAttribute('href') === currentPage) link.classList.add('active'); });

    console.log('Central México - Site loaded');
});
