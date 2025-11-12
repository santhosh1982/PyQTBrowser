"""
AI Provider integrations for OpenAI, Gemini, and Claude
"""
import os
import json


class AIProviderManager:
    """Manages API keys and provider selection"""
    
    def __init__(self):
        self.config_file = 'ai_config.json'
        self.config = self.load_config()
    
    def load_config(self):
        """Load AI configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'selected_provider': 'openai',
            'api_keys': {
                'openai': '',
                'gemini': '',
                'claude': ''
            },
            'models': {
                'openai': 'gpt-3.5-turbo',
                'gemini': 'gemini-pro',
                'claude': 'claude-3-sonnet-20240229'
            },
            'settings': {
                'temperature': 0.7,
                'max_tokens': 2000,
                'stream': False
            }
        }
    
    def save_config(self):
        """Save AI configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_api_key(self, provider):
        """Get API key for provider"""
        return self.config['api_keys'].get(provider, '')
    
    def set_api_key(self, provider, key):
        """Set API key for provider"""
        self.config['api_keys'][provider] = key
        self.save_config()
    
    def get_selected_provider(self):
        """Get currently selected provider"""
        return self.config.get('selected_provider', 'openai')
    
    def set_selected_provider(self, provider):
        """Set selected provider"""
        self.config['selected_provider'] = provider
        self.save_config()
    
    def get_model(self, provider):
        """Get model for provider"""
        return self.config['models'].get(provider, '')
    
    def set_model(self, provider, model):
        """Set model for provider"""
        self.config['models'][provider] = model
        self.save_config()


class OpenAIProvider:
    """OpenAI API integration"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.available = self.check_availability()
    
    def check_availability(self):
        """Check if OpenAI is available"""
        try:
            import openai
            return True
        except ImportError:
            return False
    
    def generate_response(self, messages, model='gpt-3.5-turbo', temperature=0.7, max_tokens=2000):
        """Generate response using OpenAI"""
        if not self.available:
            return "Error: OpenAI library not installed. Run: pip install openai"
        
        if not self.api_key:
            return "Error: OpenAI API key not configured. Please set your API key in settings."
        
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"


class GeminiProvider:
    """Google Gemini API integration"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.available = self.check_availability()
    
    def check_availability(self):
        """Check if Gemini is available"""
        try:
            import google.generativeai as genai
            return True
        except ImportError:
            return False
    
    def generate_response(self, messages, model='gemini-pro', temperature=0.7, max_tokens=2000):
        """Generate response using Gemini"""
        if not self.available:
            return "Error: Gemini library not installed. Run: pip install google-generativeai"
        
        if not self.api_key:
            return "Error: Gemini API key not configured. Please set your API key in settings."
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            model_instance = genai.GenerativeModel(model)
            
            # Convert messages to Gemini format
            prompt = self._convert_messages_to_prompt(messages)
            
            response = model_instance.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
    
    def _convert_messages_to_prompt(self, messages):
        """Convert OpenAI-style messages to Gemini prompt"""
        prompt_parts = []
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == 'system':
                prompt_parts.append(f"System: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")
        return "\n\n".join(prompt_parts)


class ClaudeProvider:
    """Anthropic Claude API integration"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.available = self.check_availability()
    
    def check_availability(self):
        """Check if Claude is available"""
        try:
            import anthropic
            return True
        except ImportError:
            return False
    
    def generate_response(self, messages, model='claude-3-sonnet-20240229', temperature=0.7, max_tokens=2000):
        """Generate response using Claude"""
        if not self.available:
            return "Error: Anthropic library not installed. Run: pip install anthropic"
        
        if not self.api_key:
            return "Error: Claude API key not configured. Please set your API key in settings."
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Extract system message if present
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_message = msg['content']
                else:
                    user_messages.append(msg)
            
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message if system_message else None,
                messages=user_messages
            )
            
            return response.content[0].text
        except Exception as e:
            return f"Claude Error: {str(e)}"
