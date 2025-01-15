// static/js/theme.js
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const htmlElement = document.documentElement;

// Vérifier les préférences système
const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

// Appliquer le thème initial
if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && systemPrefersDark)) {
  htmlElement.classList.add('dark');
  themeIcon.textContent = '🌞'; // Icône pour le mode clair
} else {
  htmlElement.classList.remove('dark');
  themeIcon.textContent = '🌙'; // Icône pour le mode sombre
}

// Basculer entre les modes clair et sombre
themeToggleBtn.addEventListener('click', () => {
  if (htmlElement.classList.contains('dark')) {
    htmlElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
    themeIcon.textContent = '🌙';
  } else {
    htmlElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
    themeIcon.textContent = '🌞';
  }
});