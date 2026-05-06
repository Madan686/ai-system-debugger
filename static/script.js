async function analyzeError() {

    const errorInput = document.getElementById("errorInput");
    const loading = document.getElementById("loading");
    const resultBox = document.getElementById("result");

    const summary = document.getElementById("summary");
    const rootCause = document.getElementById("rootCause");
    const fixSteps = document.getElementById("fixSteps");

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
                fix_steps: [...]
            }
        */

        summary.textContent = data.analysis.summary;

        rootCause.textContent = data.analysis.root_cause;

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