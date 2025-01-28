import json

class ChatBot:
    def __init__(self):
        self.input_handler = InputHandler()
        self.intent_processor = IntentProcessor()
        self.response_generator = ResponseGenerator()
        self.knowledge_base = self.load_knowledge_base()  # Load knowledge from a file

    def handle_message(self, message):
        # Process the user message
        sanitized_message = self.input_handler.sanitize_input(message)
        intents = self.intent_processor.detect_intents(sanitized_message)

        if not intents:
            response = self.learn_new_question(sanitized_message)  # Learning process for unknown intents
        else:
            response = self.response_generator.generate_responses(intents)

        return response

    def learn_new_question(self, question):
        print(f"ChatBot: I don't know how to respond to that. Can you teach me the correct response?")
        correct_response = input("You (teaching): ")

        # Ask for a keyword that should trigger this response
        keyword = input("What keyword should trigger this response? ").strip().lower()

        # Save the new question, response, and keyword in the knowledge base
        self.knowledge_base[keyword] = correct_response
        self.save_knowledge_base()
        return f"Got it! I'll remember that. The keyword '{keyword}' will trigger the response."

    def load_knowledge_base(self):
        try:
            with open("knowledge_base.json", "r") as file:
                if file.read().strip() == "":
                    return {}  # Return an empty dictionary if the file is empty
                file.seek(0)
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_knowledge_base(self):
        with open("knowledge_base.json", "w") as file:
            json.dump(self.knowledge_base, file)


class InputHandler:
    def sanitize_input(self, message):
        return message.strip().lower()


class IntentProcessor:
    def detect_intents(self, message):
        intents = []
        # Predefined intents
        if "hello" in message:
            intents.append("greeting")
        if "help" in message:
            intents.append("help")
        # Learned intents (case-insensitive matching)
        for keyword in chatbot.knowledge_base:
            if keyword in message:  # Both are already lowercase
                intents.append(keyword)
        return intents


class ResponseGenerator:
    def generate_responses(self, intents):
        responses = {
            "greeting": "Hello! I'm a chatbot.",
            "help": "Sure, what do you need help with?",
        }
        generated_responses = []

        for intent in intents:
            if intent in responses:
                generated_responses.append(responses[intent])
            elif intent in chatbot.knowledge_base:
                generated_responses.append(chatbot.knowledge_base[intent])

        # Join multiple responses into separate sentences
        return " ".join(generated_responses)


# Initialize the ChatBot
chatbot = ChatBot()

# Console Chat Loop with Learning Capability
def start_console_chat():
    print("Welcome to the Learning ChatBot! Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = chatbot.handle_message(user_input)
        print(f"ChatBot: {response}")


if __name__ == "__main__":
    start_console_chat()
