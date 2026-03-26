import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')


    def generate(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return "AI is temporarily unavailable. Try again later."
