# 🤖 AI Chat Setup Guide

## Complete AI Integration with OpenAI, Gemini & Claude

Your browser now includes a **professional AI Chat Assistant** with support for three major AI providers!

---

## 🚀 Quick Start

### 1. Install Required Libraries

```bash
# Install all AI providers
pip install openai google-generativeai anthropic

# Or install individually:
pip install openai              # For OpenAI (GPT)
pip install google-generativeai # For Google Gemini
pip install anthropic           # For Anthropic Claude
```

### 2. Get API Keys

#### OpenAI (GPT-3.5/GPT-4)
1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy your key (starts with `sk-`)

#### Google Gemini
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API key"
4. Copy your key

#### Anthropic Claude
1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys section
4. Create new key
5. Copy your key

### 3. Configure in Browser

1. **Open browser**: `python main.py`
2. **Open AI Chat**: Click 🤖 or press `Ctrl+Shift+A`
3. **Open Settings**: Click ⚙️ button in AI panel header
4. **Enter API keys**: Paste your keys for each provider
5. **Select models**: Choose your preferred model for each provider
6. **Save**: Click "💾 Save Settings"

### 4. Start Chatting!

1. **Select provider**: Use dropdown in header (🔵 OpenAI, 🟢 Gemini, 🟣 Claude)
2. **Type message**: Enter your question
3. **Send**: Click "📤 Send Message"
4. **Get response**: AI responds using selected provider!

---

## 🎯 Features

### Multi-Provider Support
- ✅ **OpenAI** - GPT-3.5-turbo, GPT-4, GPT-4-turbo
- ✅ **Google Gemini** - Gemini-pro, Gemini-pro-vision
- ✅ **Anthropic Claude** - Claude-3-opus, Claude-3-sonnet, Claude-3-haiku

### Smart Features
- ✅ **Context awareness** - Remembers conversation history
- ✅ **Page summarization** - Analyzes current web page
- ✅ **Page explanation** - Detailed content breakdown
- ✅ **Free-form chat** - Ask anything
- ✅ **Provider switching** - Change AI on the fly
- ✅ **Secure storage** - API keys saved locally

### UI Features
- ✅ **Provider selector** - Dropdown in header
- ✅ **Settings dialog** - Easy configuration
- ✅ **Message bubbles** - Clean chat interface
- ✅ **Auto-scroll** - Always see latest message
- ✅ **Clear chat** - Start fresh anytime

---

## 📊 Provider Comparison

| Feature | OpenAI | Gemini | Claude |
|---------|--------|--------|--------|
| **Speed** | Fast | Very Fast | Fast |
| **Quality** | Excellent | Excellent | Excellent |
| **Context** | 4K-128K | 32K | 200K |
| **Cost** | $$ | $ | $$ |
| **Best For** | General | Fast responses | Long context |

### Model Recommendations:

#### OpenAI
- **gpt-3.5-turbo** - Fast, affordable, great for most tasks
- **gpt-4** - Highest quality, best reasoning
- **gpt-4-turbo-preview** - Faster GPT-4, larger context

#### Gemini
- **gemini-pro** - Fast, free tier available, good quality
- **gemini-pro-vision** - Supports images (future feature)

#### Claude
- **claude-3-haiku** - Fastest, most affordable
- **claude-3-sonnet** - Balanced speed and quality
- **claude-3-opus** - Highest quality, best for complex tasks

---

## 💡 Usage Examples

### Example 1: Page Summarization
```
1. Visit any article or webpage
2. Open AI Chat (🤖)
3. Click "📄 Summarize Page"
4. AI extracts content and provides summary
```

### Example 2: Page Explanation
```
1. Visit a technical or complex page
2. Open AI Chat
3. Click "💡 Explain"
4. AI breaks down the content
```

### Example 3: Free-Form Questions
```
You: What is quantum computing?
AI: Quantum computing is a type of computing that...

You: How does it differ from classical computing?
AI: The main differences are...
```

### Example 4: Context-Aware Conversation
```
You: Summarize this article
AI: [Provides summary]

You: What are the main points?
AI: [Lists key points from the article]

You: Can you explain the third point in more detail?
AI: [Explains with context from previous messages]
```

---

## ⚙️ Configuration

### API Key Storage
- **File**: `ai_config.json` (created automatically)
- **Location**: Same directory as `main.py`
- **Format**: JSON (human-readable)

### Configuration Structure:
```json
{
  "selected_provider": "openai",
  "api_keys": {
    "openai": "sk-...",
    "gemini": "...",
    "claude": "..."
  },
  "models": {
    "openai": "gpt-3.5-turbo",
    "gemini": "gemini-pro",
    "claude": "claude-3-sonnet-20240229"
  },
  "settings": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "stream": false
  }
}
```

