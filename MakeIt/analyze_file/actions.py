import logging
import os
import decouple
import io
import json
import zipfile
import tempfile

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from google.cloud import videointelligence

from file_upload_router.actions import download_file_from_bucket


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def extract_text_from_pdf(filename, extension, username):
    file_content = download_file_from_bucket(filename, extension, username)

    if file_content is None:
        logging.error("Failed to download file")
        return None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_name = temp_file.name
            temp_file.write(file_content)
            temp_file.flush()

        credentials = Credentials.service_principal_credentials_builder() \
            .with_client_id(decouple.config('ADOBE_CLIENT_ID')) \
            .with_client_secret(decouple.config('ADOBE_CLIENT_SECRET')) \
            .build()

        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        source = FileRef.create_from_local_file(temp_file_name)
        extract_pdf_operation.set_input(source)

        extract_pdf_options = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation
        result = extract_pdf_operation.execute(execution_context)

        # After execution, call the function to process the result in memory
        result = process_extracted_pdf_result_in_memory(result)

        logging.info("PDF text extraction and processing successful")

        return result

    except (ServiceApiException, ServiceUsageException, SdkException) as e:
        logging.exception("Exception encountered while executing operation: {}".format(e))
    finally:
        # Ensure the temporary file is cleaned up in case of success or failure
        if 'temp_file_name' in locals():
            os.remove(temp_file_name)


def process_extracted_pdf_result_in_memory(result):
    # Temporarily save the result file to read it into memory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "result.zip")
        result.save_as(temp_file_path)

        # Ensure all file operations are done within this block
        with open(temp_file_path, 'rb') as file:
            zip_data_in_memory = io.BytesIO(file.read())

        with zipfile.ZipFile(zip_data_in_memory) as zip_in_memory:
            zip_file_names = zip_in_memory.namelist()
            for file_name in zip_file_names:
                with zip_in_memory.open(file_name) as file_in_zip:
                    file_content = file_in_zip.read()
                    try:
                        # Assuming JSON content for demonstration; adjust as necessary.
                        data = json.loads(file_content)
                        return extract_text_from_json_from_pdf(data)
                    except json.JSONDecodeError as e:
                        print(f"Could not decode JSON from {file_name}: {e}")


def extract_text_from_json_from_pdf(json_data):
    result = []

    for element in json_data["elements"]:
        if element.get("Text"):
            result.append(element.get("Text"))

    return result


def video_detect_text(video_file):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    video_context = videointelligence.VideoContext()

    # Since video_file is an UploadedFile object, you can read its content directly
    input_content = video_file.read()

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": input_content,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=300)
    annotation_result = result.annotation_results[0]

    # Preparing the response data
    response_data = {"text_annotations": []}
    for text_annotation in annotation_result.text_annotations:
        text_data = {"text": text_annotation.text, "segments": []}
        for segment in text_annotation.segments:
            start_time = segment.segment.start_time_offset
            end_time = segment.segment.end_time_offset
            segment_data = {
                "start_time": start_time.seconds + start_time.microseconds * 1e-6,
                "end_time": end_time.seconds + end_time.microseconds * 1e-6,
                "confidence": segment.confidence,
            }
            text_data["segments"].append(segment_data)
        response_data["text_annotations"].append(text_data)

    return response_data
