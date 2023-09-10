from dotenv import load_dotenv
import re
import os
import vt
import json

def configure():
    load_dotenv()
configure()
api_key: str = os.getenv('API_KEY')
client = vt.Client(api_key)

def extract_urls(message):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(message)
    return urls

async def handle_response(user_message: str, is_private: bool) -> str:
    p_message = user_message.lower()
    urls = extract_urls(p_message)

    if urls:
        try:
            url_id = vt.url_id(urls[0])
            url = await client.get_object_async("/urls/{}", url_id)
            return f"```json\n{json.dumps(url.last_analysis_stats, indent=4)}\n```"
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return(f"An unexpected error occurred: {str(e)}")
    
    if p_message == 'hello':
        return 'Hey there!'

    if p_message == 'help' and is_private:
        return "`This is a help message that you can modify.`"
    
    return