document.addEventListener('DOMContentLoaded', () => {
  const mainMenu = document.getElementById('mainHeader');
  const mainMenuLinks = document.getElementById('main-header-links');

  const toggle = function tog() {
    if (mainMenu) {
      if (mainMenu.classList.contains('animate-nav')) {
        mainMenu.classList.remove('animate-nav');
      } else {
        mainMenu.classList.add('animate-nav');
      }

      mainMenuLinks.classList.toggle('collapsed-navbar-show');
    }
  };

  if (mainMenu) {
    mainMenu.addEventListener('click', toggle);
  }
});