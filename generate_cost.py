import boto3 # type: ignore


def generate_services_cost(account_details, **kwargs):
    """
    Generate service costs for each account based on the provided account details and date range.
    
    Args:
        account_details (dict): A dictionary containing details of each account.
        **kwargs: Additional keyword arguments including 'start_date' and 'end_date'.
    
    Returns:
        dict: A dictionary containing the service costs for each account.
    """
    bill = {}

    try:
        # Extract account IDs from account details
        account_ids = list(account_details.keys())
        # Get cost and usage data for the specified date range and account IDs
        response = get_cost_and_usage(start=kwargs['start_date'], end=kwargs['end_date'], account_ids=account_ids)
    except Exception as e:
        print(f"Error in fetching cost data: {str(e)}")
        return {}

    # Process cost data
    for rec in response.get('ResultsByTime', []):
        for item in rec.get('Groups', []):
            try:
                account_id = item['Keys'][0]
                service_name = item['Keys'][1].replace(" ", "").replace("-", "")
                service_cost = float(item['Metrics']['UnblendedCost']['Amount'])

                if account_id not in bill:
                    # Initialize account entry in bill dictionary
                    bill[account_id] = {
                        service_name: service_cost,
                        'total_cost': round(service_cost, 4),
                        'account_details': account_details.get(account_id, "")
                    }
                else:
                    # Update service cost and total cost for existing account entry
                    if service_name in bill[account_id]:
                        bill[account_id][service_name] += service_cost
                    else:
                        bill[account_id][service_name] = service_cost
                    bill[account_id]['total_cost'] += round(service_cost, 4)
                
            except Exception as err:
                print(f"Error in processing item {item}: {str(err)}")

    return bill


def get_cost_and_usage(**kwargs):
    """
    Get cost and usage data from AWS Cost Explorer API.
    
    Args:
        **kwargs: Additional keyword arguments including 'start' (start date), 'end' (end date), and 'account_ids' (list of account IDs).
    
    Returns:
        dict: A dictionary containing the cost and usage data.
    """
    try:
        client = boto3.client('ce')
        # Get cost and usage data from AWS Cost Explorer API
        response = client.get_cost_and_usage(
            TimePeriod={
                "Start": kwargs['start'],
                "End": kwargs['end']
            },
            Filter={
                "And": [
                    {
                        "Dimensions": {
                            "Key": "LINKED_ACCOUNT",
                            "Values": kwargs['account_ids']
                        }
                    },
                    {
                        "Not": {
                            "Dimensions": {
                                "Key": "RECORD_TYPE",
                                "Values": ["Refund", "Credit"]
                            }
                        }
                    }
                ]
            },
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "LINKED_ACCOUNT"
                },
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                },
            ]
        )

        return response
    except Exception as e:
        print(f"Error in getting cost and usage data: {str(e)}")
        raise

