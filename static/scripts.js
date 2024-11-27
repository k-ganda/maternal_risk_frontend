let uploadedFilePath = ''; // To store the file path after upload

// Handle file upload
async function uploadFile() {
	const fileInput = document.getElementById('file-upload');
	const file = fileInput.files[0]; // Get the first file

	if (!file) {
		alert('Please select a file first.');
		return;
	}

	const formData = new FormData();
	formData.append('file', file);

	try {
		// Send the file to the backend
		const response = await fetch('/upload-data', {
			method: 'POST',
			body: formData,
		});

		const result = await response.json();

		if (response.ok) {
			alert(result.message); // Show success message

			uploadedFilePath = result.file_path.replace(/\\/g, '/'); // Store the file path for retraining
			console.log('File path after upload:', uploadedFilePath);
			document.getElementById('retrainButton').disabled = false; // Enable retrain button
		} else {
			alert('Error uploading data: ' + result.detail);
		}
	} catch (error) {
		console.error('Error during file upload:', error);
		alert('An error occurred while uploading the file.');
	}
}

// Handle the retrain process
async function retrainModel() {
	if (!uploadedFilePath) {
		alert('No file uploaded. Please upload a file first.');
		return;
	}

	console.log('Sending file path to retrain:', uploadedFilePath);

	// Disable the retrain button to prevent multiple clicks
	document.getElementById('retrainButton').disabled = true;
	document.getElementById('retrainButton').innerText = 'Retraining...'; // Change button text

	try {
		// Send the file path to retrain the model
		const response = await fetch('/retrain', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ file_path: uploadedFilePath }), // send file_path in JSON body
		});

		const result = await response.json();

		if (response.ok) {
			alert(
				`Model retrained successfully! Model version: ${result.model_version}`
			);
			document.getElementById('retrainButton').innerText = 'Retrain Model'; // Reset button text
			document.getElementById('retrainButton').disabled = false; // Re-enable button for further retraining
		} else {
			let errorMessage = result.detail || 'An unknown error occurred.';
			if (result.error) {
				errorMessage += ` Error: ${JSON.stringify(result.error)}`;
			}
			alert('Error retraining model: ' + result.detail);
			document.getElementById('retrainButton').innerText = 'Retrain Model'; // Reset button text
			document.getElementById('retrainButton').disabled = false; // Re-enable button
		}
	} catch (error) {
		console.error('Error during model retraining:', error);
		alert('An error occurred while retraining the model.');
		document.getElementById('retrainButton').innerText = 'Retrain Model'; // Reset button text
		document.getElementById('retrainButton').disabled = false; // Re-enable button
	}
}

// Handle file input clearing
function clearFileInput() {
	document.getElementById('file-upload').value = '';
	uploadedFilePath = ''; // Reset the uploaded file path
	document.getElementById('retrainButton').disabled = true; // Disable retrain button
	document.getElementById('retrainButton').innerText = 'Retrain Model'; // Reset button text
}
