# Script to help fix API key in .env file
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OpenAI API Key Fixer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$envPath = "C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\.env"

if (Test-Path $envPath) {
    Write-Host "Current .env file found" -ForegroundColor Green
    Write-Host ""
    
    # Show current key (masked)
    $content = Get-Content $envPath
    $apiKeyLine = $content | Select-String "OPENAI_API_KEY"
    if ($apiKeyLine) {
        Write-Host "Current API Key line found:" -ForegroundColor Yellow
        Write-Host "  $apiKeyLine" -ForegroundColor Gray
        Write-Host ""
    }
    
    Write-Host "To fix the API key error:" -ForegroundColor Yellow
    Write-Host "1. Get a NEW API key from: https://platform.openai.com/api-keys" -ForegroundColor White
    Write-Host "2. Open .env file to edit: notepad $envPath" -ForegroundColor White
    Write-Host "3. Replace the OPENAI_API_KEY value with your new key" -ForegroundColor White
    Write-Host "4. Save and restart the backend server" -ForegroundColor White
    Write-Host ""
    
    $edit = Read-Host "Would you like to open .env file now? (y/n)"
    if ($edit -eq "y" -or $edit -eq "Y") {
        notepad $envPath
        Write-Host ""
        Write-Host "After saving the file, RESTART the backend server!" -ForegroundColor Yellow
    }
} else {
    Write-Host ".env file not found at: $envPath" -ForegroundColor Red
    Write-Host "Creating template .env file..." -ForegroundColor Yellow
    
    @"
# OpenAI API Configuration
OPENAI_API_KEY=your_new_api_key_here
USE_OPENAI=true

# Model Settings
LLM_MODEL=gpt-3.5-turbo

# Chunking Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval Settings
TOP_K_RESULTS=3

# Vector Store Settings
VECTOR_STORE_TYPE=chroma

# Server Settings
HOST=0.0.0.0
PORT=8000
"@ | Out-File -FilePath $envPath -Encoding utf8
    
    Write-Host ".env file created! Now edit it and add your API key." -ForegroundColor Green
    notepad $envPath
}

Write-Host ""
Write-Host "Don't forget to RESTART the backend after updating!" -ForegroundColor Yellow
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

