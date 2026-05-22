document.addEventListener('DOMContentLoaded', () => {
    const repoUrlInput = document.getElementById('repo-url');
    const buildBtn = document.getElementById('build-btn');
    const statusSection = document.getElementById('status-section');
    const taskIdSpan = document.getElementById('task-id');
    const statusBadge = document.getElementById('status-badge');
    const progressBar = document.getElementById('progress-bar');
    const logsConsole = document.getElementById('logs-console');
    const downloadContainer = document.getElementById('download-container');
    const downloadLink = document.getElementById('download-link');

    let pollingInterval = null;

    buildBtn.addEventListener('click', async () => {
        const repoUrl = repoUrlInput.value.trim();
        if (!repoUrl) {
            alert('Please enter a repository URL');
            return;
        }

        buildBtn.disabled = true;
        statusSection.classList.remove('hidden');
        resetUI();

        try {
            const response = await fetch('/api/v1/build', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ repo_url: repoUrl }),
            });

            if (!response.ok) {
                throw new Error('Failed to start build');
            }

            const data = await response.json();
            taskIdSpan.textContent = data.task_id;
            startPolling(data.task_id);
        } catch (error) {
            alert('Error: ' + error.message);
            buildBtn.disabled = false;
        }
    });

    function resetUI() {
        taskIdSpan.textContent = '-';
        statusBadge.textContent = 'PENDING';
        statusBadge.className = 'badge PENDING';
        progressBar.className = 'progress-bar';
        progressBar.style.width = '0%';
        logsConsole.textContent = 'Waiting for logs...';
        downloadContainer.classList.add('hidden');
    }

    function startPolling(taskId) {
        if (pollingInterval) clearInterval(pollingInterval);

        pollingInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/v1/status/${taskId}`);
                if (!response.ok) throw new Error('Failed to fetch status');

                const data = await response.json();
                updateUI(data);

                if (data.status === 'SUCCESS' || data.status === 'FAILED') {
                    clearInterval(pollingInterval);
                    buildBtn.disabled = false;
                }
            } catch (error) {
                console.error('Polling error:', error);
            }
        }, 2000);
    }

    function updateUI(data) {
        statusBadge.textContent = data.status;
        statusBadge.className = `badge ${data.status}`;

        if (data.logs) {
            logsConsole.textContent = data.logs;
            logsConsole.scrollTop = logsConsole.scrollHeight;
        }

        if (data.status === 'PROCESSING') {
            progressBar.classList.add('processing');
            progressBar.style.width = '50%';
        } else if (data.status === 'SUCCESS') {
            progressBar.className = 'progress-bar success';
            if (data.download_url) {
                downloadContainer.classList.remove('hidden');
                downloadLink.href = data.download_url;
            }
        } else if (data.status === 'FAILED') {
            progressBar.className = 'progress-bar failed';
        }
    }
});
