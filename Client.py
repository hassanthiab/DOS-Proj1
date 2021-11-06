import requests
BASE = "http://127.0.0.1:8000/"
BASE2 = "http://127.0.0.1:5000/"
while(1):

    UserInput = input("Enter Operation you want to perform \n 1 --> Search by Topic \n 2--> Search by ID \n 3-->Purchase \n 4--> Exit \n")

    if UserInput == "1":
        topic = input("Enter Topic name")
        response = requests.get(BASE + "search/"+topic)
        print(response.json())
    if UserInput == "2":
        ID = input("Enter ID of book")
        response = requests.get(BASE + "info/"+ID)
        print(response.json())
    if UserInput == "3":
        ID = input("Enter ID of book")
        response = requests.put(BASE2 + "purchase/"+ID)
        print(response.text)

    elif UserInput == "4":
        break
    else:
        print("Wrong Input, Try again")



