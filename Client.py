import requests
BASE = input("Enter the IP Server for Catalog (ONLY enter the server private IP EX:192.168.1.123\n")
BASE2 = input("Enter the IP Server for Orderlog (ONLY enter the server private IP EX:192.168.1.123\n")
while 1:

    UserInput = input("Enter Operation you want to perform \n 1 --> Search by Topic \n 2--> Search by ID \n 3-->Purchase \n 4--> Exit \n")
    if UserInput == "1":
        topic = input("Enter Topic name\n")
        response = requests.get("http://"+BASE + ":8000/" + "search/"+topic)
        print(response.json())
    elif UserInput == "2":
        ID = input("Enter ID of book\n")
        response = requests.get("http://"+BASE + ":8000/" + "info/"+ID)
        print(response.json())
    elif UserInput == "3":
        ID = input("Enter ID of book\n")
        response = requests.put("http://"+BASE2 + ":5000/"+ "purchase/"+ID)
        print(response.text)

    elif UserInput == "4":
        break
    else:
        print("Wrong Input, Try again")



