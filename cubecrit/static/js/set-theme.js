/**
 * Sets the user's color theme.
 * @param {string} theme - "light" for light theme or "dark" for dark theme.
 */
function setTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem("theme", theme);
    var light_dropdown = document.getElementById("theme-light");
    var dark_dropdown = document.getElementById("theme-dark");
    if (theme === "dark") {
        light_dropdown.classList.remove("active");
        dark_dropdown.classList.add("active");
    } else {
        dark_dropdown.classList.remove("active");
        light_dropdown.classList.add("active");
    }
}