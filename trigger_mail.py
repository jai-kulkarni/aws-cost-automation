import datetime
from get_cost_details import get_cost_details
from utils import build_body_for_costing_mail, send_email

def trigger_mail():
    try:
        # Fetch date details
        date_info = get_date_details()

        # For daily cost
        start_date = date_info.get('day_before_yesterday').strftime("%Y-%m-%d")
        end_date = date_info.get('yesterday').strftime("%Y-%m-%d")
        display_date = date_info.get('day_before_yesterday').strftime("%d-%m-%Y")
        email_body_content = f"""
            Greetings!
            <br/>
            Please be advised that we have received the bill for organization accounts dated {display_date}
        """
        subject = "Daily Bill | AWS Organization Accounts"

        # For weekly cost (commented out)
        # start_date = date_info.get('week').strftime("%Y-%m-%d")
        # end_date = date_info.get('yesterday').strftime("%Y-%m-%d")
        # display_date = f"{date_info.get('week').strftime("%d-%m-%Y")} to {date_info.get('day_before_yesterday').strftime("%d-%m-%Y")}"
        # email_body_content = f"""
        #     Greetings!
        #     <br/>
        #     Please be advised that we have received the bill for organization accounts dated {display_date}
        # """
        # subject = "Weekly Bill | AWS Organization Accounts"

        # Retrieve billing details
        billing_details = get_cost_details(start_date=start_date, end_date=end_date)
        mail_content = generate_mail_content(billing_details)

        # Sort accounts cost in descending order
        sorted_mail_content = sorted(mail_content, key=lambda item: float(item['total']), reverse=True)

        # Build HTML and TEXT templates for email
        templates = build_body_for_costing_mail(sorted_mail_content, email_body_content)

        # Trigger email
        response = send_email(templates, subject)
        return response

    except Exception as e:
        # Log the error and return an error message
        error_message = f"An error occurred while triggering the mail: {str(e)}"
        return {
            'statusCode': 500,
            'body': error_message
        }


def get_date_details():
    """
    Retrieve date information for current day, yesterday, day before yesterday, and last week.
    """
    date_info = {
        "current_day": datetime.date.today(),
        "yesterday": datetime.date.today() - datetime.timedelta(1),
        "day_before_yesterday": datetime.date.today() - datetime.timedelta(2),
        "week": datetime.date.today() - datetime.timedelta(8),
    }
    return date_info


def generate_mail_content(billing_details):
    """
    Generate mail content based on billing details.
    """
    account_cost_data = []

    for account_id, services in billing_details.items():
        # Filter and round service costs
        service_costs = {
            service: round(float(cost), 2)
            for service, cost in services.items()
            if service not in ['total_cost', 'account_details']
        }

        # Sort and get top 5 services by cost
        top_services_list = sorted(service_costs.items(), key=lambda item: item[1], reverse=True)[:5]
        top_services = ',<br/>'.join(f"{service}: ${cost}" for service, cost in top_services_list)
        if not top_services:
            top_services = "No Services"

        account_cost_data.append({
            "account": f"{services['account_details']['Name']} <br/> ({account_id})",
            "account_type": services['account_details']['Type'],
            "account_status": services['account_details']['Status'],
            "total": round(services['total_cost'], 2),
            "top_services": top_services,
        })

    return account_cost_data
