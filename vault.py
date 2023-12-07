import requests

def get_Access_Token():

    headers = {
        'content-type': 'application/json',
    }

    json_data = {
        'audience': 'https://api.hashicorp.cloud',
        'grant_type': 'client_credentials',
        'client_id': 'BZNxHqqoqZut73uPhS53Yjg4HzQvaVgv',
        'client_secret': 's7yE55_l_7eaglWL7LkvvMzndbut7j2jcJUAisnuUa1bNpF98mZqdNRgDN05rwlM',
    }

    response = requests.post('https://auth.hashicorp.com/oauth/token', headers=headers, json=json_data)


    access_token = response.json()['access_token']

    return access_token

def get_Secret(name):

    access_token = get_Access_Token()

    headers = {
        'Authorization': 'Bearer '+access_token,
    }

    response = requests.get(
        'https://api.cloud.hashicorp.com/secrets/2023-06-13/organizations/2af6525e-9feb-4bb6-9884-58fba77be0d3/projects/f51f708f-9559-47b8-8a69-7bced9ef0407/apps/mvp-streamlit/open',
        headers=headers,
    )

    secrets = response.json()['secrets']
    # print(secrets)

    for secret in secrets:
        if secret['name']==name:
            # print(secret)
            return(secret['version']['value'])
    return None

if __name__=="__main__":
    secret = get_Secret('test1')

    if secret:
        print("Yes, the secret is ",secret)
    else:
        print("Secret Not Found")