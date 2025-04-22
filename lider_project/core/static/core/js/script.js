document.addEventListener('DOMContentLoaded', () => {
    const burgerMenu = document.querySelector('.burger-menu');
    const nav = document.querySelector('header nav');
    const navLinks = document.querySelectorAll('header nav ul li a');

    if (!burgerMenu || !nav) {
        console.error('Burger menu or navigation not found in the DOM');
        return;
    }

    // Переключение бургер-меню при клике на него
    burgerMenu.addEventListener('click', (event) => {
        event.stopPropagation();
        console.log('Burger menu clicked, toggling active class');
        burgerMenu.classList.toggle('active');
        nav.classList.toggle('active');
    });

    // Закрытие меню при клике вне его области
    document.addEventListener('click', (event) => {
        // Проверяем, что клик не произошёл на iframe или его потомках
        const iframes = document.querySelectorAll('iframe');
        let isClickOnIframe = false;
        iframes.forEach(iframe => {
            if (iframe.contains(event.target)) {
                isClickOnIframe = true;
            }
        });

        const isClickInsideMenu = nav.contains(event.target);
        const isClickOnBurger = burgerMenu.contains(event.target);

        console.log('Document clicked', {
            isClickInsideMenu,
            isClickOnBurger,
            isClickOnIframe,
            isNavActive: nav.classList.contains('active')
        });

        if (nav.classList.contains('active') && !isClickInsideMenu && !isClickOnBurger && !isClickOnIframe) {
            console.log('Closing menu: click outside menu and burger');
            burgerMenu.classList.remove('active');
            nav.classList.remove('active');
        }
    });

    // Закрытие меню при клике на ссылку в навигации
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            console.log('Nav link clicked, closing menu');
            burgerMenu.classList.remove('active');
            nav.classList.remove('active');

            // Плавная прокрутка к секции
            const targetId = link.getAttribute('href').substring(1); // Убираем "#"
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                event.preventDefault(); // Отменяем стандартное поведение якоря
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Учитываем высоту шапки
                    behavior: 'smooth'
                });
            }
        });
    });
});