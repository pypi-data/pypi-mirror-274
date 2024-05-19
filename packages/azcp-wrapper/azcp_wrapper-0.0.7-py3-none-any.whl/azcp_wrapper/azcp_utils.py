from dataclasses import dataclass, asdict
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)
from typing_extensions import Annotated, Doc
import time
import datetime
from urllib.parse import parse_qs
from azcp_wrapper.logging_config import logger


class LocationType:
    """
    This type is used to specify the location
    type of the object created for transfer
    for the AzCopy command
    """

    SRC = "source"
    DEST = "destination"


class AzRemoteSASLocation:
    """
    Class to create Azure Remote Location with SAS Token
    Returns the remote location url string with the information
    specified while creating the object
    """

    def __init__(
        self,
        storage_account: Annotated[str, Doc("")] = "",
        container: Annotated[str, Doc("")] = "",
        path: Annotated[str, Doc("")] = "",
        use_wildcard: Annotated[bool, Doc("")] = False,
        sas_token: Annotated[str, Doc("")] = "",
        location_type: Annotated[Optional[str], Doc("")] = None,
        blob_or_file: Annotated[str, Doc("")] = "blob",
    ) -> None:
        if len(sas_token) > 0:
            sas_token_expiry_flag = self.is_sas_token_session_expired(token=sas_token)

            if sas_token_expiry_flag == True:
                raise Exception("SAS token is expired")

        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token
        self.use_wildcard = use_wildcard
        self.path = path
        self.location_type = location_type
        self.logger = logger
        self.blob_or_file = blob_or_file.lower() if blob_or_file is not None else "blob"

    def is_sas_token_session_expired(self, token: str) -> bool:
        """
        Checks if the SAS token is expired
        """
        parsed = parse_qs(token.lstrip("?"))

        # se is the query parameter for SessionExpiry field
        session_expiry = parsed.get("se")

        if session_expiry is None:
            raise Exception("Cannot find session expiry parameter in query")

        session_expiry_string = session_expiry[0]

        session_expiry_unix_timestamp = int(
            time.mktime(
                datetime.datetime.strptime(
                    session_expiry_string, "%Y-%m-%dT%H:%M:%SZ"
                ).timetuple()
            )
        )

        current_timestamp = datetime.datetime.now(datetime.timezone.utc)

        current_unix_timestamp = int(time.mktime(current_timestamp.timetuple()))

        if current_unix_timestamp > session_expiry_unix_timestamp:
            return True
        else:
            return False

    def get_resource_uri(self) -> str:
        url = f"https://{self.storage_account}.{self.blob_or_file}.core.windows.net/{self.container}/"
        self.logger.info(f"URL: {url}")
        return url

    def __str__(self) -> str:
        """
        Creates the remote location url with sas token to be used for the final location
        """
        if len(self.sas_token) > 0:
            sas_token_expiry_flag = self.is_sas_token_session_expired(
                token=self.sas_token
            )

            if sas_token_expiry_flag == True:

                raise Exception("SAS token is expired")

        resource_uri = self.get_resource_uri()

        wildcard = ""
        if self.use_wildcard == True:
            wildcard = "*"

        all_command = resource_uri + self.path + wildcard + "?" + self.sas_token
        return all_command


class AzLocalLocation:
    """
    Class to create Local Path for data transfer using Azcopy
    """

    path: str
    use_wildcard: bool
    location_type: Optional[str]

    def __init__(
        self,
        path: Annotated[str, Doc("")] = "",
        use_wildcard: Annotated[bool, Doc("")] = False,
        location_type: Annotated[Optional[str], Doc("")] = None,
    ) -> None:
        self.path = path
        self.use_wildcard = use_wildcard
        self.location_type = location_type

    def __str__(self) -> str:
        wildcard = ""
        if self.use_wildcard == True:
            wildcard = "*"

        return self.path + wildcard


