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
    
        """
        If the environment file is stored (.env), the function loads that env file corresponding 
        to the working directory 

        Returns:
            DOTENV_PATH: Returns the path for environment file under the working directory 
        """
    
    @staticmethod
    def env_module_loader() -> str:
        working_path = os.getcwd()
        dotenv_path = f'{working_path}\\.env'
        return dotenv_path