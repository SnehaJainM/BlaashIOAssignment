import requests
import time

def send_sms(mobile_number, message, retries=3):
    url = "https://nextsmswave.in"
    headers = {"Authorization": "yyn&8934nkjjfdjf8934jkjf"}
    
    for attempt in range(retries):
        response = requests.post(url, headers=headers, json={"mobile_number": mobile_number, "message": message})
        
        if response.json() == True:
            print("Message sent successfully")
            return True
        else:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)
    
    print("Failed to send message after retries")
    return False
