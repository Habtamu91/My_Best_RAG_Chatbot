# PowerShell Test Script for RAG Chatbot
# This script tests if the backend is working without requiring Python requests

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "RAG Chatbot - Quick Test Script" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000"
$passed = 0
$failed = 0

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
Write-Host "-------------------" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get -TimeoutSec 5
    if ($response.status -eq "healthy") {
        Write-Host "✓ Status: $($response.status)" -ForegroundColor Green
        Write-Host "✓ Message: $($response.message)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "✗ Unexpected response: $response" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "✗ Failed: Cannot connect to server" -ForegroundColor Red
    Write-Host "  Make sure the backend is running on port 8000" -ForegroundColor Yellow
    Write-Host "  Start it with: cd backend; python run.py" -ForegroundColor Yellow
    $failed++
}

Write-Host ""

# Test 2: Check Upload Endpoint
Write-Host "Test 2: Upload Endpoint Check" -ForegroundColor Yellow
Write-Host "----------------------------" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/upload" -Method Options -TimeoutSec 5
    Write-Host "✓ Upload endpoint accessible (Status: $($response.StatusCode))" -ForegroundColor Green
    $passed++
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 405 -or $statusCode -eq 200) {
        Write-Host "✓ Upload endpoint accessible (Status: $statusCode)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""

# Test 3: Check Chat Endpoint
Write-Host "Test 3: Chat Endpoint Check" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Yellow
try {
    $body = @{
        question = "What is this document about?"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/api/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 5
    Write-Host "✓ Chat endpoint accessible" -ForegroundColor Green
    Write-Host "  Response: $($response.answer.Substring(0, [Math]::Min(80, $response.answer.Length)))..." -ForegroundColor Gray
    $passed++
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 400) {
        Write-Host "✓ Chat endpoint accessible (Expected: No documents uploaded yet)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
        if ($statusCode -eq 500) {
            Write-Host "  This might be normal if no documents are uploaded" -ForegroundColor Yellow
        }
        $failed++
    }
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($failed -eq 0) {
    Write-Host "🎉 All tests passed! The chatbot backend is working correctly." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Open the frontend: frontend\index.html" -ForegroundColor White
    Write-Host "2. Upload a PDF document" -ForegroundColor White
    Write-Host "3. Ask questions about the document" -ForegroundColor White
} else {
    Write-Host "⚠️  Some tests failed. Check the errors above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Cyan
    Write-Host "- Make sure the backend is running: cd backend; python run.py" -ForegroundColor White
    Write-Host "- Check if port 8000 is available" -ForegroundColor White
    Write-Host "- Verify all dependencies are installed" -ForegroundColor White
}

