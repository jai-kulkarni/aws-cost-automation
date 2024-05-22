from trigger_mail import trigger_mail


def lambda_handler(event, context):
    try:
        # Attempt to send the mail
        mail_response = trigger_mail()
        return mail_response
    except Exception as e:
        # Log the error and return an error message
        error_message = f"An error occurred while triggering the mail: {str(e)}"
        return {
            'statusCode': 500,
            'body': error_message
        }