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
from enum import Enum

from aurora_cli.src.support.dependency import check_dependency_apt


# Application texts
class AppTexts(Enum):
    @staticmethod
    def error_dependency_sshpass():
        return ('<red>Application</red> "sshpass" <red>not found, install it.</red>'
                + ('\nTry: sudo apt install sshpass' if check_dependency_apt() else ''))

    @staticmethod
    def error_dependency_git():
        return ('<red>Application</red> "git" <red>not found, install it.</red>'
                + ('\nTry: sudo apt install git' if check_dependency_apt() else ''))

    @staticmethod
    def error_dependency_sudo():
        return ('<red>Application</red> "sudo" <red>not found, install it.</red>'
                + ('\nTry: sudo apt install sudo' if check_dependency_apt() else ''))

    @staticmethod
    def error_dependency_ffmpeg():
        return ('<red>Application</red> "ffmpeg" <red>not found, install it.</red>'
                + ('\nTry: sudo apt install ffmpeg' if check_dependency_apt() else ''))

    @staticmethod
    def error_dependency_vscode():
        return ('<red>Application</red> "vscode" <red>not found, install it.</red>'
                + ('\nTry: https://code.visualstudio.com/download' if check_dependency_apt() else ''))

    @staticmethod
    def error_dependency_gdb_multiarch():
        return ('<red>Application</red> "gdb-multiarch" <red>not found, install it.</red>'
                + ('\nTry: sudo apt install gdb-multiarch' if check_dependency_apt() else ''))

    @staticmethod
    def error_dependency_clang_format():
        return ('<red>Application</red> "clang-format" <red>not found, install it.</red>'
                + ('\nTry: sudo apt install clang-format' if check_dependency_apt() else ''))

    @staticmethod
    def error_connect_internet():
        return '<red>Internet connection error. Check the connection.</red>'

    @staticmethod
    def error_find_ssh_key(path_key: str):
        return ('<red>Public-key authentication is required to connect to the debug</red>.\n'
                '<red>Key not found:</red> {path}').format(path=path_key)

    @staticmethod
    def devices_not_found():
        return '<red>Devices not found.</red>'

    @staticmethod
    def device_active(ip: str):
        return '<green>Devices</green> "{}" <green>is active.</green>'.format(ip)

    @staticmethod
    def device_not_active(ip: str):
        return '<red>Devices</red> "{}" <red>is not active.</red>'.format(ip)

    @staticmethod
    def select_index():
        return 'Select index'

    @staticmethod
    def select_device(array: []):
        if len(array) > 1:
            return 'Select device index'

    @staticmethod
    def select_versions(array: []):
        if len(array) > 1:
            return 'Select version index'

    @staticmethod
    def select_keys(array: []):
        if len(array) > 1:
            return 'Select keys index'

    @staticmethod
    def select_target(array: []):
        if len(array) > 1:
            return 'Select target index'

    @staticmethod
    def array_indexes(array: []):
        if not array or len(array) == 1:
            return None
        list_numbered = ['{}: {}'.format(index + 1, str(item)) for index, item in enumerate(array)]
        list_format = [(item[:-1] if item.endswith('/') else item) for item in list_numbered]
        return '\n'.join(list_format)

    @staticmethod
    def select_index_error(index: int):
        return '<red>Index</red> "{}" <red>is not a valid.</red>'.format(index)

    @staticmethod
    def select_index_success(index: int):
        return 'Select index: {}'.format(index)

    @staticmethod
    def command_execute_error(command: str):
        return (('<red>Command was executed with an error:</red> {}\n<cyan>'
                 'For detailed reporting, use the</cyan> --verbose (-v) <cyan>flag.</cyan>')
                .format(' {}\n   '.format('\\').join(command.split(' '))))

    @staticmethod
    def command_execute_success(command: str):
        return (('<green>Command was executed without errors:</green>\n{}\n<cyan>'
                 'For detailed reporting, use the</cyan> --verbose (-v) <cyan>flag.</cyan>')
                .format(' {}\n   '.format('\\').join(command.split(' '))))

    @staticmethod
    def command_execute_error_short():
        return (('<red>The command was completed with an error.</red>'
                 '\n<cyan>For detailed reporting, use the</cyan> --verbose (-v) <cyan>flag.</cyan>'))

    @staticmethod
    def command_execute_success_short():
        return (('<green>The command completed successfully.</green>'
                 '\n<cyan>For detailed reporting, use the</cyan> --verbose (-v) <cyan>flag.</cyan>'))

    @staticmethod
    def file_not_found(path: str):
        return '<red>File path not found:</red> {}'.format(path)

    @staticmethod
    def dir_not_found(path: str):
        return '<red>Directory path not found:</red> {}'.format(path)

    @staticmethod
    def already_exists(name: str):
        return '<blue>Already exists:</blue> {}'.format(name)

    @staticmethod
    def download(name: str):
        return '<blue>Download:</blue> {}'.format(name)

    @staticmethod
    def file_error_extension(
            extension: str,
            path: str
    ):
        return '<red>File not have</red> <blue>".{}"</blue> <red>extension:</red> {}'.format(extension, path)

    @staticmethod
    def file_no_one_not_found():
        return '<red>No files found!</red>'.format()

    @staticmethod
    def start_upload(path: str):
        return '<blue>Start upload:</blue> {}'.format(path)

    @staticmethod
    def upload_success():
        return '<green>Upload successful.</green>'

    @staticmethod
    def download_success():
        return '<green>Download successful.</green>'

    @staticmethod
    def loading():
        return '<blue>Loading...</blue>'

    @staticmethod
    def preparing():
        return '<blue>Preparing...</blue>'

    @staticmethod
    def package_install_loading():
        return '<blue>Install package loading...</blue>'

    @staticmethod
    def loading_server():
        return '<blue>Waiting for a response from the server...</blue>'

    @staticmethod
    def exec_pc_command_error(exception: str):
        return '<red>An error occurred while executing the command on the PC:</red>\n{}'.format(exception)

    @staticmethod
    def dir_already_exist(path: str):
        return '<red>Folder already exist</red>: {}'.format(path)

    @staticmethod
    def vm_already_running():
        return '<yellow>Virtual machine is already running.</yellow>'

    @staticmethod
    def vm_is_not_running():
        return ('<yellow>Virtual machine is not running.</yellow>\n'
                '<cyan>To run, run the command:</cyan> "aurora-cli emulator start"')

    @staticmethod
    def vm_not_found():
        return '<red>Virtual machine not found.</red>'

    @staticmethod
    def flutter_not_found():
        return '<red>Flutter installed not found.</red>'

    @staticmethod
    def configuration_clang_format_not_found():
        return '<red>The clang-format configuration file is required.</red>'

    @staticmethod
    def flutter_error_read_json():
        return '<red>Error read json file.</red>'

    @staticmethod
    def flutter_platform_specific_plugins(plugins: []):
        if not plugins or len(plugins) == 1:
            return None
        return '<blue>Platform-specific plugins:</blue>\n{}'.format('\n'.join(plugins))

    @staticmethod
    def flutter_platform_not_specific_plugins(plugins: []):
        if not plugins or len(plugins) == 1:
            return None
        return '<blue>Non platform-specific plugins:</blue>\n{}'.format('\n'.join(plugins))

    @staticmethod
    def flutter_platform_specific_plugins_has_aurora(plugins: []):
        if not plugins or len(plugins) == 1:
            return None
        return '<blue>Platform-specific plugins that are in Aurora OS:</blue>\n{}'.format('\n'.join(plugins))

    @staticmethod
    def flutter_project_read_pubspec_error():
        return '<red>Error reading project pubspec file.</red>'

    @staticmethod
    def flutter_plugins_save_as_pdf_success(path: str):
        return '<green>Output save as PDF successfully:</green> {}'.format(path)

    @staticmethod
    def workdir_not_found():
        return '<red>Directory workdir not found. Update the configuration file.</red>'

    @staticmethod
    def vm_error_connect():
        return '<red>Error connect to virtual machine.</red>'

    @staticmethod
    def conf_confirm():
        return 'Create default configuration file?'

    @staticmethod
    def conf_created_success(path: str):
        return '<green>Configuration file created successfully:</green> {}'.format(path)

    @staticmethod
    def conf_download_keys_confirm():
        return 'Download public keys for sign RPM packages?'

    @staticmethod
    def conf_download_clang_format_conf_confirm():
        return 'Download clang-format configuration file?'

    @staticmethod
    def conf_download_keys_success(path: str):
        return '<green>Public key pairs download successfully:</green> {}'.format(path)

    @staticmethod
    def flutter_versions(versions: []):
        return 'Available versions Flutter SDK:\n{}'.format('\n'.join(versions))

    @staticmethod
    def flutter_installed_versions(versions: []):
        return 'Found the installed Flutter SDK:\n{}'.format('\n'.join(versions))

    @staticmethod
    def flutter_installed_not_found():
        return 'Flutter SDK not found.'

    @staticmethod
    def flutter_remove_confirm(path: str):
        return 'Do you want to continue?\nThe path folder will be deleted: {}'.format(path)

    @staticmethod
    def flutter_remove_success():
        return '<green>Remove Flutter SDK successfully!</green>'

    @staticmethod
    def flutter_install_success(flutter_root_path: str, tag: str):
        return """
<green>Install Flutter SDK "{tag}" successfully!</green>

Add alias to ~/.bashrc for convenience:

    <blue>alias flutter-aurora={flutter_root_path}/flutter-{tag}/bin/flutter</blue>

After that run the command:

    <blue>source $HOME/.bashrc</blue>

You can check the installation with the command:

    <blue>flutter-aurora --version</blue>

Good luck!""".format(flutter_root_path=flutter_root_path, tag=tag)

    @staticmethod
    def sdk_versions(versions: []):
        return 'Available versions Aurora SDK:\n{}'.format('\n'.join(versions))

    @staticmethod
    def sdk_already_exist(version: str):
        return '<red>Aurora SDK already exist</red>: {}'.format(version)

    @staticmethod
    def sdk_not_found():
        return '<red>Aurora SDK not found.</red>'

    @staticmethod
    def sdk_version(version):
        return 'Aurora SDK: {}'.format(version)

    @staticmethod
    def psdk_versions(versions: []):
        return 'Available versions Aurora Platform SDK:\n{}'.format('\n'.join(versions))

    @staticmethod
    def psdk_not_found():
        return '<red>Aurora Platform SDK not found.</red>'

    @staticmethod
    def psdk_installed_versions(versions: []):
        return 'Found the installed Aurora Platform SDK: \n{}'.format('\n'.join(versions))

    @staticmethod
    def psdk_not_found_chroot():
        return '<red>Chroot tar.bz2 not found.</red>'

    @staticmethod
    def psdk_not_found_tooling():
        return '<red>Tooling tar.bz2 not found.</red>'

    @staticmethod
    def psdk_start_install_chroot():
        return '<blue>Install chroot</blue>'

    @staticmethod
    def psdk_start_install_tooling():
        return '<blue>Install tooling</blue>'

    @staticmethod
    def psdk_start_install_target(arch):
        return '<blue>Install target:</blue> {}'.format(arch)

    @staticmethod
    def psdk_install_success(psdk_path: str, version: str):
        return """
<green>Install Aurora Platform SDK "{version}" successfully!</green>

You should update your ~/.bashrc to include export:

    <blue>export PSDK_DIR={psdk_path}/sdks/aurora_psdk</blue>

Add alias for convenience:

    <blue>alias aurora_psdk={psdk_path}/sdks/aurora_psdk/sdk-chroot</blue>

After that run the command:

    <blue>source $HOME/.bashrc</blue>

You can check the installation with the command:

    <blue>aurora_psdk sdk-assistant list</blue>

The files have been downloaded to the ~/Downloads folder, if you no longer need them, delete them.

Good luck!""".format(version=version, psdk_path=psdk_path)

    @staticmethod
    def psdk_installed_not_found():
        return 'Aurora Platform SDK not found.'

    @staticmethod
    def psdk_installed_targets_not_found():
        return 'Targets not found.'

    @staticmethod
    def psdk_targets_list(targets: []):
        return 'Available targets Aurora Platform SDK:\n{}'.format('\n'.join(targets))

    @staticmethod
    def psdk_folder_psdk_not_found(path: str):
        return '<red>Expected directory with Aurora Platform SDK not found:</red> {}'.format(path)

    @staticmethod
    def psdk_remove_success():
        return '<green>Remove Aurora Platform SDK successfully!</green>'

    @staticmethod
    def psdk_clear_sudoers_success(folder_name: str):
        return '<green>Clear sudoers for</green> "{}" <green>successfully!</green>'.format(folder_name)

    @staticmethod
    def psdk_added_sudoers_success(folder_name: str):
        return '<green>Added sudoers for</green> "{}" <green>successfully!</green>'.format(folder_name)

    @staticmethod
    def psdk_remove_confirm(path: str):
        return 'Do you want to continue?\nThe path folder will be deleted: {}'.format(path)

    @staticmethod
    def psdk_sign_keys_not_found():
        return ('<red>Signing keys not found.</red>\n'
                '<cyan>Check your config file:</cyan> "~/.aurora-cli/configuration.yaml"')

    @staticmethod
    def psdk_sign(path: str):
        return '<blue>Package signature:</blue> {}'.format(path)

    @staticmethod
    def psdk_validate(path: str):
        return '<blue>Package validate:</blue> {}'.format(path)

    @staticmethod
    def psdk_target_package_install(path: str):
        return '<blue>Package install to target:</blue> {}'.format(path)

    @staticmethod
    def psdk_target_package_remove(package_name: str):
        return '<blue>Package remove from target:</blue> {}'.format(package_name)

    @staticmethod
    def psdk_target_package_search(package_name: str):
        return '<blue>Package search from target:</blue> {}'.format(package_name)

    @staticmethod
    def psdk_target_package_not_found():
        return '<yellow>Package not found.</yellow>'

    @staticmethod
    def psdk_sudoers_exist_error():
        return '<yellow>Sudoers already added.</yellow>'

    @staticmethod
    def psdk_sudoers_not_exist_error():
        return '<yellow>Sudoers not exist.</yellow>'

    @staticmethod
    def psdk_remove_snapshot(target: str):
        return '<blue>Cleaning</blue> "{}" <blue>snapshot...</blue>'.format(target)

    @staticmethod
    def file_error_size(path: str):
        return '<red>Do not match size file</red>: {}'.format(path)

    @staticmethod
    def file_error_size_common():
        return '<red>An error was found in the files, delete it and try downloading again.</red>'

    @staticmethod
    def emulator_screenshot_error():
        return (('<red>Failed to take screenshot.</red>'
                 '\n<cyan>For detailed reporting, use the</cyan> --verbose (-v) <cyan>flag.</cyan>'))

    @staticmethod
    def emulator_screenshot_success(path: str):
        return '<green>Screenshot taken successfully:</green> {}'.format(path)

    @staticmethod
    def emulator_video_record_start():
        return '<blue>Video recording started...</blue>'

    @staticmethod
    def emulator_video_record_convert():
        return '<blue>Video convert started...</blue>'

    @staticmethod
    def emulator_video_record_prompt():
        return 'Press to stop recording'

    @staticmethod
    def emulator_video_record_start_error():
        return (('<red>Failed video recording started.</red>'
                 '\n<cyan>For detailed reporting, use the</cyan> --verbose (-v) <cyan>flag.</cyan>'))

    @staticmethod
    def emulator_video_record_success(path: str):
        return '<green>Recording completed successfully:</green> {}'.format(path)

    @staticmethod
    def debug_install_vs_extension(ext: str):
        return '<blue>Installing extension:</blue> {}'.format(ext)

    @staticmethod
    def debug_is_not_flutter_aurora_project():
        return '<red>You must run debug in the flutter application for Aurora OS.</red>'

    @staticmethod
    def debug_error_launch_bin():
        return '<red>No application found to launch. Install the debug version before starting.</red>'

    @staticmethod
    def debug_error_launch_debug_app():
        return '<red>The application cannot get the debug link. Install the debug version before starting.</red>'

    @staticmethod
    def debug_configure_confirm(file_name: str):
        return 'File {} will be overwritten, continue?'.format(file_name)

    @staticmethod
    def flutter_project_read_spec_error():
        return '<red>Error reading project spec file.</red>'

    @staticmethod
    def flutter_build_script_confirm():
        return 'File build.sh will be overwritten, continue?'

    @staticmethod
    def flutter_build_script_add_success(path: str):
        return ('<green>Script has been successfully added:</green> {}'
                '\n<cyan>It requires additional manual configuration.</cyan>').format(path)

    @staticmethod
    def error_size_image_icon(width: int, height: int):
        return '<red>Minimum icon size {}x{}.</red>'.format(width, height)

    @staticmethod
    def flutter_icons_create_success(path: str):
        return '<green>Create icons successfully:</green> {}'.format(path)

    @staticmethod
    def confirm_image_size():
        return 'The image\'s width and height are not equal, continue?'

    @staticmethod
    def end_format(count_files: int, time_end: str):
        return 'Formatted {count_f} files in {time} seconds.'.format(count_f=count_files, time=time_end)

    @staticmethod
    def run_clang_format(path: str):
        return '<blue>Format</blue> <red>C++</red> <blue>files folder:</blue> {}'.format(path)

    @staticmethod
    def run_dart_format(path: str):
        return '<blue>Format</blue> <green>Dart</green> <blue>files folder:</blue> {}'.format(path)
