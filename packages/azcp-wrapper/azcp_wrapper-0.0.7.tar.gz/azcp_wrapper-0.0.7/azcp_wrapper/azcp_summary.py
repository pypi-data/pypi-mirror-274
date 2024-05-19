import re

from azcp_wrapper.azcp_utils import AzCopyJobInfo, AzSyncJobInfo, AzListJobInfo


def get_property_value(key: str, job_summary: str) -> int:
    property_value = 0

    try:
        property_key_match = re.search(
            r"{}: (\d+(\.\d+)?)".format(re.escape(key)), job_summary
        )
        # print(r"{}: (\d+(\.\d+)?)".format(re.escape(key)),property_key_match)
        if property_key_match is not None:

            property_key_text = property_key_match.group()
            property_value_match = re.search(r"(\d+(\.\d+)?)", property_key_text)

            # If the property key text exists in the job summary,
            # the gets the property value
            if property_value_match is not None:
                property_value = str(property_value_match.group())
    except Exception as e:
        print(e)

    return property_value


def get_transfer_list_summary_info(
    job_info: AzListJobInfo, summary: str
) -> AzListJobInfo:
    """
    Extract all properties of Job Info from the Azcopy job summary
    """
    properties_required = [
        "File count",
        "Total file size",
    ]

    for property_key in properties_required:

        # Converting the property key string to attribute form
        property_attribute = property_key.lower().replace(" ", "_")
        property_value = get_property_value(property_key, summary)

        # Set the attribute in job_info object
        setattr(job_info, property_attribute, property_value)
    # Crear una lista para almacenar los datos
    file_data = []

    # Usar una expresión regular para encontrar todos los pares archivo-tamaño
    pattern = re.compile(r"INFO: ([^;]+);  Content Length: ([\d.]+ \w+)")
    matches = pattern.findall(summary)

    # Rellenar la lista con los datos encontrados
    for match in matches:
        file_name, content_length = match
        file_info = {"Archivo": file_name.strip(), "peso": content_length.strip()}
        file_data.append(file_info)

    job_info.list_files = file_data
    return job_info


def get_transfer_copy_summary_info(
    job_info: AzCopyJobInfo, summary: str
) -> AzCopyJobInfo:
    """
    Extract all properties of Job Info from the Azcopy job summary
    """
    properties_required = [
        "Number of File Transfers",
        "Number of Folder Property Transfers",
        "Number of File Transfers",
        "Total Number of Transfers",
        "Number of Transfers Completed",
        "Number of File Transfers Skipped",
        "Number of Transfers Skipped",
    ]

    for property_key in properties_required:

        # Converting the property key string to attribute form
        property_attribute = property_key.lower().replace(" ", "_")
        property_value = get_property_value(property_key, summary)

        # Set the attribute in job_info object
        setattr(job_info, property_attribute, property_value)

    job_info.elapsed_time_minutes = get_property_value(
        "Elapsed Time (Minutes)", summary
    )
    job_info.total_bytes_transferred = get_property_value(
        "Total Number of Bytes Transferred", summary
    )

    return job_info


def get_sync_summary_info(sync_job_info: AzSyncJobInfo, summary: str) -> AzSyncJobInfo:
    """
    Extract all properties of Job Info from the Azcopy job summary
    """

    properties_required = [
        "Files Scanned at Source",
        "Files Scanned at Destination",
        "Number of Copy Transfers for Files",
        "Number of Copy Transfers for Folder Properties",
        "Total Number Of Copy Transfers",
        "Number of Copy Transfers Completed",
        "Number of Copy Transfers Failed",
        "Number of Deletions at Destination",
        "Total Number of Bytes Transferred",
        "Total Number of Bytes Enumerated",
    ]

    for property_key in properties_required:

        # Converting the property key string to attribute form
        property_attribute = (
            property_key.lower().replace(" ", "_").replace("(", "").replace(")", "")
        )
        property_value = get_property_value(property_key, summary)

        # Set the attribute in job_info object
        setattr(sync_job_info, property_attribute, property_value)

    # property_key = "Elapsed Time Minutes"

    # property_key_match = re.search(
    #     r"{}: \d+\.\d+|(?<=angle\s)\d+\n".format(property_key), summary
    # )

    # property_value = 0.0  # type: ignore

    # if property_key_match is not None:

    #     property_key_text = property_key_match.group()
    #     property_value_match = re.search(r"\d+\.\d+|(?<=angle\s)\d+", property_key_text)

    #     # If the property key text exists in the job summary,
    #     # the gets the property value
    #     if property_value_match is not None:
    #         property_value = float(property_value_match.group())  # type: ignore

    # sync_job_info.elapsed_time_minutes = property_value

    return sync_job_info
