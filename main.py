import base64
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

receiver = 'recipients.txt'

def hello_pubsub(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))

    with open(receiver) as file_in:
        lines = []
        for line in file_in:
            # lines.append(line.rstrip('\n').split(','))
            lines.append(line.rstrip('\n'))

    # mlist = ', '.join(lines)

    message = Mail(
        from_email='saeho@popori.info',
        to_emails=lines,
        subject='Sending with SendGrid is Fun',
        html_content=format(name))
        
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
