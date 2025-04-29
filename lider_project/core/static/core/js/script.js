document.addEventListener('DOMContentLoaded', () => {
    const burgerMenu = document.querySelector('.burger-menu');
    const nav = document.querySelector('header nav');
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    const headerHeight = document.querySelector('header').offsetHeight;

    // Проверка наличия бургер-меню и навигации
    if (!burgerMenu || !nav) {
        console.error('Burger menu or navigation not found in the DOM');
        return;
    }

    // Переключение бургер-меню при клике на него
    burgerMenu.addEventListener('click', (event) => {
        event.stopPropagation();
        // console.log('Burger menu clicked, toggling active class');
        burgerMenu.classList.toggle('active');
        nav.classList.toggle('active');
    });

    // Закрытие меню при клике вне его области
    document.addEventListener('click', (event) => {
        const isClickInsideMenu = nav.contains(event.target);
        const isClickOnBurger = burgerMenu.contains(event.target);
        const isClickOnIframe = event.target.closest('iframe');

        // console.log('Document clicked', {
        //     isClickInsideMenu,
        //     isClickOnBurger,
        //     isClickOnIframe,
        //     isNavActive: nav.classList.contains('active')
        // });

        if (nav.classList.contains('active') && !isClickInsideMenu && !isClickOnBurger && !isClickOnIframe) {
            // console.log('Closing menu: click outside menu and burger');
            burgerMenu.classList.remove('active');
            nav.classList.remove('active');
        }
    });

    // Обработка скролла и закрытия меню для всех якорных ссылок
    anchorLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // Отменяем стандартное поведение

            const targetId = link.getAttribute('href').substring(1); // Получаем ID секции
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth' // Плавный скролл
                });

                // Закрываем меню, если оно открыто (актуально для ссылок в навигации)
                if (nav.classList.contains('active')) {
                    // console.log('Nav link clicked, closing menu');
                    burgerMenu.classList.remove('active');
                    nav.classList.remove('active');
                }
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
  if (window.location.pathname === "/request/") {
    const hasErrors = /* логика с шаблона */;
    const hasMessages = /* логика с шаблона */;

    if (hasErrors || hasMessages) {
      var myModal = new bootstrap.Modal(document.getElementById('myModal'));
      myModal.show();
    }
  }
});