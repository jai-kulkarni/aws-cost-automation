import dateutil.parser as parser # type: ignore
from datetime import datetime
import boto3 # type: ignore

def datetime_handler(iso_datetime):
    """
    Convert ISO date format to human-readable format.
    
    Args:
        iso_datetime (datetime): The ISO datetime object to be formatted.
    
    Returns:
        str: The formatted date and time string.
    
    Raises:
        TypeError: If the input is not a datetime object.
    """
    try:
        if isinstance(iso_datetime, datetime):
            # Convert datetime object to string in the desired format
            formatted_datetime = iso_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # Parse the formatted string to handle timezones
            parsed_datetime = parser.parse(formatted_datetime)
            return str(parsed_datetime)
        else:
            raise TypeError("Input is not a datetime object")
    except Exception as e:
        print(f"An error occurred while formatting the datetime: {str(e)}")
        raise


def send_email(templates, subject):
    """
    Send an email using AWS SES with the provided templates and subject.
    
    Args:
        templates (dict): A dictionary containing text and HTML email templates.
        subject (str): The subject of the email.
    
    Returns:
        dict: The response from the SES service.
    """
    try:
        to_addresses = ["user1@email.com", "user2@email.com"]
        cc_addresses = []
        bcc_addresses = []
        text_template, html_template = templates['text_template'], templates['html_template']
        
        ses_client = boto3.client('ses', region_name='us-east-1')
        response = ses_client.send_email(
            Source="<no-reply@email.com>", # Your email address goes here
            Destination={
                'ToAddresses': to_addresses,
                'CcAddresses': cc_addresses,
                'BccAddresses': bcc_addresses
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': text_template,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': html_template,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        print("Mail response:", response)
        return response
    except Exception as e:
        print(f"Error in sending mail: {e}")
        raise


def build_body_for_costing_mail(data, email_body_content):
    """
    Build the email body for the cost summary mail using the provided data.
    
    Args:
        data (list): A list of dictionaries containing account cost details.
    
    Returns:
        dict: A dictionary containing the text and HTML email templates with populated data.
    """
    try:
        template_paths = {
            "html": "./templates/costing_mail.html",
            "text": "./templates/costing_mail.txt"
        }
        templates = {}

        # Load email templates from files
        for template_type, path in template_paths.items():
            with open(path, "r") as file:
                templates[template_type] = file.read()

        html_rows = ""
        text_rows = ""

        # Populate email templates with data
        for ind, details in enumerate(data):
            # HTML Template
            html_row = f"""
                <tr>
                    <td class="rowCellStyle" align="center">{details['account']}</td>
                    <td class="rowCellStyle" align="center">{details['account_type']}</td>
                    <td class="rowCellStyle" align="center">{details['account_status']}</td>
                    <td class="rowCellStyle" align="center">${details['total']}</td>
                    <td class="rowCellStyle" align="center">{details['top_services']}</td>
                </tr>
            """
            html_rows += html_row

            # Text Template
            text_row = f"{ind + 1}. {details['account']}  -  {details['account_type']})  -  {details['account_status']}  -  ${details['total']}  -  {details['top_services']}\n"
            text_rows += text_row

        # Replace dynamic content in templates
        html_template_resp = templates['html'].replace("#email_body", email_body_content).replace("#dynamic_rows", html_rows)
        txt_template_resp = templates['text'].replace("#email_body", email_body_content).replace("#dynamic_rows", text_rows)

        return {"html_template": html_template_resp, "text_template": txt_template_resp}
    
    except Exception as e:
        print(f"An error occurred while building email body: {str(e)}")
        raise
