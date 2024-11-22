document.getElementById('clear-file').addEventListener('click', function () {
	document.getElementById('file-upload').value = ''; // Clear the file input
});

// Function to enable the retrain button once a file is uploaded
function enableRetrainButton() {
	const fileInput = document.querySelector('#file-upload');
	const retrainButton = document.querySelector('#retrainButton');

	// Check if a file is selected
	if (fileInput.files.length > 0) {
		retrainButton.disabled = false; // Enable retrain button
	} else {
		retrainButton.disabled = true; // Keep it disabled if no file selected
	}
}

// Function to handle the retraining process once the button is clicked
function retrainModel() {
	const retrainButton = document.querySelector('#retrainButton');
	const progressBar = document.querySelector('.progress-bar');
	const resultMessage = document.querySelector('.result-message');
	const progressContainer = document.querySelector('.progress-container');
	const fileInput = document.querySelector('#file-upload');

	// Ensure a file is uploaded before retraining
	if (fileInput.files.length === 0) {
		alert('Please upload a dataset first.');
		return; // Exit the retraining process if no file is selected
	}

	// Disable the retrain button during retraining
	retrainButton.disabled = true;

	// Show progress bar and start retraining
	progressContainer.style.display = 'block';
	progressBar.style.width = '0%';
	progressBar.style.transition = 'none'; // Remove transition during update

	// Simulate retraining process
	setTimeout(function () {
		progressBar.style.transition = 'width 2s ease-in-out'; // Re-enable smooth transition
		progressBar.style.width = '100%'; // Fill progress bar

		// After retraining is complete, show the result message
		setTimeout(function () {
			resultMessage.style.opacity = 1;
			resultMessage.textContent = 'Retraining complete!';

			// Re-enable retrain button after a short delay
			retrainButton.disabled = false;
		}, 2000); // Delay for progress bar to fill
	}, 3000); // Simulate retraining time (replace with actual logic)
}
