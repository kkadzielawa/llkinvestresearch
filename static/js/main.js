menuBtn = document.querySelector('.menu-btn');
mainMenu = document.querySelector('.main-menu');

menuBtn.addEventListener('click', () => {
    mainMenu.classList.toggle('show');
})