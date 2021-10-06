import os
import requests
from ratelimiter import RateLimiter
import hubspot
from hubspot.crm.companies import PublicObjectSearchRequest, ApiException

HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
PREDICTLEADS_X_USER_EMAIL = os.getenv('PREDICTLEADS_X_USER_EMAIL')
PREDICTLEADS_X_USER_TOKEN = os.getenv('PREDICTLEADS_X_USER_TOKEN')


hubspot_search_limiter = RateLimiter(max_calls=4, period=1) # Hubspot Search API is limited to 4 calls by seconds, see here for more info: https://developers.hubspot.com/docs/api/usage-details#rate-limits

def hubspot_get_companies(client, query, limit=100) -> set:
    """
    Get every companies from Hubspot API matching the given query

    :param client: Hubspot client
    :param query: Companies are retrieved based on this criteria
    :param limit: number of companies retrieved by API call
    :return: set of companies website
    """
    after, all_response = 0, []
    while after != None:
        request = PublicObjectSearchRequest(filter_groups=query, properties=["name", "website"], limit=limit, after=after)
        try:
            with hubspot_search_limiter:
                api_response = client.crm.companies.search_api.do_search(public_object_search_request=request)
        except ApiException as e:
            raise SystemExit("Exception when calling search_api: {}".format(e))
        after = api_response.paging.next.after if api_response.paging and api_response.paging.next else None
        all_response.extend(api_response.results)
    return set([res.properties['website'] for res in all_response])

def predictleads_get_all_companies(user_email=PREDICTLEADS_X_USER_EMAIL, user_token=PREDICTLEADS_X_USER_TOKEN) -> set:
    """
    Get every companies from Predictleads API

    :param user_email: email account used to authenticate on Predictleads API
    :param user_token: token used to authenticate on Predictleads API
    :return: set of companies website
    """
    payload = {'user_email': user_email, 'user_token': user_token}
    try:
        r = requests.get('https://predictleads.com/api/v2/followings', params=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit("Exception when getting all companies on PredictLeads: {}".format(e))
    return set([companies['domain'] for companies in r.json()])

def _predictleads_company_action(action, company, user_email=PREDICTLEADS_X_USER_EMAIL, user_token=PREDICTLEADS_X_USER_TOKEN) -> bool:
    """
    Call PredictLeads endpoint depending on action given (currently follow and unfollow)

    :param action: Can be either follow or unfollow
    :param company: the company aimed
    :param user_email: email account used to authenticate on Predictleads API
    :param user_token: token used to authenticate on Predictleads API
    :return: True if everything went fine
    """
    payload = {'user_email': user_email, 'user_token': user_token}
    try:
        r = requests.post('https://predictleads.com/api/v2/companies/{}/{}'.format(company, action), params=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit("Exception when following {} on PredictLeads: {}".format(company, e))
    return r.status_code == 200

def predictleads_follow_company(company, user_email=PREDICTLEADS_X_USER_EMAIL, user_token=PREDICTLEADS_X_USER_TOKEN) -> bool:
    """
    Call PredictLeads follow endpoint

    :param company: the company aimed
    :param user_email: email account used to authenticate on Predictleads API
    :param user_token: token used to authenticate on Predictleads API
    :return: True if everything went fine
    """
    _predictleads_company_action('follow', company, user_email=user_email, user_token=user_token)

def predictleads_unfollow_company(company, user_email=PREDICTLEADS_X_USER_EMAIL, user_token=PREDICTLEADS_X_USER_TOKEN) -> bool:
    """
    Call PredictLeads unfollow endpoint

    :param company: the company aimed
    :param user_email: email account used to authenticate on Predictleads API
    :param user_token: token used to authenticate on Predictleads API
    :return: True if everything went fine
    """
    _predictleads_company_action('unfollow', company, user_email=user_email, user_token=user_token)

def compare_dataset(predictleads_websites, hubspot_websites) -> None:
    """
    Compare the PredictLeads and Hubspot companies dataset

    :param predictleads_websites: Set of website from PredictLeads
    :param hubspot_websites: Set of website from Hubspot
    """
    for company in hubspot_websites - predictleads_websites:
        if not predictleads_follow_company(company):
            print("failed to follow company {}".format(company))
    for company in predictleads_websites - hubspot_websites:
        if not predictleads_unfollow_company(company):
            print("failed to unfollow company {}".format(company))

if __name__ == '__main__':
    if None in (HUBSPOT_API_KEY, PREDICTLEADS_X_USER_EMAIL, PREDICTLEADS_X_USER_TOKEN):
        raise ValueError("""Some API key are missing, it should be provided by environment variable
            You need to provide HUBSPOT_API_KEY, PREDICTLEADS_X_USER_EMAIL, PREDICTLEADS_X_USER_TOKEN""")
    hubspot_client = hubspot.Client.create(api_key=HUBSPOT_API_KEY)
    query = [
        {"filters": [{"value": "shopify","propertyName": "ecommerce_platform","operator": "EQ"}, {"value": 1000000,"propertyName": "alexa","operator": "LT"}]},
        {"filters": [{"value": "magento_2","propertyName": "ecommerce_platform","operator": "EQ"}, {"value": 1000000,"propertyName": "alexa","operator": "LT"}]}
    ]
    hubspot_websites = hubspot_get_companies(hubspot_client, query)
    predictleads_websites = predictleads_get_all_companies()
    compare_dataset(predictleads_websites, hubspot_websites)