/* -------------------------------------------------
   Utility: show only the requested wizard step
   ------------------------------------------------- */
function showStep(stepNumber) {
    document.querySelectorAll('.wizard-step').forEach(sec => sec.classList.add('d-none'));
    document.getElementById(`step-${stepNumber}`).classList.remove('d-none');
}

/* -------------------------------------------------
   STEP 1 → STEP 2 : upload CSV & store it on the server
   ------------------------------------------------- */
document.getElementById('nextBtn1').addEventListener('click', async () => {
    const fileInput = document.getElementById('csvFile');
    if (!fileInput.files.length) {
        alert('Please select a CSV file.');
        return;
    }

    const formData = new FormData();
    formData.append('csv_file', fileInput.files[0]);

    try {
        const resp = await fetch('/api/upload-pipeline', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || 'Upload failed');

        // Store the temporary filename returned by the server
        window.sessionStorage.setItem('uploadedFile', data.temp_filename);
        showStep(2);
    } catch (e) {
        alert('Error uploading file: ' + e.message);
    }
});

/* -------------------------------------------------
   Show rename inputs only when the rename checkbox is checked
   ------------------------------------------------- */
document.getElementById('tRenameCol').addEventListener('change', function () {
    document.getElementById('renameInputs').classList.toggle('d-none', !this.checked);
});

/* -------------------------------------------------
   STEP 2 → STEP 3 : send selected transformations, get preview
   ------------------------------------------------- */
document.getElementById('nextBtn2').addEventListener('click', async () => {
    const tempFile = window.sessionStorage.getItem('uploadedFile');
    if (!tempFile) {
        alert('No uploaded file found – go back to step 1.');
        return;
    }

    // Gather selected transformations
    const selected = [];
    document.querySelectorAll('#transformForm input[name="transformation"]:checked')
        .forEach(cb => selected.push(cb.value));

    const payload = {
        temp_filename: tempFile,
        transformations: selected
    };

    // Add rename details if needed
    if (selected.includes('rename_column')) {
        payload.rename = {
            old_name: document.getElementById('oldName').value.trim(),
            new_name: document.getElementById('newName').value.trim()
        };
        if (!payload.rename.old_name || !payload.rename.new_name) {
            alert('Please fill both old and new column names for rename.');
            return;
        }
    }

    try {
        const resp = await fetch('/api/preview-pipeline', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || 'Preview failed');

        // Navigate to the download page
        window.location.href = '/download';
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

/* -------------------------------------------------
   Navigation buttons (Back)
   ------------------------------------------------- */
document.getElementById('backBtn2').addEventListener('click', () => showStep(1));
document.getElementById('backBtn3').addEventListener('click', () => showStep(2));

/* -------------------------------------------------
   Download button – triggers download of transformed CSV
   ------------------------------------------------- */
document.getElementById('finishBtn').addEventListener('click', () => {
    // Create a temporary link and trigger download
    const link = document.createElement('a');
    link.href = '/download-csv';
    link.download = 'transformed_data.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    alert('Download started! Your file is being saved.');
});
