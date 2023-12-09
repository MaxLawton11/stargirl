# tester function 
def testResponse(prmpt) :
    return prmpt.upper()

def printLogo() :
    logo_raw = """
   _____ _       _ _          _____             _                 
  / ____| |     | | |        / ____|           (_)                
 | (___ | |_ ___| | | __ _  | (___  _   _  __ _ _ _   _ _ __ __ _ 
  \___ \| __/ _ \ | |/ _` |  \___ \| | | |/ _` | | | | | '__/ _` |
  ____) | ||  __/ | | (_| |  ____) | |_| | (_| | | |_| | | | (_| |
 |_____/ \__\___|_|_|\__,_| |_____/ \__,_|\__, |_|\__,_|_|  \__,_|
                                           __/ |                  
                                          |___/                 
--------------------------------------------------------------------                                                    
    """
    print(logo_raw)
    
def main() :
    printLogo()
    while True:
        try :
            prompt = input("#>>")
        except KeyboardInterrupt :
            print("\n goodbye!")
            
        response = testResponse(prompt)
        print("\033[92mhe$>> {}\033[00m".format(str(response)))
        
if __name__ == "__main__":
    main()
    
    