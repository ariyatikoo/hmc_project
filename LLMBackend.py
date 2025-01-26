import sys
from openai import OpenAI
import os
sys.path.append('/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project')
from DataAnalyzer import DataAnalyzer  

class LLMBackend(DataAnalyzer):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4"
    
    def __init__(self, specific_date='2024-11-10', time_frame='1 day'):
        super().__init__()
        data_analyzer = DataAnalyzer()
        self.summary = data_analyzer.Summary(specific_date, time_frame)

    def chat_with_gpt(self):

        # Validate summary content
        if not self.summary:
            print("Error: Summary nonexistent.")
            return
        elif not isinstance(self.summary, str):
            print("Error: Summary data is invalid.")
            return
        
        # system message is now updated to include the summary and is condensed 
        conversation = [
            {
                "role": "system",
                "content": (
                    "You are an assistant for someone with type 1 diabetes. "
                    "You will receive data analytics about the user's blood glucose and insulin delivery data. "
                    "Your job is to explain the analytics to the user in a way that is easier for them to understand, "
                    "and to answer their questions about it. Here is the user's data:\n\n" + self.summary
                )
            }
        ]

        print("Summary provided to the chatbot:\n", self.summary)
        print("\nHello! How may I assist you?")

        # Chat loop
        while True:
            user_input = input("User: ")  # User prompt
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            conversation.append({"role": "user", "content": user_input})

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation
                )
                reply = response.choices[0].message.content
                print(f"Cassie: {reply}")
                conversation.append({"role": "assistant", "content": reply})
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    backend = LLMBackend()
    backend.chat_with_gpt()