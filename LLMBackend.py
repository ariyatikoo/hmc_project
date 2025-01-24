import sys
from openai import OpenAI
import os
sys.path.append('/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project')
from DataAnalyzer import DataAnalyzer  

class LLMBackend(DataAnalyzer):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4"
    
    def __init__(self, summary=None):
        super().__init__()  # Ensure DataAnalyzer's constructor runs
        if summary is not None:
            self.summary = summary  # Override if provided

    def chat_with_gpt(self):
        
        # Validate summary content
        if not self.summary :
            print("Error: summary nonexistent.")
            return
        elif not isinstance(self.summary, str):
            print("Error: summary data is invalid.")
            return
        

        print("Hello!")
        

        # Start conversation
        conversation = [
            {
                "role": "system",
                "content": "You are an assistant for someone with type 1 diabetes. You will receive data analytics about the user's blood glucose and insulin delivery data. Your job is to explain the analytics to the user in a way that is easier for them to understand, and to answer their questions about it."
            },
            {
                "role": "user",
                "content": self.summary
            }
        ]

        print(self.summary)

        while True:
            user_input = input("User: ")  # User prompt
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            conversation.append({
                "role": "user",
                "content": f"Please rely on the information in the system message to answer the user's question about diabetes management and their insulin delivery and CGM data: {user_input}"
            })

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation
                )
                reply = response.choices[0].message.content
                print(f"ChatGPT: {reply}")
                conversation.append({"role": "assistant", "content": reply})
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    backend = LLMBackend()
    backend.chat_with_gpt()