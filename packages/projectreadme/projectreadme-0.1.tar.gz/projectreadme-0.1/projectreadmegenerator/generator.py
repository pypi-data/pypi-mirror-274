from .customuserinput import custominput
import google.generativeai as genai
import time
from .storage import Storage
import os
from dotenv import load_dotenv

class generate:
    def generatereadmefile():
        STORAGE = Storage
        CUSTOMER_INPUT = custominput

        load_dotenv()

        API_KEY = os.getenv("API_KEY")
        MODEL_USING = os.getenv("MODEL")

        if not API_KEY or not MODEL_USING:
            print('Value not provided')
            API_KEY = API_KEY or CUSTOMER_INPUT.askfortheapikey().strip().replace(' ', '')
            MODEL_USING = MODEL_USING or CUSTOMER_INPUT.askforthemodel().strip().replace(' ', '')
            if(STORAGE.storetheapikey(API_KEY, MODEL_USING)): 
                print('ENV file is added')
            
            
        PROJECT_LINK = CUSTOMER_INPUT.askforprojectlinkinput()

        genai.configure(api_key=API_KEY)

        try:
            model = genai.GenerativeModel(model_name=MODEL_USING)
        except Exception as e:
            raise ValueError(f"Failed to initialize the model with name '{MODEL_USING}': {e}")

        response = model.generate_content(f"Please generate a beautiful and step by step README FILE for the project link {PROJECT_LINK}")

        def writereadme():
            while True:
                try:
                    with open('README.md', 'w', encoding='utf-8') as readme_file:
                        readme_file.write(response.text)

                    with open('README.md', 'r', encoding='utf-8') as readme_file:
                        content_written = readme_file.read()
                        
                    if content_written == response.text:
                        print('Readme file is generated')
                        break
                    
                except Exception as e:
                    print("Error occurred while reading/writing the README file:", e)
                
                time.sleep(1)
        writereadme()
        
    generatereadmefile()


