import pyautogui
import pygetwindow as gw
import time
import sys

ASA_SEARCH_TERMS = ('ArkAscended', 'ARK: Survival Ascended')
ACTIVATE_WAIT = 1.5

COMMANDS = [
    'r.VolumetricCloud 0',
    'r.VolumetricFog 0',
    'r.Water.SingleLayer.Reflection 0',
    'r.DistanceFieldShadowing 1',
    'grass.sizeScale .33',
]

def find_asa_window(search_terms):
    all_windows = [w for w in gw.getAllWindows() if w.title.strip()]

    for term in search_terms:
        matches = [w for w in all_windows if term.lower() in w.title.lower()]
        if matches:
            print(f"Found {len(matches)} window(s) matching '{term}':")
            for w in matches:
                print(f"  '{w.title}'")
            return matches[0]

    print("No matching window found. All open windows:")
    for w in sorted(all_windows, key=lambda w: w.title.lower()):
        print(f"  '{w.title}'")
    return None


def activate_window(window) -> bool:
    title = window.title
    try:
        if window.isMinimized:
            window.restore()
            time.sleep(0.5)

        window.activate()
        time.sleep(ACTIVATE_WAIT)

        active = gw.getActiveWindow()
        if active and title in active.title:
            print(f"Window '{title}' is now active.")
            return True

        active_title = active.title if active else "None"
        print("WARNING: Activation may have failed.")
        print(f"  Expected : '{title}'")
        print(f"  Active is: '{active_title}'")
        print("  Click the ARK window manually, then press Enter to continue...")
        input()
        return True

    except Exception as e:
        print(f"Error activating window: {e}")
        return False

asa_window = find_asa_window(ASA_SEARCH_TERMS)

if asa_window is None:
    print("Make sure ARK: Survival Ascended is running and try again.")
    sys.exit(1)

if not activate_window(asa_window):
    print("Could not activate the ARK window. Exiting.")
    sys.exit(1)

# Open console
pyautogui.press('`')
time.sleep(0.2)

for cmd in COMMANDS:
    pyautogui.write(cmd, interval=0.05)
    pyautogui.press('enter')
    print(f"{cmd}  ✓")

print("\nAll commands entered successfully!")
print("Enjoy your time in the ARK!")
sys.exit(0)