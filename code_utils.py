import re
import openai
import numpy as np

openai.api_key = str(np.load('open_ai_key.npy'))


def query(message, system_prompt='You are a helpful assistant.', model='gpt-3.5-turbo-0125'):
    """
    The most basic kind of call to GPT, just gets a simple answer to the given message
    """
    messages = [make_message('system', system_prompt),
                make_message('user', message)]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    content = response.choices[0].message['content']
    return content


def extract_python(input_string):
    """
    Given a string containing ```python <python code>``` (as ChatGPT likes to write) 
    this function returns all those code blocks (the <python code> in the above example)
    """
    pattern_python_code = r'```python\s(.*?)```'
    matches = re.findall(pattern_python_code, input_string, re.DOTALL)
    return matches


def extract_bash(input_string):
    """
    Given a string containing ```bash <bash code>``` (as ChatGPT likes to write) 
    this function returns all those code blocks (the <bash code> in the above example)
    """
    pattern_bash_code = r'```bash\s(.*?)```'
    matches = re.findall(pattern_bash_code, input_string, re.DOTALL)
    return [m.strip('\n') for m in matches]


def reformat_code(code):
    """
    Queries GPT 3.5 and gets it to fix errors (mostly indentation) in given code.
    """
    prompt = "Your job is to take python code an correct indentation errors. The code will most likely not have any indentation. Use spaces to indent. DO NOT alter the code or make any transcription errors. DO NOT reply with anything other than the corrected code."
    return query(code, system_prompt=prompt, model='gpt-3.5-turbo-0125')