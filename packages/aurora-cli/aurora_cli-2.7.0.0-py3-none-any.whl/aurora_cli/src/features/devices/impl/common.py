"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os

from paramiko.client import SSHClient

from aurora_cli.src.support.helper import get_path_files
from aurora_cli.src.support.output import VerboseType, echo_stderr, echo_line, echo_stdout
from aurora_cli.src.support.ssh import ssh_client_exec_command, upload_file_sftp
from aurora_cli.src.support.texts import AppTexts


# Execute the command on the device
def common_command(
        client: SSHClient,
        execute: str,
        verbose: VerboseType
):
    # Execute command
    ssh_client_exec_command(client, execute, verbose, ['^bash.+'])

    # Close ssh client
    client.close()


# Run package on device in container
def common_run(
        client: SSHClient,
        package: str,
        verbose: VerboseType
):
    # Exec command
    execute = 'invoker --type=qt5 {package}'.format(package=package)

    # Execute command
    ssh_client_exec_command(client, execute, verbose, ['.+died.+'])

    # Close ssh client
    client.close()


# Install RPM package on device
def common_install(
        client: SSHClient,
        path: [],
        data: {},
        is_apm: bool,
        verbose: VerboseType
):
    # Read paths
    paths = get_path_files(path, extension='rpm')

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    # @todo old version 5.0 use pkcon - I'll temporarily add a flag until everyone is reflashed
    # Check version Aurora OS
    # is_apm = False
    # _, ssh_stdout, _ = client.exec_command('version')
    # for value in iter(ssh_stdout.readline, ""):
    #     print(str(value).strip())
    #     is_apm = 'Aurora 5' in str(value).strip()

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.start_upload(path))
        if upload_file_sftp(client, upload_path, path):
            # Get file name
            file_name = os.path.basename(path)
            # Exec command
            if is_apm:
                prompt = "{'ShowPrompt': <false>}"
                execute = (f'gdbus call --system '
                           f'--dest ru.omp.APM '
                           f'--object-path /ru/omp/APM '
                           f'--method ru.omp.APM.Install '
                           f'"{upload_path}/{file_name}" '
                           f'"{prompt}"')
            else:
                if data:
                    execute = 'echo {} | {} {upload_path}/{file_name}'.format(
                        data['devel-su'],
                        'devel-su pkcon -y install-local',
                        upload_path=upload_path,
                        file_name=file_name
                    )
                else:
                    execute = '{} {upload_path}/{file_name}'.format(
                        'pkcon -y install-local',
                        upload_path=upload_path,
                        file_name=file_name
                    )
            echo_line()
            if verbose != VerboseType.verbose:
                echo_stdout(AppTexts.package_install_loading())
            # Execute command
            ssh_client_exec_command(client, execute, verbose, ['^error.+', '.+error.+'])

    # Close ssh client
    client.close()


# Upload file to ~/Download directory device
def common_upload(
        client: SSHClient,
        path: [],
):
    # Read paths
    paths = get_path_files(path)

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.start_upload(path))
        upload_file_sftp(client, upload_path, path)

    # Close ssh client
    client.close()
