import textract
import os.path
from google.cloud import storage

storage_client = storage.Client(project="ndis291100")

#project_id = os.environ["GCP_PROJECT"]


#[START pdf_extraction_of_text]
def extract_pdf(bucketname, filename):
    print("Looking for text in image {}".format(filename))
    bucket = storage_client.get_bucket(bucketname)
    text = textract.process(filename)
    print("Fulltext:" + text)
    # decode content from bytes to string
    content = text.decode('cp1252')
    save_result(content, filename)
#[END pdf_extraction_of_text]
#[START save_result]
def save_result(text, filename):
    bucket_name = os.environ["RESULT_BUCKET"]
    result_filename = "{}.txt".format(filename)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(result_filename)
    print("Saving result to {} in bucket {}.".format(result_filename, bucket_name))
    blob.upload_from_string(text)
    print("File saved.")
#[END save_result]
#[START Save_PDF_File_Name_from_trigger]
def process_pdf(file, context):
    """Cloud Function triggered by Cloud Storage when a file is changed.
    Args:
        file (dict): Metadata of the changed file, provided by the triggering
                                 Cloud Storage event.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to stdout and Stackdriver Logging
    """
    bucketname = validate_message(file, "bucket")
    filename = validate_message(file, "name")

    extract_pdf(bucketname, filename)

    print("File {} processed.".format(file["name"]))
#[START Save_PDF_File_Name_from_trigger]
# [START message_validatation_helper]
def validate_message(message, param):
    var = message.get(param)
    if not var:
        raise ValueError(
            "{} is not provided. Make sure you have \
                          property {} in the request".format(
                param, param
            )
        )
    return var
# [END message_validatation_helper]
