/**
 * main.js
 * Handles data transmission between the website and the Python backend.
 */

async function postData(url, data) {
    console.log(`🚀 Sending data to: ${url}`); // Helps you see where it's going in Console

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        // 1. Check if the server rejected the request
        if (!response.ok) {
            // Try to read the error text from the server
            const errorText = await response.text();
            console.error(`❌ Server Error ${response.status}:`, errorText);

            // Throw specific errors based on the status code
            if (response.status === 404) {
                throw new Error("404 Not Found: Vercel cannot find the Python file. (Did you forget .py?)");
            }
            if (response.status === 500) {
                throw new Error("500 Server Error: The Python code crashed. (Check Logs: __init__.py or Environment Variable)");
            }
            throw new Error(`Server Error: ${response.status}`);
        }

        // 2. Success! Parse the JSON response
        const jsonResponse = await response.json();
        console.log("✅ Success:", jsonResponse);
        return jsonResponse;

    } catch (error) {
        console.error('Detailed Fetch Error:', error);

        // Show a helpful popup to the user (You)
        if (error.message.includes("404")) {
            alert("⚠️ SYSTEM ERROR (404)\nThe website cannot find the API file.\nFix: Add '.py' to the URL in your HTML file.");
        } else if (error.message.includes("500")) {
            alert("⚠️ CRASH ERROR (500)\nThe Python backend failed.\nFix: Check Vercel Logs for 'ModuleNotFound' or Key errors.");
        } else {
            alert(`⚠️ Connection Error\n${error.message}\nCheck your internet or Vercel deployment.`);
        }
        return null;
    }
}
