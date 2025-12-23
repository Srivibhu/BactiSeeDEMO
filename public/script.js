async function runAnalysis() {
    const imageFile = document.getElementById('imageInput').files[0];
    const statusText = document.getElementById('statusText');
    const bar = document.getElementById('gaugeBar');

    if (!imageFile) {
        alert("Please capture or select an image first!");
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    // Add visual "Scanning" feedback
    statusText.innerText = "🔍 SCANNING SURFACE...";
    statusText.classList.add('scanning');
    bar.style.width = "0%";

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        statusText.classList.remove('scanning');

        // Logic using your new percentage data
        const percent = data.percentage ?? 0;
        const status = data.safetyLevel ?? "Safe";
        
        // Update Gauge
        bar.style.width = Math.min(100, percent * 5) + "%"; // Scaled for visibility

        // Graphical Feedback (Icons and Colors)
        if (status === "Danger") {
            bar.style.backgroundColor = "#dc3545"; // Dark Red
            statusText.innerHTML = `🚨 <strong>DANGER:</strong> Contamination High (${percent}%)`;
        } else if (status === "Warning") {
            bar.style.backgroundColor = "#ffc107"; // Amber
            statusText.innerHTML = `⚠️ <strong>WARNING:</strong> Trace Detection (${percent}%)`;
        } else {
            bar.style.backgroundColor = "#28a745"; // Green
            statusText.innerHTML = `✅ <strong>SAFE:</strong> Surface Clean (${percent}%)`;
        }

    } catch (err) {
        statusText.innerText = "❌ Connection Error: Is the backend running?";
        statusText.classList.remove('scanning');
    }
}
