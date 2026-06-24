document.addEventListener("DOMContentLoaded", function () {

    // Sidebar

    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");

    sidebarToggle?.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
    });


    // Theme

    function setTheme(theme) {

        document.documentElement.setAttribute(
            "data-theme",
            theme
        );

        localStorage.setItem(
            "splitledger_theme",
            theme
        );

        const themeButton =
            document.getElementById("themeToggle");

        if (themeButton) {

            const icon =
                themeButton.querySelector("i");

            if (icon) {

                if (theme === "dark") {
                    icon.className = "bi bi-sun";
                } else {
                    icon.className = "bi bi-moon-stars";
                }

            }

        }

    }


    setTheme(
        localStorage.getItem("splitledger_theme")
        || "light"
    );


    document
        .getElementById("themeToggle")
        ?.addEventListener("click", function () {

            const currentTheme =
                document.documentElement.getAttribute("data-theme");

            if (currentTheme === "dark") {
                setTheme("light");
            } else {
                setTheme("dark");
            }

        });

});