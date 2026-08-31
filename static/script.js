// Wait for the DOM to load before setting up event listeners
document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');

    // Trigger prompt sending when user clicks the button
    submitBtn.addEventListener('click', sendPrompt);
});

async function sendPrompt() {
    const promptInput = document.getElementById('promptInput');
    const modelSelect = document.getElementById('modelSelect');
    const submitBtn = document.getElementById('submitBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const outputCard = document.getElementById('outputCard');
    const outputText = document.getElementById('outputText');
    const modelTag = document.getElementById('modelTag');

    // Metadata DOM elements
    const metaSection = document.getElementById('metaSection');
    const reqId = document.getElementById('reqId');
    const providerTag = document.getElementById('providerTag');
    const tokenUsage = document.getElementById('tokenUsage');
    const costTag = document.getElementById('costTag');

    const prompt = promptInput.value.trim();
    const model = modelSelect.value;
    if (!prompt) return;

    // Set UI to loading state
    submitBtn.disabled = true;
    btnSpinner.style.display = 'block';
    outputCard.style.display = 'none';
    outputCard.classList.remove('error');
    metaSection.style.display = 'none';

    try {
        // Make the network request to the backend '/chat' endpoint
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt, model: model })
        });

        const data = await response.json();

        // Check if the backend returned any error
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred while processing the request.');
        }

        // Display the output and model details in the card
        outputText.innerText = data.output;
        modelTag.innerText = data.model;

        // Populate metadata
        reqId.innerText = data.id;
        providerTag.innerText = data.provider.toUpperCase();
        tokenUsage.innerText = `${data.usage.total_tokens} (Prompt: ${data.usage.input_tokens} | Completion: ${data.usage.output_tokens})`;
        costTag.innerText = `$${data.cost.provider_cost.toFixed(6)}`;

        // Show metadata section
        metaSection.style.display = 'flex';
        outputCard.style.display = 'block';
    } catch (error) {
        // Display the error message in the UI
        outputText.innerText = error.message;
        modelTag.innerText = 'Error';
        outputCard.classList.add('error');
        outputCard.style.display = 'block';
        metaSection.style.display = 'none';
    } finally {
        // Reset the UI to its active state
        submitBtn.disabled = false;
        btnSpinner.style.display = 'none';
    }
}
