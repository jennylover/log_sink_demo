# Imports the Google Cloud client library
from google.cloud import logging
from google.cloud import storage
from googleapiclient.discovery import build
import google.auth
import os

# Instantiates a client
logging_client = logging.Client()
storage_client = storage.Client()

# The name of the log to write to
file_name = 'log_filter.txt'
sink_name = 'log_sink_demo'
org_id = os.environ.get('ORG_ID')

def update_sink(name, filter_):
    """Changes a sink's filter.

    The filter determines which logs this sink matches and will be exported
    to the destination. For example a filter of 'severity>=INFO' will send
    all logs that have a severity of INFO or greater to the destination.
    See https://cloud.google.com/logging/docs/view/advanced_filters for more
    filter information.
    """

    credentials, _ = google.auth.default()
    logging_client = build('logging', 'v2', credentials=credentials, cache_discovery=False)

    org_sink_name = 'organizations/{}/sinks/{}'.format(org_id,sink_name)

    sinks = logging_client.sinks().get(sinkName=org_sink_name).execute()
    print(sinks,end='\n\n')

    sink_body={
        'destination' : sinks['destination'],
        'filter' : filter_
        #'filter':filter_.replace('"','\\"')
    }

    sinks_updated = logging_client.sinks().update(sinkName=org_sink_name,body=sink_body).execute()
    print(sinks_updated,end='\n\n')

def hello_gcs(event, context):
     """Background Cloud Function to be triggered by Cloud Storage.
          This generic function logs relevant data when a file is changed.

     Args:
          event (dict):  The dictionary with data specific to this type of event.
                         The `data` field contains a description of the event in
                         the Cloud Storage `object` format described here:
                         https://cloud.google.com/storage/docs/json_api/v1/objects#resource
          context (google.cloud.functions.Context): Metadata of triggering event.
     Returns:
          None; the output is written to Stackdriver Logging
     """

     if event['name'] == file_name:
          bucket = storage_client.get_bucket(event['bucket'])
          blob = bucket.get_blob(event['name'])
          data = blob.download_as_string()
          data = data.decode('utf-8')
          data = data.replace("\n", " ")
          # data = data.replace('"', '\\"')
          update_sink(sink_name, data)
     else:
          print('go away!')
