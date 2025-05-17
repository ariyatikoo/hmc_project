import sys
from openai import OpenAI
import json
import os
sys.path.append('/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project')
from DataAnalyzer import DataAnalyzer  

class LLMBackend(DataAnalyzer): # Summary data inherited from DataAnalyzer so LLM has access to statistics generated

    # ChatGPT 4.0 API
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4"
    
    def __init__(self, user_id, specific_date='2025-01-01', time_frame='1 day'):
        super().__init__()
        self.user_id = user_id
        data_analyzer = DataAnalyzer()
        self.summary = data_analyzer.Summary(specific_date, time_frame)

    def chat_with_gpt(self): # user history log for recommendations and added personalization
        user_name = input("What's your user name? ")
        file_path = f"/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/DiabetesLogDirectory"
        file_name = f"{user_name}.jsonl"
        
        if not self.summary:
            print("Error: Summary nonexistent.")
            return
        elif not isinstance(self.summary, str):
            print("Error: Summary data is invalid.")
            return
        
       

        

        conversation = []

        if (file_name not in os.listdir(file_path)):
            conversation = [
                { # prompt engineering --> tailored prompt created, shown below
                    "role": "system",
                    "content": (
                        "You are an assistant for someone with type 1 diabetes. "
                        "You will receive data analytics about the user's blood glucose and insulin delivery data. "
                        "Your job is to explain the analytics to the user in a way that is easier for them to understand, "
                        "and to answer their questions about it." 
                        "You must provide a disclaimer to the user" 
                        "and encourage them to consider these changes before executing them and/or consult a medical professional."
                        "You must make sure to complete user requests to the best of your ability when they request a change in the care they are receiving from you."
                        "If a user specifically requests a change to the care they receive, it is your first responsibility to adjust to those changes accordingly in future conversations with the same user."
                        "Even though you are an AI you have access to past sessions."
                        "This is essential to tailoring your performance to individual users."
                        "Here is the user's data:\n\n" + self.summary
                    )
                }
            ]

            open(f"{file_path}/{file_name}", "w").write(json.dumps(conversation[0])+"\n")

        else:
            conversation = [json.loads(line) for line in open(f"{file_path}/{file_name}").readlines()]

        print("Summary provided to the chatbot:\n", self.summary)
        print("\nHello! How may I assist you?")

        # Chat loop so that the conversation will continue to run
        while True:
            user_input = input("User: ") 
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            conversation.append({"role": "user", "content": user_input})
            open(f"{file_path}/{file_name}", "a").write(json.dumps({"role": "user", "content": user_input})+"\n")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation
                )
                reply = response.choices[0].message.content
                print(f"Cassie: {reply}")
                conversation.append({"role": "assistant", "content": reply})
                open(f"{file_path}/{file_name}", "a").write(json.dumps({"role": "assistant", "content": reply})+"\n")

            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    backend = LLMBackend(1) 
    backend.chat_with_gpt()