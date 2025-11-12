# 🎯 Context Menu AI Integration Guide

## Overview
Your browser now features **intelligent context menu integration** that lets you send selected text directly to AI for analysis!

---

## ✨ Features

### 🤖 AI Actions Menu
Right-click on any selected text to access AI-powered actions:

- **💡 Explain this** - Get detailed explanations
- **📄 Summarize this** - Quick summaries
- **🌐 Translate this** - Translate to/from English
- **📝 Simplify this** - Simplify complex text
- **📖 Define terms** - Define key terms
- **💬 Ask about this...** - Custom questions

### 🎯 Smart Features
- ✅ **Auto-open AI panel** - Opens automatically when needed
- ✅ **Selection indicator** - Shows 📌 for context-based queries
- ✅ **Instant processing** - No copy-paste needed
- ✅ **Context preservation** - Maintains conversation flow
- ✅ **Multi-provider support** - Works with OpenAI, Gemini, Claude

---

## 🚀 How to Use

### Basic Usage

#### 1. Select Text
- Highlight any text on a webpage
- Can be a word, sentence, paragraph, or multiple paragraphs

#### 2. Right-Click
- Right-click on the selected text
- Context menu appears

#### 3. Choose AI Action
- Click "🤖 Ask AI" to see options
- Select your desired action

#### 4. Get AI Response
- AI panel opens automatically (if closed)
- Your query appears with 📌 indicator
- AI processes and responds instantly

---

## 💡 Use Cases

### 1. Learning & Research

**Scenario**: Reading a technical article
```
1. Select: "Quantum entanglement is a phenomenon..."
2. Right-click → Ask AI → Explain this
3. AI: Provides detailed explanation
```

**Scenario**: Complex terminology
```
1. Select: "Blockchain consensus mechanisms"
2. Right-click → Ask AI → Define terms
3. AI: Explains each term clearly
```

### 2. Language Learning

**Scenario**: Foreign language text
```
1. Select: "Bonjour, comment allez-vous?"
2. Right-click → Ask AI → Translate this
3. AI: "Hello, how are you?"
```

**Scenario**: Simplifying academic text
```
1. Select: Complex academic paragraph
2. Right-click → Ask AI → Simplify this
3. AI: Provides simple explanation
```

### 3. Content Analysis

**Scenario**: Long article
```
1. Select: Multiple paragraphs
2. Right-click → Ask AI → Summarize this
3. AI: Provides concise summary
```

**Scenario**: News analysis
```
1. Select: News article excerpt
2. Right-click → Ask AI → Explain this
3. AI: Provides context and analysis
```

### 4. Quick Reference

**Scenario**: Technical documentation
```
1. Select: Code snippet or technical term
2. Right-click → Ask AI → Explain this
3. AI: Breaks down the concept
```

**Scenario**: Historical context
```
1. Select: Historical event mention
2. Right-click → Ask AI → Ask about this
3. AI: Provides historical context
```

---

## 🎨 Visual Indicators

### Selection Indicator (📌)
Messages sent from context menu show a pin icon:
```
📌 You: Please explain the following text...
```

This helps you distinguish between:
- **Regular messages** - Typed manually
- **Context messages** - Sent from text selection

### Menu Styling
- **Blue border** - Matches browser theme
- **Rounded corners** - Modern design
- **Hover effects** - Clear visual feedback
- **Organized sections** - AI actions grouped together

---

## ⚙️ Configuration

### AI Provider Selection
The context menu uses your currently selected AI provider:
1. Open AI panel (🤖)
2. Select provider from dropdown (🔵 OpenAI, 🟢 Gemini, 🟣 Claude)
3. Context menu actions use selected provider

### Customizing Actions
Edit `main.py` to add custom actions:

```python
# In BrowserTab.build_context_menu()
custom_action = ai_menu.addAction("🎯 Your Custom Action")
custom_action.triggered.connect(
    lambda: self.send_to_ai("custom", selected_text)
)

# In BrowserTab.send_to_ai()
prompts = {
    # ... existing prompts ...
    "custom": f"Your custom prompt: {text}"
}
```

---

## 🎯 Action Details

### 💡 Explain This
**Purpose**: Get detailed explanations  
**Best for**: Complex concepts, technical terms, unfamiliar topics  
**Prompt**: "Please explain the following text in detail:"

**Example**:
```
Selected: "Machine learning algorithms"
AI Response: Detailed explanation of ML algorithms, types, and applications
```

### 📄 Summarize This
**Purpose**: Quick summaries  
**Best for**: Long paragraphs, articles, documentation  
**Prompt**: "Please provide a concise summary of:"

**Example**:
```
Selected: 5 paragraphs about climate change
AI Response: 2-3 sentence summary of key points
```

### 🌐 Translate This
**Purpose**: Language translation  
**Best for**: Foreign language text, multilingual content  
**Prompt**: "Please translate... to English (or Spanish if already English)"

**Example**:
```
Selected: "Hola, ¿cómo estás?"
AI Response: "Hello, how are you?"
```

