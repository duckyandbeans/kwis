// public/js/main.js

async function postData(url, data) {
    console.log(`Attempting to send data to: ${url}`); // Debug log

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        // 1. Check for Server Errors (Red Lights)
        if (!response.ok) {
            // Read the text response (usually an HTML error page from Vercel)
            const errorText = await response.text(); 
            console.error(`Server Error ${response.status}:`, errorText);

            if (response.status === 404) {
                throw new Error("404 Not Found: The website cannot find the Python file.");
            }
            if (response.status === 500) {
                throw new Error("500 Server Error: The Python code crashed (Check logs).");
            }
            throw new Error(`Server Error: ${response.status}`);
        }

        // 2. Success? Parse the JSON
        return await response.json();

    } catch (error) {
        console.error('Detailed Fetch Error:', error);
        
        // Show specific alerts so you know what to fix
        if (error.message.includes("404")) {
            alert("System Error (404): API Route not found. The `vercel.json` configuration is likely wrong.");
        } else if (error.message.includes("500")) {
            alert("System Error (500): The backend crashed. Check '__init__.py' files or Environment Variables.");
        } else {
            alert(`Connection Error: ${error.message}`);
        }
        return null;
    }
}
