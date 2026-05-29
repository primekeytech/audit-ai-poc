# ============================================
# AUDIT POC - AI Provider Abstraction Layer
# ============================================
# This file creates a flexible AI system that
# can switch between different AI providers:
# - Ollama (local - default for Phase 1)
# - OpenAI (future)
# - Anthropic Claude (future)
#
# To switch providers - just change config.yaml
# No code changes needed!
# ============================================

import yaml
from abc import ABC, abstractmethod

# ============================================
# BASE CLASS - ALL PROVIDERS INHERIT FROM THIS
# ============================================

class AIProvider(ABC):
    """
    Abstract base class for all AI providers.
    Every provider MUST implement the 'analyze' method.
    This ensures all providers work the same way.
    """
    
    @abstractmethod
    def analyze(self, prompt: str) -> str:
        """
        Send a prompt to the AI and get a response.
        
        Args:
            prompt: The question/instruction for the AI
            
        Returns:
            str: The AI's response
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this AI provider is available and running.
        
        Returns:
            bool: True if available, False if not
        """
        pass


# ============================================
# PROVIDER FACTORY - CREATES CORRECT PROVIDER
# ============================================

def get_ai_provider(config: dict) -> AIProvider:
    """
    Factory function - reads config and returns
    the correct AI provider instance.
    
    Args:
        config: Configuration dictionary from config.yaml
        
    Returns:
        AIProvider: The correct provider instance
        
    Example:
        config = {"ai": {"provider": "ollama"}}
        provider = get_ai_provider(config)
        response = provider.analyze("What is this document about?")
    """
    
    # Get provider name from config
    provider_name = config["ai"]["provider"].lower()
    
    print(f"Initialising AI provider: {provider_name}")
    
    # Return the correct provider based on config
    if provider_name == "ollama":
        # Local Ollama provider - Phase 1 default
        from providers.ollama_provider import OllamaProvider
        return OllamaProvider(config)
    
    elif provider_name == "openai":
        # OpenAI provider - future use
        from providers.openai_provider import OpenAIProvider
        return OpenAIProvider(config)
    
    elif provider_name == "anthropic":
        # Anthropic Claude provider - future use
        from providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider(config)
    
    else:
        # Unknown provider - raise helpful error
        raise ValueError(
            f"Unknown AI provider: '{provider_name}'. "
            f"Valid options are: 'ollama', 'openai', 'anthropic'"
        )


# ============================================
# AUDIT-SPECIFIC AI FUNCTIONS
# ============================================

class AuditAI:
    """
    High-level audit AI functions.
    Uses the provider abstraction layer underneath.
    This is what the rest of the app uses directly.
    """
    
    def __init__(self, config: dict):
        """
        Initialise AuditAI with the configured provider.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        # Get the correct AI provider based on config
        self.provider = get_ai_provider(config)
        self.config = config
        
        print(f"AuditAI ready with provider: {config['ai']['provider']}")
    
    
    def analyse_control(self, control_question: str, extracted_text: str) -> dict:
        """
        Analyses a single audit control against extracted documents.
        This is the CORE function of the entire system.
        
        Args:
            control_question: The audit control being tested
                Example: "Determine if a security exception policy exists"
            extracted_text: All text extracted from bank documents
            
        Returns:
            dict: {
                "score": 1-4,
                "notes": "AI explanation",
                "artifact": "Document reference",
                "confidence": "high/medium/low"
            }
        """
        
        # Build the prompt for the AI
        # This tells the AI exactly what to do and how to respond
        prompt = f"""
You are an expert IT auditor analysing bank audit documents.

AUDIT CONTROL TO TEST:
{control_question}

BANK DOCUMENTS PROVIDED:
{extracted_text[:3000]}

SCORING CRITERIA:
Score 1 = Control fully satisfied. Document found and meets requirements.
Score 2 = Control partially satisfied. Document found but has minor gaps.
Score 3 = Cannot determine. Need more information or clarification.
Score 4 = Control NOT satisfied. Document missing or non-compliant. THIS IS A FINDING.

YOUR TASK:
1. Read the bank documents carefully
2. Determine if this control is satisfied
3. Assign a score from 1 to 4
4. Explain your reasoning clearly
5. Reference the specific document you used

RESPOND IN EXACTLY THIS FORMAT:
SCORE: [1, 2, 3, or 4]
ARTIFACT: [Document name or "Not provided"]
NOTES: [Your explanation in 1-2 sentences]
CONFIDENCE: [high, medium, or low]

