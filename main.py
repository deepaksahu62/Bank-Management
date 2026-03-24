import json
import random
import string
from pathlib import Path





class Bank():

    database = 'data.json'
    data = []


    try:                                     ## used for exception handling

        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())     ## json.loads , fs FILE SE DATA , data (dummy data storage area) ME STORE KR DETA H.
        else:
            print("No such file exists.")


    except Exception as err:
        print(f"an exception is occured as {err}")



    @classmethod
    def __update(cls):

        with open(cls.database , 'w') as fs:
            fs.write(json.dumps(Bank.data))


    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters , k=3)
        num = random.choices(string.digits , k=3)
        spchar = random.choices("!@#$%^&*" , k=1)

        id = alpha + num + spchar

        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
        
        info = {                                             ### json file me data key : values ke form me store hota h. {------}

            "name": input("tell your name :-"),
            "age" : int(input("tell your age :-")),
            "email" : input("tell your email :- "),
            "pin": int(input("tell your 4 digit pin :-")),
            "accountNo." : Bank.__accountgenerate() ,
            "ballance" : 0
        }

        if info["age"]<18 or len(str(info["pin"])) != 4 :
            print("sorry! , you cannot creat your account.")

        else:
            print("account has been created succesfully")

            for i in info :
                print(f"{i}:{info[i]}")
            print("please note down your account number.")        

            Bank.data.append(info)
            Bank.__update()


    def depositmoney(self):

        accnumber = input("please tell your account number :-")
        pin = int(input("please tell your 4 digit pin :-"))

        userdata = [i for i in Bank.data if i["accountNo."]== accnumber and i["pin"] == pin]


        if userdata == [] :
            print("data not found")

        else:
            amount = int(input("How much you want to depposit :-"))

            if amount > 10000 and amount > 0:
                print("sorry the ammount is too much you can deposit blow 1000 and above 0")

            else:
                userdata[0]['ballance'] +=amount

                Bank.__update()

                print("amount deposited successfully.")
        


    def withdrawmoney(self):
        accnumber=input("Enter your account number :-")
        pin = int(input("enter your 4 digit pin number :-"))

        userdata=[i for i in Bank.data if i['accountNo.'] == accnumber and i['pin']==pin]

        if userdata == []:
            print("no data found")

        else:
            amount = int(input("how much you want to withdraw : -"))

            if amount>userdata[0]['ballance']:
                print("sorry you dont have that much money")

            else:
                userdata[0]['ballance']-=amount

                Bank.__update()

                print(f"amount withdrew successfully , your current ballance is {userdata[0]['ballance']}")


    def showdetails(self):
        accnumber = input("enter your account number :- ")
        pin = int(input("enter your 4 digit pin :- "))

        userdata=[i for i in Bank.data if i['accountNo.']== accnumber and i['pin']==pin]
        if userdata == []:
            print("data not found")

        else:
            print("your information are :")

            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")


    
    def updatedetails(self):
        accnumber = input("enter your account number :- ")
        pin = int(input("enter your 4 digit pin :- "))

        userdata=[i for i in Bank.data if i['accountNo.']== accnumber and i['pin']==pin]
        
        if userdata == []:
            print("data not found")

        else:
            print("you cannot change the age , account number and ballance")
            print("press 1 for change the name")
            print("press 2 for change the Email")
            print("press 3 to change the pin")
            print("press 0 for exit.")

            while True:
                
                choice=int(input("Enter your choice :-"))

                if choice == 0 :
                    break

                if choice == 1:
                    userdata[0]['name'] = input("Enter new name :-")
                    print("name updated successfully.")

                if choice == 2 :
                    userdata[0]['email']=input("Enter your new email :- ")
                    print("Email updated successfully.")

                if choice == 3:
                    userdata[0]['pin']=input("Enter your new pin :- ")
                    print("pin updated successfully.")
                    
                choice2= int(input("press 0 for exit and 1 for continue :-  "))

                if choice2 == 0 :
                    break

                else:
                    print("you cannot change the age , account number and ballance")
                    print("press 1 for change the name")
                    print("press 2 for change the Email")
                    print("press 3 to change the pin")
                    print("press 0 for exit.")

        Bank.__update()

    def deleteaccount(self):
        accnumber = input("enter your account number :- ")
        pin = int(input("enter your 4 digit pin :- "))

        userdata=[i for i in Bank.data if i['accountNo.']== accnumber and i['pin']==pin]
        
        if userdata == []:
            print("data not found")

        else:
            check = input("press y if you actually want to delete the account or press n to cancel :- ")
            if check == "y" or check=="Y":
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully")

                Bank.__update()
            else:
                print("canceled")
        



user = Bank()

print("press 1 for creating an account")
print("press 2 for deepositing the money in the bank")
print("press 3 for withdrawing tthe money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting your account")


check = int(input("tell your responce :- "))


if check == 1:
    user.createaccount()


if check ==2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6 :
    user.deleteaccount()