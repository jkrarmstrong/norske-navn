
// Dette fungerer. Må bare sette det opp i mot Flask når jeg er ferdig.
const clearBtn = document.querySelector(".clear-button");
const input = document.querySelector(".search-input");

if(clearBtn && input) {
    clearBtn.addEventListener("click", () => {
        input.value = "";
        input.focus();
    });
}

// This also works.
// Toggle .active on visual buttons and update year inputs
const buttons = document.querySelectorAll(".visual-button");
const yearInputsContainer = document.getElementById("year-inputs");

// Define how many inputs each graph requires
const graphConfig = {
    trend: { years: 0 },    // No input
    top10: { years: 1 },    // One year input
    rising: { years: 2 },   // Two year input etc.
    total: { years: 0 },
    prefix: { years: 1 },
};

// Chart description
const graphDescriptions = {
  trend: "Shows how the popularity of a specific name has changed over time.",
  top10: "Displays the 10 most used names in the selected year.",
  rising: "Shows the names with the greatest increase in usage between two years.",
  total: "Displays total number of people named (with any name) per year.",
  prefix: "Shows the most common names that begin with a specific letter or letters.",
};

// Add click event listener to all buttons
buttons.forEach(button => {
    button.addEventListener("click", () => {
    button.classList.toggle("active");                  // Toggle active class
    updateYearInputs();                                 // Refresh input fields 
    });
});

// Generate year input fields based on active buttons
function updateYearInputs() {
    yearInputsContainer.innerHTML = "";                 // Clear current input fields
    
    // Get all selected chart types
    const activeButtons = Array.from(document.querySelectorAll(".visual-button.active"));

    activeButtons.forEach(button => {
        const visual = button.dataset.visual;           // Get graph type
        const config = graphConfig[visual];             // Get how many year inputs it requires

        const group = document.createElement("div");    // Create container for the selected chart
        group.classList.add("year-input-group");        // For styling

        const heading = document.createElement("h3");   // h3 for readability
        heading.textContent = button.textContent;
        group.appendChild(heading);

        const description = document.createElement("p");
        description.textContent = graphDescriptions[visual]; // Hent tekst fra dictionary
        group.appendChild(description);


        if (config.years === 1) {
            const yearInput = document.createElement("input");
            yearInput.type = "number";
            yearInput.placeholder = "Year";             // Placeholder shown in input field
            yearInput.name = `${visual}-year`;          // Name used when submitting form
            group.appendChild(yearInput);
            } else if (config.years === 2) {
            const startInput = document.createElement("input");
            startInput.type = "number";
            startInput.placeholder = "Start year";
            startInput.name = `${visual}-start-year`;
            
            const endInput = document.createElement("input");
            endInput.type = "number";
            endInput.placeholder = "End year";
            endInput.name = `${visual}-end-year`;

            group.appendChild(startInput);
            group.appendChild(endInput);
            }
            
            // Add entire input group to the page
            yearInputsContainer.appendChild(group);
        });
    }