# 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

import openai
API_KEY = "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"
openai.api_key = API_KEY
def chatGPTResponse(conversation):
    try:
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages=conversation
        )
    except openai.error.APIConnectionError:
        return None
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation
