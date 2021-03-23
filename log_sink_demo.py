# Imports the Google Cloud client library
from google.cloud import logging
from google.cloud import storage
import os

# Instantiates a client
logging_client = logging.Client()
storage_client = storage.Client()

# The name of the log to write to
log_name = 'my-log'
file_name = 'log_filter.txt'
sink_name = 'log_sink_demo'

def update_sink(sink_name, filter_):
    """Changes a sink's filter.

    The filter determines which logs this sink matches and will be exported
    to the destination. For example a filter of 'severity>=INFO' will send
    all logs that have a severity of INFO or greater to the destination.
    See https://cloud.google.com/logging/docs/view/advanced_filters for more
    filter information.
    """

    sink = logging_client.sink(sink_name)

    sink.reload()

    sink.filter_ = filter_
    print("Updated sink {}".format(sink.name))
    sink.update(unique_writer_identity=True)

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
