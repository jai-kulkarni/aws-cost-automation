import json
import boto3  # type: ignore
import re
from utils import datetime_handler
from generate_cost import generate_services_cost

def get_cost_details(**kwargs):
    """
    Retrieve cost details for all accounts by generating service costs.
    
    Args:
        **kwargs: Additional arguments to pass to the generate_services_cost function.
    
    Returns:
        dict: A dictionary containing the cost details for all accounts.
    """
    try:
        accounts = list_organization_accounts()
        accounts_costing = generate_services_cost(accounts, **kwargs)
        return accounts_costing
    except Exception as e:
        error_message = f"An error occurred while retrieving cost details: {str(e)}"
        print(error_message)
        raise

def list_organization_accounts():
    """
    List all organization accounts recursively.
    
    Returns:
        dict: A dictionary containing all organization accounts with their details.
    """
    try:
        org_client = boto3.client('organizations', region_name='us-east-1')
        accounts_paginator = org_client.get_paginator('list_accounts_for_parent')
        ou_paginator = org_client.get_paginator('list_organizational_units_for_parent')

        def get_accounts_recursive(parent_id):
            """
            Recursively retrieve accounts under a given parent ID.
            
            Args:
                parent_id (str): The parent ID to list accounts and organizational units for.
            
            Returns:
                list: A list of accounts.
            """
            accounts = []
            # List accounts for the given parent ID
            for page in accounts_paginator.paginate(ParentId=parent_id):
                for account in page['Accounts']:
                    management_account = re.search(r'::(\d+):', account['Arn']).group(1)
                    comparison_account = account['Arn'][-12:]
                    account['Type'] = "Management Account" if management_account == comparison_account else "Member Account"
                accounts.extend(page['Accounts'])

            # List organizational units for the given parent ID
            for page in ou_paginator.paginate(ParentId=parent_id):
                for ou in page['OrganizationalUnits']:
                    accounts.extend(get_accounts_recursive(ou['Id']))

            return accounts

        # Get root ID and list all accounts recursively
        root_id = org_client.list_roots()["Roots"][0]["Id"]
        organization_accounts = get_accounts_recursive(root_id)

        # Structure the organization accounts
        structured_org_accounts = {account["Id"]: {**account} for account in organization_accounts}

        return json.loads(json.dumps(structured_org_accounts, default=datetime_handler))

    except Exception as e:
        error_message = f"An error occurred while listing organization accounts: {str(e)}"
        print(error_message)
        raise
