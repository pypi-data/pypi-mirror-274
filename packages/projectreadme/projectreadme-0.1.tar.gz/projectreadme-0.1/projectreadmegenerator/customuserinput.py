class custominput:
    """
    Gets input for the github project link
     
    Returns:
        String: Github project link 
    """
    @staticmethod
    def askforprojectlinkinput() -> str:
        link = input("Enter the link of the project: ")
        if not link:
            raise KeyError("no valid link")
        return link
     
    """
    Gets an input for the Gemini Api key to use as AI Model 
    
    Returns:
        String : Api key
    """
    @staticmethod
    def askfortheapikey() -> str:
        api_key = input("Please enter the api key for Gemini Model: ")
        if not api_key:
            raise KeyError("input the valid key")
        return api_key
    
      
    """
    Gets an input of the model they are using
    
    Returns:
        String : Model type
    """
    @staticmethod
    def askforthemodel() -> str:
        modelforg = input("What model are you using: ")
        if not modelforg:
            raise KeyError("Error model is invalid")
        return modelforg 
    
    