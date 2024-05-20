#bot.py
import os
import json
import re
import hashlib
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
import random
import pwinput as pw
import asyncio
import aiofiles

# Ensure necessary NLTK data is downloaded
nltk_data_path = 'nltk_data'
if not os.path.exists(nltk_data_path):
    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('stopwords', download_dir=nltk_data_path)
nltk.data.path.append(nltk_data_path)

class Bot:
    def __init__(self, name):
        self.name = name
        self.engine = pyttsx3.init()
        self.users = {}
        self.current_user = None
        self.non_alpha_re = re.compile(r'[^a-zA-Z]')
        self.conversations = self.load_conversations("conversations.json")
        self.preprocessed_questions = [(entry["question"], self.preprocess_text(entry["question"])) for entry in self.conversations]

    def preprocess_text(self, text):
        corrected_text = str(TextBlob(text).correct())
        tokens = word_tokenize(corrected_text)
        stop_words = set(stopwords.words('english'))
        tokens = [self.non_alpha_re.sub('', token).lower() for token in tokens if token.lower() not in stop_words]
        tokens = [token for token in tokens if token]
        return tokens

    def generate_response(self, user_input):
        max_similarity = 0
        best_response = None
        if not self.conversations:
            return "I'm sorry, I don't have any conversations to reference."
        try:
            user_input_tokens = self.preprocess_text(user_input)
            for question, question_tokens in self.preprocessed_questions:
                common_tokens = set(question_tokens) & set(user_input_tokens)
                similarity = len(common_tokens) / max(len(question_tokens), len(user_input_tokens)) if len(question_tokens) and len(user_input_tokens) else 0
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = next(entry["answers"] for entry in self.conversations if entry["question"] == question)
            if best_response:
                return random.choice(best_response)
            else:
                return "I'm sorry, I didn't understand your question."
        except BaseException as e:
            return f"Error: {e}"

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error with TTS engine: {e}")

    async def load_users(self):
        try:
            async with aiofiles.open("users.json", 'r') as file:
                self.users = json.loads(await file.read())
        except FileNotFoundError:
            pass

    async def save_users(self):
        async with aiofiles.open("users.json", 'w') as file:
            await file.write(json.dumps(self.users, indent=4))

    def is_admin(self, username):
        if username in self.users:
            return self.users[username].get('is_admin', False)
        return False

    def edit_username(self, username, new_name):
        if username in self.users:
            self.users[username]['username'] = new_name
            asyncio.run(self.save_users())
            print(f"Username for {username} has been changed to {new_name}.")
        else:
            print("User not found.")

    def manage_chats(self, username):
        if self.is_admin(username):
            print("Admin access granted. You can manage chats here.")
        else:
            print("You do not have permission to manage chats.")

    async def load_chat_logs(self, username):
        chat_log_file = os.path.join("chat_logs", f"{username}.json")
        if os.path.exists(chat_log_file):
            async with aiofiles.open(chat_log_file, 'r') as file:
                try:
                    return json.loads(await file.read())
                except json.decoder.JSONDecodeError:
                    return []
        else:
            return []

    async def save_chat_log(self, username, chat_log):
        chat_log_file = os.path.join("chat_logs", f"{username}.json")
        async with aiofiles.open(chat_log_file, 'w') as file:
            await file.write(json.dumps(chat_log, indent=4))

    def view_chat(self, username):
        chat_log_file = os.path.join("chat_logs", f"{username}.json")
        if os.path.exists(chat_log_file):
            async def read_chat_log():
                async with aiofiles.open(chat_log_file, 'r') as file:
                    return json.loads(await file.read())
            chat_log = asyncio.run(read_chat_log())
            print(f"Chat log for {username}:")
            for entry in chat_log:
                print(f"User: {entry['user']}")
                print(f"Bot: {entry['bot']}")
                print("-" * 20)
        else:
            print(f"No chat log found for {username}.")

    def process_input(self, user_input):
        user_input_lower = user_input.lower()
        if user_input_lower == "login":
            self.login()
        elif user_input_lower == "signup":
            self.signup()
        elif user_input_lower == "what's my name?":
            print(f"Your name is {self.current_user}.")
        elif user_input_lower.startswith("change my name to "):
            new_name = user_input[17:].strip()
            self.edit_username(self.current_user, new_name)
        elif user_input_lower.startswith("view chat log for "):
            username = user_input[18:].strip()
            if self.is_admin(self.current_user):
                self.view_chat(username)
            else:
                print("You do not have permission to view chats.")
        else:
            bot_response = self.generate_response(user_input)
            print(f"{self.name}: {bot_response}")
            self.speak(bot_response)
            if self.current_user:
                chat_log = asyncio.run(self.load_chat_logs(self.current_user))
                chat_log.append({'user': user_input, 'bot': bot_response})
                asyncio.run(self.save_chat_log(self.current_user, chat_log))

    def login(self):
        username = input("Username: ")
        password = pw.pwinput(prompt="Password: ", mask="*")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username in self.users and self.users[username]['password'] == password_hash:
            print(f"Welcome back, {username}!")
            self.current_user = username
        else:
            print("Invalid username or password.")

    def signup(self):
        username = input("Choose a username: ")
        password = pw.pwinput(prompt="Choose a password: ", mask="*")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username not in self.users:
            self.users[username] = {'password': password_hash}
            asyncio.run(self.save_users())
            print(f"Account created successfully for {username}.")
        else:
            print("Username already exists. Please choose another one.")

    def load_conversations(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error loading conversations from {file_path}")
            return []

    def listen_for_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio)
            print(f"{self.current_user if self.current_user else 'You'}: {user_input}")
            self.process_input(user_input)
        except sr.UnknownValueError:
            print(f"{self.name}: Sorry, I could not understand your speech.")
        except sr.RequestError as e:
            print(f"{self.name}: Speech recognition request failed:", e)

def run():
    bot = Bot(name="JZ")
    asyncio.run(bot.load_users())

    try:
        while True:
            if not bot.current_user:
                user_choice = input("Do you want to (login) or (signup)? ")
                if user_choice.lower() == "login":
                    bot.login()
                elif user_choice.lower() == "signup":
                    bot.signup()
                else:
                    print("Invalid choice. Please enter 'login' or 'signup'.")
                    continue
            user_input = input(f"{bot.current_user if bot.current_user else 'You'}: ")
            if user_input.lower() == 'exit':
                break
            if user_input.lower() == '/m':
                bot.listen_for_input()
            else:
                bot.process_input(user_input)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        bot.engine.stop()

if __name__ == "__main__":
    import cProfile
    cProfile.run('run()')