### 📝 Simplify This
**Purpose**: Simplify complex text  
**Best for**: Academic papers, legal text, technical jargon  
**Prompt**: "Please simplify and explain in simple terms:"

**Example**:
```
Selected: Complex legal clause
AI Response: Plain English explanation
```

### 📖 Define Terms
**Purpose**: Define key terms  
**Best for**: Technical vocabulary, acronyms, specialized terms  
**Prompt**: "Please define and explain the key terms in:"

**Example**:
```
Selected: "API, REST, JSON"
AI Response: Definitions of each term with examples
```

### 💬 Ask About This
**Purpose**: Custom questions  
**Best for**: Specific queries, follow-up questions  
**Prompt**: Uses selected text as context

**Example**:
```
Selected: Historical event description
AI Response: Provides context and additional information
```

---

## 🔄 Workflow Examples

### Research Workflow
```
1. Visit Wikipedia article
2. Select interesting paragraph
3. Right-click → Explain this
4. Read AI explanation
5. Select another section
6. Right-click → Summarize this
7. Continue research with AI assistance
```

### Learning Workflow
```
1. Read tutorial or documentation
2. Select confusing section
3. Right-click → Simplify this
4. Understand concept
5. Select technical terms
6. Right-click → Define terms
7. Build comprehensive understanding
```

### Translation Workflow
```
1. Visit foreign language site
2. Select text to translate
3. Right-click → Translate this
4. Read translation
5. Continue with more selections
6. Build vocabulary understanding
```

---

## 🎨 Advanced Features

### Context Preservation
The AI maintains conversation context:
```
1st Query: "Explain quantum computing"
AI: [Explanation]

2nd Query: "How does it differ from classical?"
AI: [Compares with previous context]
```

### Multi-Selection Support
Select and query multiple times:
```
1. Select paragraph 1 → Summarize
2. Select paragraph 2 → Summarize
3. Ask: "Compare these two summaries"
4. AI: [Provides comparison]
```

### Provider Switching
Switch providers mid-conversation:
```
1. Use OpenAI for explanation
2. Switch to Claude for detailed analysis
3. Switch to Gemini for quick summary
```

---

## 🔧 Troubleshooting

### Context Menu Not Appearing
**Solution**:
- Ensure text is selected
- Right-click directly on selected text
- Try selecting again

### AI Panel Not Opening
**Solution**:
- Check if AI panel is already open
- Try clicking 🤖 button manually
- Restart browser if needed

### No AI Response
**Solution**:
- Verify API key is configured (⚙️ Settings)
- Check internet connection
- Ensure AI provider is selected
- Check provider status

### Selection Not Captured
**Solution**:
- Select text more carefully
- Avoid selecting across multiple elements
- Try smaller selections

---

## 💡 Pro Tips

### 1. Quick Definitions
Select single words for instant definitions:
```
Select: "Algorithm"
Right-click → Define terms
```

### 2. Paragraph Analysis
Select full paragraphs for comprehensive analysis:
```
Select: Entire paragraph
Right-click → Explain this
```

### 3. Comparative Analysis
Use multiple selections to compare:
```
1. Select text A → Summarize
2. Select text B → Summarize
3. Ask: "What are the differences?"
```

### 4. Language Practice
Use translate for language learning:
```
Select foreign text → Translate
Then ask follow-up questions about grammar
```

### 5. Research Assistance
Build knowledge progressively:
```
1. Explain concept
2. Define terms
3. Simplify explanation
4. Ask follow-up questions
```

---

## 📊 Comparison with Manual Method

### Traditional Method:
1. Select text
2. Copy (Ctrl+C)
3. Open AI panel
4. Type prompt
5. Paste text
6. Send

**Time**: ~30 seconds

### Context Menu Method:
1. Select text
2. Right-click → Choose action

**Time**: ~3 seconds

**10x faster!** ⚡

---

## 🎉 Benefits

### Productivity
- ⚡ **10x faster** than manual copy-paste
- 🎯 **One-click actions** for common tasks
- 🔄 **Seamless workflow** integration
- 💡 **Instant insights** from any text

### User Experience
- 🎨 **Beautiful UI** matching browser theme
- 📌 **Clear indicators** for context queries
- 🤖 **Smart automation** (auto-open panel)
- 🎯 **Intuitive actions** with clear labels

### Flexibility
- 🔧 **Customizable** actions
- 🌐 **Multi-provider** support
- 💬 **Context-aware** conversations
- 📚 **Unlimited** selections

---

## 🚀 Summary

Your browser now features **intelligent context menu AI integration**:

✅ **6 AI actions** (Explain, Summarize, Translate, Simplify, Define, Ask)  
✅ **Right-click** on any selected text  
✅ **Auto-open** AI panel  
✅ **Selection indicator** (📌)  
✅ **Context preservation**  
✅ **Multi-provider** support  
✅ **10x faster** than manual method  
✅ **Beautiful UI** with hover effects  

**Transform your browsing with AI-powered text analysis!** 🎯✨

---

*Context Menu AI - Intelligence at your fingertips!* 🌐🤖
