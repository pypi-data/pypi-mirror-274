import re
import os
import warnings

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
from azcp_wrapper.azcp_summary import (
    get_transfer_copy_summary_info,
    get_sync_summary_info,
    get_transfer_list_summary_info,
)

from typing_extensions import Annotated, Doc
from azcp_wrapper.azcp_utils import (
    AzCopyJobInfo,
    AzCopyOptions,
    AzLocalLocation,
    AzRemoteSASLocation,
    AzSyncJobInfo,
    AzSyncOptions,
    AzListJobInfo,
    LocationType,
)

from pathlib import Path

from azcp_wrapper.logging_config import run_name, run_log_directory, logger
from azcp_wrapper.utils.execute_command import execute_command


class AzClient:
    """
    Azcopy client to execute commands for the user
    If azcopy is already installed in the system, then the client will directly use that exe

    For ex. If the azcopy binary file exists in /usr/local/bin/, then client will by default use that file.

    But if the usr wants to use another specific file which is stored in some other location, then they will have to
    specify it while creating the AzClient object
    """

    def __init__(
        self,
        exe_to_use: Annotated[str, Doc("")] = "azcopy",
        process_name: Annotated[Optional[str], Doc("process_name")] = __name__,
        artefact_dir: Annotated[Optional[str], Doc("")] = None,
    ) -> None:
        self.exe_to_use = (
            exe_to_use
            if not (
                Path("~/.azcp/azcopy.exe").expanduser().exists()
                or Path("~/.azcp/azcopy").expanduser().exists()
            )
            else Path("~/.azcp/azcopy").expanduser()
        )
        self.process_name = process_name
        self.artefact_dir = artefact_dir
        self.run_name, self.run_log_directory, self.logger = (
            run_name,
            run_log_directory,
            logger,
        )
        self.logger.info(f"Process Name: {self.process_name}")
        self.logger.info(f"Run name: {self.run_name}")
        self.logger.info(f"Run log directory: {self.run_log_directory}/{self.run_name}")
        self.logger.info(f"Executable to use: {self.exe_to_use}")
        # self.logger.warn([x for x in execute_command(['python','-m', 'pip', '-V'])])

    def List(self, src: Union[AzRemoteSASLocation, AzLocalLocation]) -> AzListJobInfo:
        cmd = [
            self.exe_to_use,
            "ls",
            str(src),
        ] + ["--running-tally"]
        print(cmd)
        summary = ""
        job_info = AzListJobInfo()
        for output_line in execute_command(cmd):
            # print(output_line, end="")
            # if "File count:" in output_line:
            summary += output_line

        job_info = get_transfer_list_summary_info(job_info, summary=summary)
        str(job_info)
        return job_info

    def copy(
        self,
        src: Union[AzRemoteSASLocation, AzLocalLocation],
        dest: Union[AzRemoteSASLocation, AzLocalLocation],
        transfer_options: AzCopyOptions,
    ) -> AzCopyJobInfo:
        """
        Copies that data from source to destionation
        with the transfer options specified
        """
        import re

        # Generating the command to be used for subprocess
        cmd = [
            self.exe_to_use,
            "cp",
            str(src),
            str(dest),
        ] + transfer_options.get_options_list()
        # cmd = ["python", "-V"]
        job_info = AzCopyJobInfo()

        try:
            summary = ""
            # A boolean flag to be set as True when
            # azcopy starts sending summary information
            unlock_summary = False

            for output_line in execute_command(cmd):
                print(output_line, end="")

                # Extracting the percent complete information from the
                # current output line and updating it in the job_info
                if "%" in output_line:
                    percent_expression = r"(?P<percent_complete>\d+\.\d+) %,"
                    transfer_match = re.match(percent_expression, output_line)

                    if transfer_match is not None:
                        transfer_info = transfer_match.groupdict()

                        job_info.percent_complete = float(
                            transfer_info["percent_complete"]
                        )
                # If azcopy has started sending summary then
                # appending it to summary text
                if unlock_summary:
                    summary += output_line

                # Job summary starts with line ->
                # Job {job_id} summary
                if output_line.startswith("Job") and "summary" in output_line:
                    unlock_summary = True

                if "AuthenticationFailed" in output_line:
                    job_info.error_msg = output_line

                if "Final Job Status:" in output_line:
                    job_info.final_job_status_msg = output_line.split(":")[-1].strip()
        except Exception as e:
            # Checking if the error is because of the sas token
            token_expiry_flag = False
            if isinstance(dest, AzRemoteSASLocation):
                token = str(dest.sas_token)
                token_expiry_flag = dest.is_sas_token_session_expired(token)
            elif isinstance(src, AzRemoteSASLocation):
                token = str(src.sas_token)
                token_expiry_flag = src.is_sas_token_session_expired(token)
            else:
                token = ""

            if token_expiry_flag == True:
                job_info.error_msg = "SAS token is expired"
            else:
                job_info.error_msg = str(e)

            job_info.completed = False

        # Get the final job summary info
        job_info = get_transfer_copy_summary_info(job_info, summary)

        if (
            job_info.final_job_status_msg == "Completed"
            or job_info.final_job_status_msg == "CompletedWithSkipped"
        ):
            job_info.completed = True
        elif job_info.number_of_transfers_failed > 0:
            job_info.error_msg += "; Tranfers failed = {}".format(
                job_info.number_of_transfers_failed
            )
            job_info.completed = False
            raise Exception(job_info.error_msg)
        else:
            job_info.error_msg += "; Error while transferring data"
            job_info.completed = False
            raise Exception(job_info.error_msg)

        return job_info

    def sync(
        self,
        src: Union[AzRemoteSASLocation, AzLocalLocation],
        dest: Union[AzRemoteSASLocation, AzLocalLocation],
        transfer_options: AzSyncOptions,
    ) -> AzSyncJobInfo:
        """
        Syncs that data from source to destionation
        with the transfer options specified
        """
        # Generating the command to be used for subprocess
        cmd = [
            self.exe_to_use,
            "sync",
            str(src),
            str(dest),
        ] + transfer_options.get_options_list()

        # Creating AzSyncJobInfo object to store the job info
        job_info = AzSyncJobInfo()

        try:
            summary = ""
            # A boolean flag to be set as True when
            # azcopy starts sending summary information
            unlock_summary = False

            for output_line in execute_command(cmd):
                print(output_line, end="")

                # Extracting the percent complete information from the
                # current output line and updating it in the job_info
                if "%" in output_line:

                    percent_expression = r"(?P<percent_complete>\d+\.\d+) %,"
                    transfer_match = re.match(percent_expression, output_line)

                    if transfer_match is not None:
                        transfer_info = transfer_match.groupdict()

                        job_info.percent_complete = float(
                            transfer_info["percent_complete"]
                        )

                # If azcopy has started sending summary then
                # appending it to summary text
                if unlock_summary:
                    summary += output_line.replace("(", "").replace(")", "")

                # Job summary starts with line ->
                # Job {job_id} summary
                output_line_cleaned = output_line.strip().lower()

                if (
                    output_line_cleaned.startswith("job")
                    and "summary" in output_line_cleaned
                ):
                    unlock_summary = True

                if "AuthenticationFailed" in output_line:
                    job_info.error_msg = output_line

                if "Final Job Status:" in output_line:
                    job_info.final_job_status_msg = output_line.split(":")[-1].strip()

        except Exception as e:
            job_info.completed = False

        # Get the final job summary info
        job_info = get_sync_summary_info(job_info, summary)

        if (
            job_info.final_job_status_msg == "Completed"
            or job_info.final_job_status_msg == "CompletedWithSkipped"
        ):
            job_info.completed = True
        elif job_info.number_of_copy_transfers_failed > 0:
            job_info.error_msg += "; Tranfers failed = {}".format(
                job_info.number_of_copy_transfers_failed
            )
            job_info.completed = False
            raise Exception(job_info.error_msg)
        else:
            job_info.error_msg += "; Error while transferring data"
            job_info.completed = False
            raise Exception(job_info.error_msg)

        return job_info
