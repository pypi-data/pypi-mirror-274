import os 
class Storage:
    """
    The function ask for the API key for the Gemini and the model for the Gemini,
    then it outputs the envfile content so that user does not have to store the or enter the key again
    and again
    """
    @staticmethod 
    def storetheapikey(api_key , project_model):
        content = f'API_KEY = {api_key} \nMODEL = {project_model}'
        env_file_path = os.path.join(os.getcwd(), '.env')   
        with open(env_file_path, 'w') as envfile:
            envfile.write(content)
            