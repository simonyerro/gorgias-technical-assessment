# {Some company} APIs challenge 
## Intro

One of the challenges that we have in the Growth Team is to use our CRM data (HubSpot) to trigger any types of marketing actions. 
For instance, a marketing action would be to start tracking a given company in a tool called PredictLeads.

Then PredictLeads will start sending us webhooks (marketing buying intents) only on companies we follow - hence the need to follow the right companies.

Here, we want to pull all companies from HubSpot that match certain criteria, compare this list of companies with the companies we're already tracking in PredictLeads, and then follow or unfollow certain companies from PredictLeads, given HubSpot data. 

## Guidelines and context

Your goal is to: 
1. Pull all companies from HubSpot whose properties: 
 - 'ecommerce_platform' is equal to 'shopify' OR to 'magento_2'
 - AND Their 'alexa' property is under 1,000,000.
3. Fetch all companies we're already following in PredictLeads.
4. Compare the 2 sets of data: 
- If Company A is present in HubSpot set of data (given the above criteria) BUT is not present in PredictLeads set of data, THEN start following Company A in PredictLeads.
- If Company B is present in PredictLeads set of data BUT is not present in HubSpot set of data, THEN stop following Company B in PredictLeads. 
- If Company C is present in both set of data, THEN do nothing. 


### What are the constraints?

- Use the same approach that you would use for a regular task on the job
- Use best practices for API keys and token. API key will be provided in a secure 1password vault called '{Some company} Growth Engineering Hiring'. You should receive an email to access the secret vault.
- Use the HubSpot V3 API. Find the most suited endpoint(s) and explain your choice, docs: https://developers.hubspot.com/docs/api/overview
- Take into account pagination.
- Handle a potential throttling limit
- Use the most suited PredictLeads endpoints, docs: https://predictleads.com/docs/
- The code should be compatible with Python3.8.


### What is considered a success? 

- Focus on quality: Code as if you'd have to maintain this codebase later and keep building upon it.
- Focus on security: You don't want your API keys to get stolen.
- Part of the task is to find the right endpoints for each APIs used.
- Make your code structure and logs easy to understand: Comment your code and print/log intermediary results, to make the logs understandable by a marketing team.

Good luck!
