# Imports the Google Cloud client library
from google.cloud import storage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64
import os

# Instantiates a client
storage_client = storage.Client()

bucket_name = 'log_sink_demo'
mail_receiver = 'recipients.txt'

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

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(mail_receiver)
    data = blob.download_as_string()
    data = data.decode('utf-8')
    data = data.splitlines()
    print(data)

    message = Mail(
        from_email='saeho@popori.info',
        to_emails=data,
        subject='[Alert] Audit Logging',
        html_content=format(name))
        
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
