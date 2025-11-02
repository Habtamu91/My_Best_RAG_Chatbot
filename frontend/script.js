// Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const pdfInput = document.getElementById('pdfInput');
const fileInfo = document.getElementById('fileInfo');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

// State
let uploadedFileName = null;
let isProcessing = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    pdfInput.addEventListener('change', handleFileSelect);
    uploadBtn.addEventListener('click', handleUpload);
    sendBtn.addEventListener('click', handleSendQuestion);
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isProcessing) {
            handleSendQuestion();
        }
    });
}

async function checkServerHealth() {
    try {
        const response = await fetch('http://localhost:8000/health');
        if (!response.ok) {
            showStatus('Server is not responding. Make sure the backend is running.', 'error');
        }
    } catch (error) {
        showStatus('Cannot connect to server. Make sure the backend is running on http://localhost:8000', 'error');
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        uploadedFileName = file.name;
        fileInfo.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
        fileInfo.classList.remove('hidden');
        uploadBtn.disabled = false;
        uploadStatus.textContent = '';
    }
}

async function handleUpload() {
    if (!pdfInput.files[0]) {
        showStatus('Please select a PDF file first.', 'error');
        return;
    }

    const file = pdfInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    showStatus('Uploading and processing PDF...', 'info');

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showStatus(
                `✓ PDF uploaded successfully! Processed ${data.chunks_count} chunks.`,
                'success'
            );
            
            // Enable chat
            questionInput.disabled = false;
            sendBtn.disabled = false;
            
            // Clear welcome message and show success
            clearWelcomeMessage();
            addMessage('ai', 'System', `PDF "${data.filename}" has been uploaded and processed. You can now ask questions about it!`);
            
            // Reset upload button
            uploadBtn.textContent = 'Upload PDF';
        } else {
            showStatus(`Error: ${data.detail || 'Failed to upload PDF'}`, 'error');
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload PDF';
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload PDF';
    }
}

async function handleSendQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) {
        return;
    }

    if (isProcessing) {
        return;
    }

    // Disable input and show loading
    isProcessing = true;
    questionInput.disabled = true;
    sendBtn.disabled = true;
    
    // Hide send text, show spinner
    document.querySelector('.send-text').classList.add('hidden');
    document.querySelector('.loading-spinner').classList.remove('hidden');

    // Add user message to chat
    addMessage('user', 'You', question);
    questionInput.value = '';

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok) {
            addMessage('ai', 'AI Assistant', data.answer);
            
            // Optionally show sources
            if (data.sources && data.sources.length > 0) {
                const sourcesText = `\n\n📚 Sources (${data.sources.length}):\n${data.sources.map((s, i) => `• ${s.text.substring(0, 100)}...`).join('\n')}`;
                // You can add this as a separate message or include in the main message
            }
        } else {
            addMessage('ai', 'Error', data.detail || 'Failed to get response');
        }
    } catch (error) {
        addMessage('ai', 'Error', `Connection error: ${error.message}. Make sure the backend server is running.`);
    } finally {
        // Re-enable input
        isProcessing = false;
        questionInput.disabled = false;
        sendBtn.disabled = false;
        
        // Show send text, hide spinner
        document.querySelector('.send-text').classList.remove('hidden');
        document.querySelector('.loading-spinner').classList.add('hidden');
        
        questionInput.focus();
    }
}

function addMessage(type, sender, content) {
    clearWelcomeMessage();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    messageDiv.innerHTML = `
        <div class="message-header">${sender}</div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function clearWelcomeMessage() {
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
}

function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status-message ${type}`;
    
    if (type === 'error' || type === 'success') {
        setTimeout(() => {
            uploadStatus.textContent = '';
            uploadStatus.className = 'status-message';
        }, 5000);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

