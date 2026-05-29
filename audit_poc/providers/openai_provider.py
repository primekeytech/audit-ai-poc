# ============================================
# AUDIT POC - OpenAI Provider (Future Use)
# ============================================
# This file handles OpenAI API integration.
# NOT used in Phase 1 - kept for future use.
#
# To enable:
# 1. Add API key to config.yaml
# 2. Change provider to "openai" in config.yaml
# ============================================

from core.ai_provider import AIProvider

class OpenAIProvider(AIProvider):
    """
    OpenAI API provider.
    Future use - not active in Phase 1.
    """
    
    def __init__(self, config: dict):
        """
        Initialise OpenAI provider.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        
        try:
            # Import OpenAI library
            from openai import OpenAI
            
            # Get API key from config
            api_key = config["openai"]["api_key"]
            
            # Check if API key is set
            if not api_key:
                raise ValueError(
                    "OpenAI API key not set in config.yaml! "
                    "Add your key under openai.api_key"
                )
            
            # Initialise OpenAI client
            self.client = OpenAI(api_key=api_key)
            self.model = config["openai"]["model"]
            self.temperature = config["ai"]["temperature"]
            self.max_tokens = config["ai"]["max_tokens"]
            
            print(f"OpenAI provider ready - model: {self.model}")
            
        except ImportError:
            raise ImportError(
                "OpenAI library not installed! "
                "Run: pip install openai"
            )
    
    
    def analyze(self, prompt: str) -> str:
        """
        Send prompt to OpenAI API and get response.
        
        Args:
            prompt: The question/instruction for the AI
            
        Returns:
            str: The AI's response text
        """
        
        try:
            # Send to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert IT auditor 
                        specialising in bank IT audits. You analyse 
                        documents carefully and provide accurate, 
                        professional assessments."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract and return response text
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"OpenAI error: {str(e)}"
            print(error_msg)
            return f"ERROR: {error_msg}"
    
    
    def is_available(self) -> bool:
        """
        Check if OpenAI API is accessible.
        
        Returns:
            bool: True if available, False if not
        """
        
        try:
            # Simple test call to check connectivity
            self.client.models.list()
            return True
        except Exception as e:
            print(f"OpenAI not available: {str(e)}")
            return False
