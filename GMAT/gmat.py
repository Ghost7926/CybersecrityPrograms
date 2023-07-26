#!/bin/python3
import requests
import click
import json

'''
@click.command()
@click.option('-T', '--target', default=None, required=True, help='Your target.')
'''

def fetch_company_domain(company_name):
    api_url = f"https://api.hunter.io/v2/domain-search?company={company_name}&api_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    hunter_results = requests.get(api_url)
    hunter_data = hunter_results.json()
    
    # For debugging purposes
    print(hunter_data)

    domain = hunter_data['data']['domain']
    return domain


def dehashed_information(target_arg):
    headers = {'Accept': 'application/json'}
    params = (('query', f'domain:{target_arg}'),)
    
    dehashed_json = requests.get('https://api.dehashed.com/search',
        headers=headers,
        params=params,
        auth=('XXXXXXXXX@XXXXXX.com', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')).text
    
    return dehashed_json


# For debugging purposes
#print(target)


domain = fetch_company_domain("Grand Canyon University")
if domain:
    print("Domain: ", domain)
else:
    print("No domain found for the company domain on Hunter.io.")

results = dehashed_information(domain)
if results:
    # For debugging purposes
    print(results)

    # reformat to json, better viewing
    data_dict = json.loads(results)
    formatted_results = json.dumps(data_dict, indent=4)

    print(formatted_results)
else:
    print("No information found for the domain on dehashed.com.")




'''
put the results to a file
clean up the initil print
put the full hunter.io to a file
fix the click stuff
try to delete the blank variables 
create orcing the domain, add the domain hunter.io api
'''
