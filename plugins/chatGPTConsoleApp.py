import openai

API_KEY = "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"
openai.api_key = API_KEY

chat_log = []


if __name__ == '__main__':
    while True:
        user_message = input("User: ")
        if user_message.lower() == "quit":
            break
        else:
            chat_log.append({'role': 'user', 'content': user_message})
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=chat_log,
            )
            bot_response = response['choices'][0]['message']['content'].strip('\n').strip()
            print("ChatGPT: ", bot_response)
            chat_log.append({'role': 'assistant', 'content': bot_response})