IMPORTANT:
- Be conservative - if unsure, score 3 not 1
- Always reference which document supports your score
- Keep notes concise and professional
- Do not make assumptions - only score based on evidence provided
"""
        
        # Send prompt to AI provider
        response = self.provider.analyze(prompt)
        
        # Parse the AI response into structured data
        result = self._parse_control_response(response)
        
        return result
    
    
    def analyse_questionnaire(self, question: str, answer: str, extracted_text: str) -> dict:
        """
        Analyses a questionnaire response against documents.
        Cross-references what the bank SAID against what they UPLOADED.
        
        Args:
            question: The questionnaire question
            answer: What the bank answered
            extracted_text: All extracted document text
            
        Returns:
            dict: Analysis result with score and notes
        """
        
        # Build prompt to cross-reference questionnaire vs documents
        prompt = f"""
You are an expert IT auditor cross-referencing questionnaire responses
against actual bank documents.

QUESTIONNAIRE QUESTION:
{question}

BANK'S ANSWER:
{answer}

SUPPORTING DOCUMENTS:
{extracted_text[:2000]}

YOUR TASK:
Verify if the bank's answer is supported by the documents provided.

RESPOND IN EXACTLY THIS FORMAT:
SCORE: [1, 2, 3, or 4]
ARTIFACT: [Document that supports or contradicts the answer]
NOTES: [Brief explanation - use "Reportedly" if self-reported only]
CONFIDENCE: [high, medium, or low]
"""
        
        # Send to AI and parse response
        response = self.provider.analyze(prompt)
        return self._parse_control_response(response)
    
    
    def generate_finding(self, control_name: str, notes: str) -> dict:
        """
        Auto-generates a professional finding for score 4 controls.
        
        Args:
            control_name: Name of the failed control
            notes: AI notes from the analysis
            
        Returns:
            dict: {
                "header": "Finding title",
                "risk_description": "What the risk is",
                "recommendation": "What to do about it"
            }
        """
        
        prompt = f"""
You are writing a professional IT audit finding for a bank audit report.

FAILED CONTROL:
{control_name}

ANALYSIS NOTES:
{notes}

Write a professional audit finding with exactly these sections:

HEADER: [Short finding title - max 6 words]
RISK_DESCRIPTION: [1-2 sentences explaining the risk to the bank]
RECOMMENDATION: [1-2 sentences on what the bank should do to fix this]

Keep language professional, clear and actionable.
Reference FFIEC guidance where appropriate.
"""
        
        response = self.provider.analyze(prompt)
        return self._parse_finding_response(response)
    
    
    def _parse_control_response(self, response: str) -> dict:
        """
        Parses AI response text into a structured dictionary.
        
        Args:
            response: Raw AI response text
            
        Returns:
            dict: Structured result with score, notes, artifact, confidence
        """
        
        # Default values in case parsing fails
        result = {
            "score": 3,           # Default to 3 (needs review) if unsure
            "artifact": "Review required",
            "notes": response,    # Store full response as notes if parsing fails
            "confidence": "low"
        }
        
        try:
            # Split response into lines
            lines = response.strip().split('\n')
            
            # Parse each line
            for line in lines:
                line = line.strip()
                
                # Extract score
                if line.startswith("SCORE:"):
                    score_text = line.replace("SCORE:", "").strip()
                    # Extract just the number
                    score_num = ''.join(filter(str.isdigit, score_text))
                    if score_num in ['1', '2', '3', '4']:
                        result["score"] = int(score_num)
                
                # Extract artifact
                elif line.startswith("ARTIFACT:"):
                    result["artifact"] = line.replace("ARTIFACT:", "").strip()
                
                # Extract notes
                elif line.startswith("NOTES:"):
                    result["notes"] = line.replace("NOTES:", "").strip()
                
                # Extract confidence
                elif line.startswith("CONFIDENCE:"):
                    confidence = line.replace("CONFIDENCE:", "").strip().lower()
                    if confidence in ["high", "medium", "low"]:
                        result["confidence"] = confidence
        
        except Exception as e:
            # If parsing fails completely - return defaults
            print(f"Warning: Could not parse AI response: {str(e)}")
        
        return result
    
    
    def _parse_finding_response(self, response: str) -> dict:
        """
        Parses AI finding response into structured dictionary.
        
        Args:
            response: Raw AI response text
            
        Returns:
            dict: Finding with header, risk_description, recommendation
        """
        
        # Default values
        result = {
            "header": "Finding requires review",
            "risk_description": response,
            "recommendation": "Please review and update manually"
        }
        
        try:
            lines = response.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("HEADER:"):
                    result["header"] = line.replace("HEADER:", "").strip()
                
                elif line.startswith("RISK_DESCRIPTION:"):
                    result["risk_description"] = line.replace("RISK_DESCRIPTION:", "").strip()
                
                elif line.startswith("RECOMMENDATION:"):
                    result["recommendation"] = line.replace("RECOMMENDATION:", "").strip()
        
        except Exception as e:
            print(f"Warning: Could not parse finding response: {str(e)}")
        
        return result
