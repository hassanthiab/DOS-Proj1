import requests
import time
#Link for Client Server
# This needs to be filled twice in terminal for some reason
BASE = input("Enter the IP Server for Client Front Server (ONLY enter the server private IP EX:192.168.1.123\n")
while 1:
    # Performs a request towards the ClientServer based on the Input
    UserInput = input("Enter Operation you want to perform \n 1 --> Search by Topic \n 2--> Search by ID \n 3-->Purchase \n 4--> Exit \n")
    if UserInput == "1":
        topic = input("Enter Topic name\n")
        response = requests.get("http://"+BASE + ":6000/" + "search/"+topic)
        print(response.json())
        print(response.elapsed.total_seconds())

    elif UserInput == "2":
        ID = input("Enter ID of book\n")
        response = requests.get("http://"+BASE + ":6000/" + "info/"+ID)
        print(response.json())
        print(response.elapsed.total_seconds())
    elif UserInput == "3":
        ID = input("Enter ID of book\n")
        response = requests.put("http://"+BASE + ":6000/" + "purchase/"+ID)
        print(response.text)
        print(response.elapsed.total_seconds())
    elif UserInput == "4":
        break
    else:
        print("Wrong Input, Try again")