@dataclass
class AzCopyOptions:
    as_subdir: Annotated[
        bool, Doc("Places folder sources as subdirectories under the destination.")
    ] = None
    force_if_read_only: Annotated[
        bool, Doc("Places folder sources as subdirectories under the destination.")
    ] = None
    block_size_mb: Annotated[
        str,
        Doc(
            "Use this block size (specified in MiB) when uploading to Azure Storage, and downloading from Azure Storage."
        ),
    ] = None
    check_length: Annotated[
        bool, Doc("Check the length of a file on the destination after the transfer.")
    ] = None
    dry_run: Annotated[
        str, Doc("Prints the file paths that would be copied by this command.")
    ] = None
    exclude_path: Annotated[
        str,
        Doc(
            "Exclude these paths when copying. This option doesn't support wildcard characters (*). Checks relative path prefix."
        ),
    ] = None
    exclude_pattern: Annotated[
        str,
        Doc(
            "Exclude these files when copying. This option supports wildcard characters (*)."
        ),
    ] = None
    exclude_regex: Annotated[str, Doc("")] = None
    follow_symlinks: Annotated[str, Doc("")] = None
    include_after: Annotated[str, Doc("")] = None
    include_before: Annotated[str, Doc("")] = None
    include_path: Annotated[str, Doc("")] = None
    include_pattern: Annotated[str, Doc("")] = None
    include_regex: Annotated[str, Doc("")] = None
    log_level: Annotated[
        str,
        Doc(
            "Define the log verbosity for the log file, available levels: INFO, WARNING, ERROR, and NONE."
        ),
    ] = None
    metadata: Annotated[
        str, Doc("Upload to Azure Storage with these key-value pairs as metadata.")
    ] = None
    overwrite: Annotated[
        str,
        Doc(
            """# Overwrite the conflicting files and blobs at the destination if this flag is set to true.
                                    # Possible values include 'true', 'false', 'prompt', and 'ifSourceNewer'.
                                    # """
        ),
    ] = "ifSourceNewer"
    put_md5: Annotated[
        bool,
        Doc(
            "Create an MD5 hash of each file, and save the hash as the Content-MD5 property of the destination blob or file."
        ),
    ] = None
    recursive: Annotated[
        bool,
        Doc(
            "Look into subdirectories recursively when uploading from local file system."
        ),
    ] = True

    def get_options_list(self):
        dict_conf = asdict(self)
        config = {k.replace("_", "-"): v for k, v in dict_conf.items() if v != "NULL"}
        cmd_parts = []
        for option, value in config.items():
            if isinstance(value, bool) and value:
                cmd_parts.append(f"--{option}=true")
            elif value is not None:
                cmd_parts.append(f"--{option}={value}")
        return cmd_parts


@dataclass
class AzSyncOptions:

    exclude_path: Annotated[
        str,
        Doc(
            "Exclude these paths when copying. This option doesn't support wildcard characters (*). Checks relative path prefix."
        ),
    ] = None
    put_md5: Annotated[
        bool,
        Doc(
            "Create an MD5 hash of each file, and save the hash as the Content-MD5 property of the destination blob or file."
        ),
    ] = None
    recursive: Annotated[
        bool,
        Doc(
            "Look into subdirectories recursively when uploading from local file system."
        ),
    ] = True

    def get_options_list(self):
        dict_conf = asdict(self)
        config = {k.replace("_", "-"): v for k, v in dict_conf.items() if v != "NULL"}
        cmd_parts = []
        for option, value in config.items():
            if isinstance(value, bool) and value:
                cmd_parts.append(f"--{option}=true")
            elif value is not None:
                cmd_parts.append(f"--{option}={value}")
        return cmd_parts


class AzListJobInfo:
    """
    Created the job info of the Azcopy job executed by the user
    """

    def __init__(
        self,
        file_count: Annotated[int, Doc("")] = 0,
        total_file_size: Annotated[float, Doc("")] = float(0),
        list_files: Annotated[Dict, Doc("")] = dict(),
    ) -> None:
        self.file_count = file_count
        self.total_file_size = total_file_size
        self.logger = logger
        self.list_files = list_files

    def __str__(self) -> str:
        """
        Get a human-readable string representation of the AzCopyJobInfo object.
        """
        self.logger.info(f"AzCopy Job Info List:")
        self.logger.info(f"File count: {self.file_count}")
        self.logger.info(f"Total file size: {self.total_file_size} GB")
        return (
            f"AzCopy Job Info List:\n"
            f"File count: {self.file_count}\n"
            f"Total file size: {self.total_file_size}GB"
        )


