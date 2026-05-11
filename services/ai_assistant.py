import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


class BakeryAIAssistant:
    def __init__(self, manager, log_path="ai-assistant/ai_logs.json"):
        self.manager = manager
        self.log_path = Path(log_path)

        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def build_context(self, user_email):
        user_orders = self.manager.find_orders_by_customer(user_email)
        inventory = self.manager.all_inventory()

        return f"""
        Bakery inventory:
        {json.dumps(inventory, indent=2)}

        Current customer's orders:
        {json.dumps(user_orders, indent=2)}
        """

    def get_response(self, messages, user_email):
        if self.client is None:
            return "OpenAI API key was not found. Please check your .env file."

        context = self.build_context(user_email)

        system_prompt = f"""
        You are a helpful bakery assistant for Blossom and Nandika's Bakery Delights.

        Help customers understand:
        - what items are available
        - how to place an order
        - how to view their cart
        - how to check order status
        - how to cancel placed orders

        Use only the bakery data provided below. 
        Do not make up fake orders or fake inventory.

        Context:
        {context}
        """

        final_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages

        try:
            response = self.client.chat.completions.create(
                model="gpt-5-mini",
                messages=final_messages
            )

            return response.choices[0].message.content

        except Exception:
            return "AI assistant is currently unavailable because the OpenAI API quota has been exceeded."

    def load_logs(self):
        if self.log_path.exists():
            with open(self.log_path, "r") as f:
                return json.load(f)
        return []

    def save_logs(self, logs):
        self.log_path.parent.mkdir(exist_ok=True)

        with open(self.log_path, "w") as f:
            json.dump(logs, f, indent=4)