import configparser
import pkg_resources
import curses

CONFIG_FILE = pkg_resources.resource_filename('EAACommander', 'settings.ini')

# Function to load settings from the configuration file
def load_settings():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

# Function to save settings to the configuration file
def save_settings(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Helper function to display a message
def display_message(stdscr, message):
    full_message = f"{message}... Press Space to return to the menu."
    stdscr.clear()
    stdscr.addstr(0, 0, full_message)
    stdscr.refresh()
    while stdscr.getch() != ord(' '):
        pass

# Function to update server settings
def update_server_settings(stdscr, config):
    stdscr.clear()
    server_settings = config['Server']
    hostname = server_settings.get('Hostname', 'astro')
    port = server_settings.get('Port', '50000')

    stdscr.addstr(0, 0, f"Current Server Settings:\nHostname: {hostname}\nPort: {port}")
    stdscr.addstr(4, 0, "Do you want to change these settings? (y/n): ")
    stdscr.refresh()

    confirm_choice = stdscr.getch()
    if confirm_choice == ord('y'):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Current Server Settings:\nHostname: {hostname}\nPort: {port}")
        stdscr.addstr(4, 0, "Enter new Hostname (or press Enter to keep current): ")
        curses.echo()
        new_hostname = stdscr.getstr(5, 0, 20).decode('utf-8')
        stdscr.addstr(6, 0, "Enter new Port (or press Enter to keep current): ")
        new_port = stdscr.getstr(7, 0, 20).decode('utf-8')
        curses.noecho()

        # Use the new values if provided, otherwise keep the old ones
        hostname = new_hostname if new_hostname else hostname
        port = new_port if new_port else port

        config['Server']['Hostname'] = hostname
        config['Server']['Port'] = port
        save_settings(config)
        display_message(stdscr, "Server settings updated")
    else:
        display_message(stdscr, "Server settings not changed")

# Function to update camera settings
def update_camera_settings(stdscr, config):
    stdscr.clear()
    camera_settings = config['Camera']
    camera_name = camera_settings.get('CameraName', 'Folder Monitor Camera')
    is_camera_folder_monitor = camera_settings.get('isCameraFolderMonitor', 'True')
    monitor_folder = camera_settings.get('monitorFolder', '')
    folder_camera_path = camera_settings.get('folderCameraPath', '')
    monitor_for_latest = camera_settings.get('monitorForLatest', 'False')

    stdscr.addstr(0, 0, f"Current Camera Settings:\nCameraName: {camera_name}\nisCameraFolderMonitor: {is_camera_folder_monitor}\nmonitorFolder: {monitor_folder}\nfolderCameraPath: {folder_camera_path}\nmonitorForLatest: {monitor_for_latest}")
    stdscr.addstr(6, 0, "Do you want to change these settings? (y/n): ")
    stdscr.refresh()

    confirm_choice = stdscr.getch()
    if confirm_choice == ord('y'):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Current Camera Settings:\nCameraName: {camera_name}\nisCameraFolderMonitor: {is_camera_folder_monitor}\nmonitorFolder: {monitor_folder}\nfolderCameraPath: {folder_camera_path}\nmonitorForLatest: {monitor_for_latest}")
        stdscr.addstr(6, 0, "Enter new CameraName (or press Enter to keep current): ")
        curses.echo()
        new_camera_name = stdscr.getstr(7, 0, 40).decode('utf-8')
        stdscr.addstr(8, 0, "Enter new isCameraFolderMonitor (True/False, or press Enter to keep current): ")
        new_is_camera_folder_monitor = stdscr.getstr(9, 0, 5).decode('utf-8')
        stdscr.addstr(10, 0, "Enter new monitorFolder (or press Enter to keep current): ")
        new_monitor_folder = stdscr.getstr(11, 0, 40).decode('utf-8')
        stdscr.addstr(12, 0, "Enter new folderCameraPath (or press Enter to keep current): ")
        new_folder_camera_path = stdscr.getstr(13, 0, 40).decode('utf-8')
        stdscr.addstr(14, 0, "Enter new monitorForLatest (True/False, or press Enter to keep current): ")
        new_monitor_for_latest = stdscr.getstr(15, 0, 5).decode('utf-8')
        curses.noecho()

        # Use the new values if provided, otherwise keep the old ones
        camera_name = new_camera_name if new_camera_name else camera_name
        is_camera_folder_monitor = new_is_camera_folder_monitor if new_is_camera_folder_monitor else is_camera_folder_monitor
        monitor_folder = new_monitor_folder if new_monitor_folder else monitor_folder
        folder_camera_path = new_folder_camera_path if new_folder_camera_path else folder_camera_path
        monitor_for_latest = new_monitor_for_latest if new_monitor_for_latest else monitor_for_latest

        config['Camera']['CameraName'] = camera_name
        config['Camera']['isCameraFolderMonitor'] = is_camera_folder_monitor
        config['Camera']['monitorFolder'] = monitor_folder
        config['Camera']['folderCameraPath'] = folder_camera_path
        config['Camera']['monitorForLatest'] = monitor_for_latest
        save_settings(config)
        display_message(stdscr, "Camera settings updated")
    else:
        display_message(stdscr, "Camera settings not changed")

# Function to handle settings menu
def settings(stdscr):
    config = load_settings()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Settings Menu\n1. Server settings\n2. Camera settings\n0. Exit to main menu\nEnter choice: ")
        stdscr.refresh()
        
        choice = stdscr.getch()
        stdscr.clear()
        if choice == ord('0'):
            break
        elif choice == ord('1'):
            update_server_settings(stdscr, config)
        elif choice == ord('2'):
            update_camera_settings(stdscr, config)
        else:
            display_message(stdscr, "Invalid choice")