window.addEventListener('scroll', function() {
    var scrollIndicator = document.querySelector('.scroll-indicator');
    if (window.pageYOffset > 100) {
        scrollIndicator.style.opacity = '0';
        scrollIndicator.style.visibility = 'hidden';
    } else {
        scrollIndicator.style.opacity = '1';
        scrollIndicator.style.visibility = 'visible';
    }
});
