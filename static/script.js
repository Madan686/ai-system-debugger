async function analyzeError() {

    const errorInput = document.getElementById("errorInput");
    const loading = document.getElementById("loading");
    const resultBox = document.getElementById("result");

    const summary = document.getElementById("summary");
    const rootCause = document.getElementById("rootCause");
    const fixSteps = document.getElementById("fixSteps");
    const category=document.getElementById("category");
    const correctedCommand = document.getElementById("correctedCommand");

    const errorText = errorInput.value.trim();

    // Validation
    if (errorText === "") {
        alert("Please paste an error log first.");
        return;
    }

    // Show loading
    loading.classList.remove("hidden");
    resultBox.classList.add("hidden");

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                error_text: errorText
            })
        });

        const data = await response.json();

        // Backend validation failed
        if (!data.success) {
            alert(data.message || "Something went wrong.");
            return;
        }

        /*
            data.analysis is now a JSON object:

            {
                summary: "...",
                root_cause: "...",
                fix_steps: [...],   
                category: "..."
            }
        */

        summary.textContent = data.analysis.summary;
        category.textContent = data.analysis.category;
        rootCause.textContent = data.analysis.root_cause;
        correctedCommand.textContent = data.analysis.corrected_code_or_command;
        // Clear old steps
        fixSteps.innerHTML = "";

        // Add new fix steps
        data.analysis.fix_steps.forEach(function(step) {

            const li = document.createElement("li");

            li.textContent = step;

            fixSteps.appendChild(li);
        });

        // Show result section
        resultBox.classList.remove("hidden");

    } catch (error) {

        console.error(error);

        alert("Failed to connect to backend.");

    } finally {

        loading.classList.add("hidden");
    }
}

function copyCorrectedCommand() {
    const correctedCommand = document.getElementById("correctedCommand");

    const commandText = correctedCommand.textContent.trim();

    if (commandText === "" || commandText === "Not applicable") {
        alert("No command available to copy.");
        return;
    }

    navigator.clipboard.writeText(commandText)
        .then(function() {
            alert("Command copied to clipboard.");
        })
        .catch(function(error) {
            console.error(error);
            alert("Failed to copy command.");
        });
}


async function loadHistory() {

    const historyContainer = document.getElementById("historyContainer");

    historyContainer.innerHTML = "<p>Loading history...</p>";

    try {

        const response = await fetch("/history");

        const data = await response.json();

        if (!data.success) {

            historyContainer.innerHTML = "<p>Failed to load history.</p>";

            return;
        }

        const history = data.history;

        if (history.length === 0) {

            historyContainer.innerHTML = "<p>No history found.</p>";

            return;
        }

        historyContainer.innerHTML = "";

        history.forEach(function(record) {

            const card = document.createElement("div");

            card.classList.add("history-card");

            let fixStepsHtml = "";

            record.fix_steps.forEach(function(step) {

                fixStepsHtml += `<li>${step}</li>`;
            });

            card.innerHTML = `
                <h3>Error</h3>
                <p>${record.error_text}</p>
                
                <h3>Category</h3>
                <p class="category-badge">${record.category}</p>

                <h3>Summary</h3>
                <p>${record.summary}</p>

                <h3>Root Cause</h3>
                <p>${record.root_cause}</p>

                <h3>Possible Location</h3>
                <p>${record.possible_location}</p>

                <h3>Fix Steps</h3>
                <ul>
                    ${fixStepsHtml}
                </ul>

                <h3>Corrected Code / Command</h3>
                <p>${record.corrected_code_or_command}</p>

                <div class="timestamp">
                    Saved At: ${record.created_at}
                </div>
            `;

            historyContainer.appendChild(card);
        });

    } catch (error) {

        console.error(error);

        historyContainer.innerHTML =
            "<p>Failed to connect to backend.</p>";
    }
}