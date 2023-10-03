import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from getpass import getpass


def main():
    os.system('clear')

    url = 'https://chedro5stufap.com/index.php/grantee_auth/login_validation'
    target_url = 'https://chedro5stufap.com/grantee'

    award_no, password = get_user_credentials()

    payload = {
     'award_no': award_no,
     'password': password
    }

    response = request_data(url, target_url, payload)

    if response.status_code == 200:
        content = BeautifulSoup(response.text, 'html.parser')
        scholarship_data = parse_scholarship_data(content)
        grantee_data = parse_grantee_data(content)

        print("\nGrantee Information:")
        print("Name: {}".format(grantee_data["name"]))
        print("Application Number: {}".format(grantee_data["application_number"]))
        print("Status: {}".format(grantee_data["status"]))
        print("HEI Name: {}".format(grantee_data["hei_name"]))
        print("Degree: {}".format(grantee_data["degree"]))
        print("")
        print("Scholarship Data:")
        print(tabulate(scholarship_data[1:10], headers=scholarship_data[0], tablefmt='fancy_grid'))
    else:
        print("Error: Invalid credentials.")


def get_user_credentials():
    award_no = input("Enter award number: ")
    password = getpass("Enter password: ")
    print("")

    return award_no, password


def request_data(url, target_url, payload):
    with requests.Session() as session:
        session.post(url, data = payload)
        response = session.get(target_url)

    return response
    

def parse_scholarship_data(content):
    table = content.find('table')
    table_rows = table.find_all('tr')

    data = []

    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        data.append(row)

    for row in data:
        while len(row) < 8:
            row.insert(0, '')

    return data


def parse_grantee_data(content):
    name = content.find("h3", {"class": "text-success"})
    application_number = content.find("b", {"class": "text-danger"})
    other_info = content.find_all("b", {"class": "text-primary"})
    status = other_info[0]
    hei_name = other_info[1]
    degree = other_info[2]

    grantee_data = {
        "name": name.text,
        "application_number": application_number.text,
        "status": status.text,
        "hei_name": hei_name.text,
        "degree": degree.text
    }

    return grantee_data


if __name__ == "__main__":
    main()
