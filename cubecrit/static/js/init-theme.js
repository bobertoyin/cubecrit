/**
 * Initializes the user's color theme.
 */
function initTheme() {
    var theme = localStorage.getItem("theme");
    if (theme !== null) {
        document.documentElement.setAttribute("data-bs-theme", theme);
    }
};

/**
 * Initializes the active color theme selection in the dropdown menu.
 */
function initThemeSelection() {
    var theme = localStorage.getItem("theme");
    var light_dropdown = document.getElementById("theme-light");
    var dark_dropdown = document.getElementById("theme-dark");
    if (theme === "dark") {
        dark_dropdown.classList.add("active");
    } else {
        light_dropdown.classList.add("active");
    }
}

// initialize the theme and theme selection dropdown
initTheme();
window.onload = initThemeSelection;