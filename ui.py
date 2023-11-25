def testResponse(prmpt) :
    return prmpt.upper()

def printLogo() :
    logo_raw = """
     __  __              _                    _              
    |  \/  |            | |                  | |             
    | \  / | __ ___  __ | |     __ ___      _| |_ ___  _ __  
    | |\/| |/ _` \ \/ / | |    / _` \ \ /\ / / __/ _ \| '_ \ 
    | |  | | (_| |>  <  | |___| (_| |\ V  V /| || (_) | | | |
    |_|  |_|\__,_/_/\_\ |______\__,_| \_/\_/  \__\___/|_| |_|                                                   
    """
    print(logo_raw)
    
def main() :
    printLogo()
    while True:
        try :
            prompt = input("#>>")
        except KeyboardInterrupt :
            print("goodbye!")
            
        response = testResponse(prompt)
        print("\033[92mhe$>> {}\033[00m".format(str(response)))
        
if __name__ == "__main__":
    main()
    
    