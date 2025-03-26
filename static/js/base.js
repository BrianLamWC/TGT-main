function loadUrl(path) {
    window.location.href = path;
}

document.querySelectorAll('.excercise-tag-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tagContent = button.nextElementSibling;
        button.classList.toggle('excercise-tag-btn-active');
        if (button.classList.contains('excercise-tag-btn-active')) {
            tagContent.style.maxHeight = '700px';
            button.style.borderBottomLeftRadius = '0px'
            button.style.borderBottomRightRadius = '0px'
        } else {
            tagContent.style.maxHeight = 0;
            button.style.borderBottomLeftRadius = '10px'
            button.style.borderBottomRightRadius = '10px'
        }
    });
});

