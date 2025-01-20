from openai import OpenAI
import os
from hmc_project.DataAnalyzer import DataAnalyzer  # type: ignore

class LLMBackend(DataAnalyzer):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"
        self.data_analyzer = DataAnalyzer()

    def chat_with_gpt(self):
        print("Hello!")
        

        summary = self.data_analyzer.Summary(
            '2024-11-18',
            self.data_analyzer.BGmean,
            self.data_analyzer.BGmedian,
            self.data_analyzer.bg_TIR,
            self.data_analyzer.percent_high,
            self.data_analyzer.percent_low,
            self.data_analyzer.calcedNighttimeBasal,
            self.data_analyzer.morningSpike,
            self.data_analyzer.carbRatioAdjustments
        )

        # Start conversation
        conversation = [
            {
                "role": "system",
                "content": "You are an assistant for someone with type 1 diabetes. You will receive data analytics about the user's blood glucose and insulin delivery data. Your job is to explain the analytics to the user in a way that is easier for them to understand, and to answer their questions about it."
            },
            {
                "role": "user",
                "content": summary
            }
        ]

        while True:
            user_input = input("User: ")  # User prompt
            if user_input.lower() == "exit":
                print("Goodbye")
                break

            conversation.append({
                "role": "user",
                "content": f"Please rely on the information in the system message to answer the user's question about diabetes management and their insulin delivery and CGM data: {user_input}"
            })

            try:
                response = self.client.ChatCompletion.create(
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
