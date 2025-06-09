
// Dette fungerer. Må bare sette det opp i mot Flask når jeg er ferdig.
const clearBtn = document.querySelector(".clear-button");
const input = document.querySelector(".search-input");

if(clearBtn && input) {
    clearBtn.addEventListener("click", () => {
        input.value = "";
        input.focus();
    });
}

// Dette fungerer også.
    // Toggle .active på visual-knapper
    const buttons = document.querySelectorAll(".visual-button")

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            button.classList.toggle("active");
        });
    });