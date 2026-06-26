from pypresence import Presence
import time
import win32gui


# NOTE:
#     Copy this into Steam launch option:
#         "C:\...\launch-wrapper.bat" %command%"
#     Replace '...' with file path for the 'launch-wrapper.bat' file.


APP_ID = "1511742323325927617"
RPC = Presence(APP_ID)
RPC.connect()
GODOT = "Godot Engine"

start_timer = int(time.time())

current_window_title = "Godot Engine - Project Manager"

rpc_details = "Project Manager"
rpc_state = "Idle"

project_name = ""
active_scene = ""

running = True


def main():
    try:
        print("RPC connected.")

        while running:
            RPC.update(
                details=rpc_details,
                state=rpc_state,
                start=start_timer,
                large_text=GODOT,
                small_text=GODOT
            )
            time.sleep(5)

            check_for_update()
    except KeyboardInterrupt:
        print("Shutting down RPC...")
    finally:
        RPC.clear()
        RPC.close()
        print("RPC disconnected.")


def find_window_id(hwnd, windows):
    title = win32gui.GetWindowText(hwnd)

    if GODOT in title:
        windows.append(hwnd)
        windows.append(title)


def check_for_update():
    global running
    global current_window_title

    windows = []

    win32gui.EnumWindows(find_window_id, windows)

    if windows:
        current_window_title = win32gui.GetWindowText(windows[0])
    else:
        running = False
        return

    update_active_scene()


def update_active_scene():
    global rpc_details
    global rpc_state
    global project_name
    global active_scene

    words = current_window_title.split(" - ")

    if len(words) > 2:
        project_name = words[1]
        rpc_details = project_name
        if active_scene != words[0]:
            active_scene = words[0]
            rpc_state = f"Editing {active_scene}"
            print("RPC updated.")


if __name__ == "__main__":
    main()
