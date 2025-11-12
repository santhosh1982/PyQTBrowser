@echo off
echo ========================================
echo   AI Chat Assistant - Installation
echo ========================================
echo.
echo Installing AI provider libraries...
echo.

pip install openai
pip install google-generativeai
pip install anthropic

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python main.py
echo 2. Click the robot icon (🤖) or press Ctrl+Shift+A
echo 3. Click Settings (⚙️) to configure API keys
echo 4. Start chatting!
echo.
echo Get API keys from:
echo - OpenAI: https://platform.openai.com/api-keys
echo - Gemini: https://makersuite.google.com/app/apikey
echo - Claude: https://console.anthropic.com/
echo.
pause
