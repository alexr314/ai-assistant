import openai
import numpy as np

openai.api_key = str(np.load('open_ai_key.npy'))

import markdown
from IPython.display import HTML, display, clear_output
    

def display_imessage(message, sender="user"):
    """Display a message in a styled box resembling iMessage, with markdown support. Sender can be 'user', 'system', or 'assistant'."""
    
    # Convert markdown to HTML, extensions are optional but can enhance functionality
    html_message = markdown.markdown(message, extensions=['extra', 'smarty'])
    
    # Define different styles for different senders
    styles = {
        "user": {
            "bg_color": "#007AFF",  # iMessage blue
            "text_color": "white",
            "align": "flex-end",
            "border_radius": "20px 20px 0px 20px"
        },
        "system": {
            "bg_color": "#E5E5EA",  # Light gray
            "text_color": "black",
            "align": "center",
            "border_radius": "20px 20px 20px 20px",
            "prefix": "SYSTEM: "
        },
        "assistant": {
            "bg_color": "#303030",  # Dark gray
            "text_color": "white",
            "align": "flex-start",
            "border_radius": "20px 20px 20px 0px"
        }
    }
    
    # Get the correct style based on sender
    style = styles.get(sender, styles["user"])
    if "prefix" in style:
        html_message = style["prefix"] + html_message
    
    # Define the HTML for the message
    html = f"""
    <div style="display: flex; justify-content: {style['align']}; margin: 5px;">
        <div style="max-width: 60%; min-width: 10%; background-color: {style['bg_color']}; color: {style['text_color']}; padding: 10px;
                    font-family: Arial, sans-serif; font-size: 16px; border-radius: {style['border_radius']};
                    word-wrap: break-word; margin-bottom: 2px;">
            {html_message}
        </div>
    </div>
    """
    display(HTML(html))

# Example usage:
display_imessage("Here is some **bold text** and _italic text_.\n\n1. First item\n2. Second item", "user")



def display_messages(messages):
    """
    Display a series of messages in a styled format resembling iMessage.
    Each message in the list is a dictionary with 'role' and 'content' keys.
    
    :param messages: List of message dictionaries.
    """
    for message in messages:
#         sender = "user" if message['role'] == "user" else "system"
        display_imessage(message['content'], sender=message['role'])

    
def make_message(role, content):
    '''helper function: formats message:
    {'role' : role, 'content' : content}'''
    
    return {'role' : role, 'content' : content}

class Session:
    
    def __init__(self, model='gpt-3.5-turbo-0125', system_message='You are a helpful assistant'):
        self.model = model
        self.messages = [make_message('system', system_message)]
        
        self.fail_counter = 0
        self.max_fails = 3
        self.verbose = True
        
    def add_system_message(self, content):
        self.messages.append(make_message('system', content))

    def add_user_message(self, content):
        self.messages.append(make_message('user', content))

    def generate_response(self):
        
        if self.fail_counter < self.max_fails:
            
            try:
                response = self._query_api()
                self.messages.append(dict(response['choices'][0].message))
            except:
                self.fail_counter += 1
                # try again
                if self.verbose: 
                    print(f'Query failed, retrying (#{self.fail_counter})')
                self.generate_response()
            
    def _query_api(self):
        # Broken off into its own function, will likely need maintance when we update openai
        return openai.ChatCompletion.create(model=self.model, messages=self.messages)
    
    def display_messages(self):
        display_messages(self.messages)
        
    def print_last(self):
        print(self.messages[-1]['content'])



def start_chat(system_prompt='You are a helpful assistant', model='gpt-3.5-turbo-0125'):
    '''Mimics the basic ChatGPT experience: takes user's text input and displays messages like iMessage'''
    
    # instantiate session
    chat = Session(system_message=system_prompt, model=model)
    
    while True:
        # get input
        user_message = input()
        if user_message.lower()=='end': break
            
        # redraw with user message
        clear_output(wait=True)
        chat.add_user_message(user_message)
        chat.display_messages()
        
        # redraw upon receipt of assistant message
        chat.generate_response()
        clear_output(wait=True)
        chat.display_messages()

    return chat