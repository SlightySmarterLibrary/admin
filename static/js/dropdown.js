function toggleClass(event) {
  const parent = event.target.parentNode;

  if (parent) {
    if (parent.querySelector('.dropdown-content') !== null) {
      parent.querySelector('.dropdown-content').classList.toggle('show');
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.getElementsByClassName('dropdown-parent');

  if (dropdown) {
    for (let i = 0; i < dropdown.length; i += 1) {
      dropdown[i].addEventListener('click', toggleClass);
    }
  }
});

// Hides dropdown button when user click anywhere else
window.onclick = function hideDropdown(event) {
  if (!event.target.matches('.dropdownBtn')) {
    const dropdowns = document.getElementsByClassName('dropdown-content');

    for (let i = 0; i < dropdowns.length; i += 1) {
      const openDropdown = dropdowns[i];

      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.toggle('show');
      }
    }
  }
};