### Settings Explained:
- **temperature** (0.0-1.0): Creativity level (higher = more creative)
- **max_tokens**: Maximum response length
- **stream**: Enable streaming responses (future feature)

---

## 🔒 Security & Privacy

### API Key Security:
- ✅ Stored locally only
- ✅ Never sent to browser servers
- ✅ Password-masked in UI
- ✅ Direct API communication

### Data Privacy:
- ✅ Conversations sent only to selected AI provider
- ✅ No third-party tracking
- ✅ Local conversation history
- ✅ Clear chat anytime

### Best Practices:
1. **Never share** your API keys
2. **Rotate keys** periodically
3. **Monitor usage** on provider dashboards
4. **Set spending limits** on provider accounts
5. **Clear chat** when done with sensitive topics

---

## 💰 Cost Management

### Free Tiers:
- **OpenAI**: $5 free credit for new accounts
- **Gemini**: Generous free tier (60 requests/minute)
- **Claude**: Limited free tier

### Cost Estimates (per 1000 messages):
- **GPT-3.5-turbo**: ~$0.50
- **GPT-4**: ~$15-30
- **Gemini-pro**: Free tier or ~$0.25
- **Claude-3-haiku**: ~$0.25
- **Claude-3-sonnet**: ~$3
- **Claude-3-opus**: ~$15

### Tips to Save Money:
1. Use **GPT-3.5** or **Gemini** for simple tasks
2. Use **Claude-haiku** for fast, cheap responses
3. Reserve **GPT-4** or **Claude-opus** for complex tasks
4. Clear conversation history to reduce context tokens
5. Set max_tokens limit in settings

---

## 🐛 Troubleshooting

### "AI providers not configured"
**Solution**: Install libraries
```bash
pip install openai google-generativeai anthropic
```

### "API key not configured"
**Solution**: 
1. Click ⚙️ Settings
2. Enter API key for your provider
3. Click Save

### "Error: Invalid API key"
**Solution**:
1. Verify key is correct
2. Check key hasn't expired
3. Ensure billing is set up on provider account

### "Error: Rate limit exceeded"
**Solution**:
1. Wait a few minutes
2. Switch to different provider
3. Upgrade provider plan

### "Could not extract page content"
**Solution**:
1. Ensure page has loaded completely
2. Try refreshing the page
3. Some pages block content extraction

### Provider not responding
**Solution**:
1. Check internet connection
2. Verify API key is valid
3. Check provider status page
4. Try different provider

---

## 🎓 Advanced Usage

### Custom System Prompts
Edit `ai_providers.py` to customize the system prompt:
```python
messages = [
    {"role": "system", "content": "Your custom instructions here"}
]
```

### Adjust Temperature
Lower temperature (0.3) = More focused, deterministic
Higher temperature (0.9) = More creative, varied

### Context Window Management
The chat keeps last 20 messages for context. Adjust in code:
```python
if len(self.conversation_messages) > 20:  # Change this number
    self.conversation_messages = self.conversation_messages[-20:]
```

### Add Custom Quick Actions
Add new buttons in `setup_ui()`:
```python
translate_btn = QPushButton("🌐 Translate")
translate_btn.clicked.connect(self.translate_page)
actions_layout.addWidget(translate_btn)
```

---

## 📚 API Documentation

### OpenAI
- Docs: https://platform.openai.com/docs
- Models: https://platform.openai.com/docs/models
- Pricing: https://openai.com/pricing

### Google Gemini
- Docs: https://ai.google.dev/docs
- Models: https://ai.google.dev/models/gemini
- Pricing: https://ai.google.dev/pricing

### Anthropic Claude
- Docs: https://docs.anthropic.com/
- Models: https://docs.anthropic.com/claude/docs/models-overview
- Pricing: https://www.anthropic.com/pricing

---

## 🎉 Summary

Your browser now has **enterprise-grade AI integration**:

✅ **3 AI providers** (OpenAI, Gemini, Claude)  
✅ **9+ models** to choose from  
✅ **Easy configuration** via settings dialog  
✅ **Context-aware** conversations  
✅ **Page analysis** (summarize & explain)  
✅ **Secure** local API key storage  
✅ **Professional UI** with provider switching  
✅ **Cost-effective** with free tier options  

**Start chatting with AI in your browser today!** 🚀

---

*Made with ❤️ - Your AI-Powered Browser* 🌐🤖✨
