// public/js/autosave.js
document.addEventListener("DOMContentLoaded", () => {
    // 1. Generate Unique Key based on URL + Input Name
    const getStorageKey = (name) => `autosave_${window.location.pathname}_${name}`;

    const inputs = document.querySelectorAll("input, textarea, select");

    inputs.forEach(input => {
        const key = getStorageKey(input.name);

        // A. LOAD SAVED DATA
        const saved = localStorage.getItem(key);
        if (saved) {
            if (input.type === "radio" || input.type === "checkbox") {
                if (input.value === saved) input.checked = true;
            } else {
                input.value = saved;
            }
        }

        // B. SAVE ON CHANGE
        input.addEventListener("input", (e) => {
            const val = e.target.value;
            // Only save radio if checked
            if (e.target.type === "radio" && !e.target.checked) return;
            localStorage.setItem(key, val);
        });
    });
});

// Call this when quiz is successfully submitted
function clearAutoSave() {
    console.log("Clearing local storage...");
    const inputs = document.querySelectorAll("input, textarea, select");
    inputs.forEach(input => {
        localStorage.removeItem(`autosave_${window.location.pathname}_${input.name}`);
    });
}