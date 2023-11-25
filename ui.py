def testResponse(prmpt) :
    return prmpt.upper()
    

while True:
    try :
        prompt = input("#>>")
    except KeyboardInterrupt :
        print("goodbye!")
        
    response = testResponse(prompt)
    print("\033[92mhe$>> {}\033[00m".format(str(response)))
        
    
    
    