class AzCopyJobInfo:
    """
    Created the job info of the Azcopy job executed by the user
    """

    def __init__(
        self,
        percent_complete: Annotated[float, Doc("")] = float(0),
        elapsed_time_minutes: Annotated[float, Doc("")] = float(0),
        error_msg: Annotated[str, Doc("")] = "",
        final_job_status_msg: Annotated[str, Doc("")] = "",
        number_of_file_transfers: Annotated[int, Doc("")] = 0,
        number_of_folder_property_transfers: Annotated[int, Doc("")] = 0,
        total_number_of_transfers: Annotated[int, Doc("")] = 0,
        number_of_transfers_completed: Annotated[int, Doc("")] = 0,
        number_of_transfers_failed: Annotated[int, Doc("")] = 0,
        number_of_file_transfers_skipped: Annotated[int, Doc("")] = 0,
        total_bytes_transferred: Annotated[int, Doc("")] = 0,
        completed: Annotated[bool, Doc("")] = False,
    ) -> None:
        # NOTE: Sometimes, azcopy doesn't return value as 100%
        # even if the entire data is transferred.
        # This might be because if the transfer is completed in between
        # the value sent by azcopy, then azcopy fails to send the final
        # percent value and directly sends the job summary
        self.percent_complete = percent_complete
        self.elapsed_time_minutes = elapsed_time_minutes
        self.error_msg = error_msg
        self.final_job_status_msg = final_job_status_msg
        self.number_of_file_transfers = number_of_file_transfers
        self.number_of_folder_property_transfers = number_of_folder_property_transfers
        self.total_number_of_transfers = total_number_of_transfers
        self.number_of_transfers_completed = number_of_transfers_completed
        self.number_of_transfers_failed = number_of_transfers_failed
        self.number_of_file_transfers_skipped = number_of_file_transfers_skipped
        self.total_bytes_transferred = total_bytes_transferred
        self.completed = completed

    def __str__(self) -> str:
        """
        Get a human-readable string representation of the AzCopyJobInfo object.
        """
        return (
            f"AzCopy Job Info:\n"
            f"Elapsed Time (Minutes): {self.elapsed_time_minutes}\n"
            f"Percent Complete: {self.percent_complete}%\n"
            f"Final Job Status: {self.final_job_status_msg}\n"
            f"Number of File Transfers: {self.number_of_file_transfers}\n"
            f"Transfers Completed: {self.number_of_transfers_completed}\n"
            f"Transfers Failed: {self.number_of_transfers_failed}\n"
            f"Transfers Skipped: {self.number_of_file_transfers_skipped}\n"
            f"Total Bytes Transferred: {self.total_bytes_transferred}"
        )


class AzSyncJobInfo:
    """
    Created the job info of the Azcopy job executed by the user
    """

    def __init__(
        self,
        percent_complete: Annotated[float, Doc("")] = float(0),
        error_msg: Annotated[str, Doc("")] = "",
        files_scanned_at_source: Annotated[int, Doc("")] = 0,
        files_scanned_at_destination: Annotated[int, Doc("")] = 0,
        # elapsed_time_minutes: float = float(0),
        number_of_copy_transfers_for_files: Annotated[int, Doc("")] = 0,
        number_of_copy_transfers_for_folder_properties: Annotated[int, Doc("")] = 0,
        number_of_folder_property_transfers: Annotated[int, Doc("")] = 0,
        total_number_of_copy_transfers: Annotated[int, Doc("")] = 0,
        number_of_copy_transfers_completed: Annotated[int, Doc("")] = 0,
        number_of_copy_transfers_failed: Annotated[int, Doc("")] = 0,
        number_of_deletions_at_destination: Annotated[int, Doc("")] = 0,
        total_number_of_bytes_transferred: Annotated[int, Doc("")] = 0,
        total_number_of_bytes_enumerated: Annotated[int, Doc("")] = 0,
        final_job_status_msg: Annotated[str, Doc("")] = "",
        completed: Annotated[bool, Doc("")] = False,
    ) -> None:
        # NOTE: Sometimes, azcopy doesn't return value as 100%
        # even if the entire data is transferred.
        # This might be because if the transfer is completed in between
        # the value sent by azcopy, then azcopy fails to send the final
        # percent value and directly sends the job summary
        self.percent_complete = percent_complete
        self.error_msg = error_msg
        self.final_job_status_msg = final_job_status_msg
        self.files_scanned_at_source = files_scanned_at_source
        self.files_scanned_at_destination = files_scanned_at_destination
        # self.elapsed_time_minutes = elapsed_time_minutes
        self.number_of_copy_transfers_for_files = number_of_copy_transfers_for_files
        self.number_of_copy_transfers_for_folder_properties = (
            number_of_copy_transfers_for_folder_properties
        )
        self.number_of_folder_property_transfers = number_of_folder_property_transfers
        self.total_number_of_copy_transfers = total_number_of_copy_transfers
        self.number_of_copy_transfers_completed = number_of_copy_transfers_completed
        self.number_of_copy_transfers_failed = number_of_copy_transfers_failed
        self.number_of_deletions_at_destination = number_of_deletions_at_destination
        self.total_number_of_bytes_transferred = total_number_of_bytes_transferred
        self.total_number_of_bytes_enumerated = total_number_of_bytes_enumerated
        self.completed = completed
