import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and self.api_key != "your_google_genai_api_key_here":
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[LLMService] Could not initialize Gemini client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        if self.client:
            try:
                # Use gemini-2.5-flash (or gemini-1.5-flash)
                model_name = "gemini-2.5-flash"
                contents = prompt
                if system_instruction:
                    contents = f"System Instructions: {system_instruction}\n\nUser: {prompt}"

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=contents,
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[LLMService] Gemini API call failed: {e}. Falling back to rule-based response.")

        return self._offline_fallback(prompt, system_instruction)

    def _offline_fallback(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        prompt_lower = prompt.lower()
        if "scam" in prompt_lower or "fake" in prompt_lower or "fraud" in prompt_lower:
            return (
                "🛡️ **Scam & Fraud Analysis**\n\n"
                "• **Key Safety Rule:** Legitimate banks, RBI-registered NBFCs, and government portals **never** demand upfront processing fees or asking for your OTP / UPI PIN.\n"
                "• **Immediate Action:** Do not click suspicious links or pay any advance deposit. Block the sender and verify credentials at **cybercrime.gov.in** (Helpline: **1930**)."
            )
        if "scheme" in prompt_lower:
            return (
                "🏛️ **Government Welfare Guidance**\n\n"
                "Based on your profile, you are eligible for key Indian social security schemes including **e-Shram**, **PM SVANidhi**, and **Atal Pension Yojana**."
            )
        
        # Financial coaching offline fallback
        return (
            "💡 **Smart Financial Action Plan**\n\n"
            "• **1. Daily / Weekly Savings:** Save ₹100 – ₹200 daily into a separate liquid bank account or recurring deposit.\n"
            "• **2. Build an Emergency Buffer:** Target ₹15,000 to cover 1 month of living and fuel/maintenance expenses.\n"
            "• **3. Avoid Trap Loans:** Never borrow from unverified instant 7-day mobile loan apps with predatory interest rates."
        )


llm_client = LLMService()

