// The header blends into the page at the top and turns solid once scrolled (see extra.css)
if (!window.dobHeaderState) {
    window.dobHeaderState = function() {
        document.documentElement.classList.toggle("dob-top", window.scrollY < 4);
    };
    window.addEventListener("scroll", window.dobHeaderState, { passive: true });
}
window.dobHeaderState();

document.addEventListener("DOMContentLoaded", function() {
    const lightboxLinks = [];

    document.querySelectorAll('.md-typeset img').forEach(img => {
        // Skip if already inside a link
        if (img.parentNode.tagName.toLowerCase() === 'a') return;

        // Wrap image in <a> for lightbox
        const link = document.createElement('a');
        link.href = img.src;
        link.classList.add('glightbox');
        img.parentNode.insertBefore(link, img);
        link.appendChild(img);

        // Add zoom icon on hover
        link.style.position = 'relative';
        link.style.display = 'inline-block';
    });

    // Initialize GLightbox
    GLightbox({ selector: '.glightbox' });
});