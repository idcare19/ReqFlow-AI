document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        window.setTimeout(() => {
            if (alert.classList.contains("show")) {
                const closeButton = alert.querySelector(".btn-close");
                if (closeButton) {
                    closeButton.click();
                }
            }
        }, 4000);
    });
});
