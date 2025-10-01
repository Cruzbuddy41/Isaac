import curses
import time
from classes_we_use import HR8825
STEP_DELAY = 0.0005
DEFAULT_STEPS = 15
def controller():
    def _run(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(50)
        Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        try:
            Motor1.SetMicroStep('hardward', '1/16step')
            Motor2.SetMicroStep('hardward', '1/16step')
            steps_setting = DEFAULT_STEPS
            remaining_steps = 0
            batch_direction = None      # 'forward' or 'backward' for current batch
            continuous_mode = None      # 'forward' or 'backward' or None
            paused = False
            status_msg = "Ready."
            time.sleep(5)
            def single_step(direction: str):
                if direction == 'forward':
                    Motor2.TurnStep(Dir='forward', steps=1, stepdelay=STEP_DELAY)
                    Motor1.TurnStep(Dir='backward', steps=1, stepdelay=STEP_DELAY)
                else:
                    Motor2.TurnStep(Dir='backward', steps=1, stepdelay=STEP_DELAY)
                    Motor1.TurnStep(Dir='forward', steps=1, stepdelay=STEP_DELAY)
            def draw():
                stdscr.erase()
                stdscr.addstr(0, 0, "Stepper Remote Control (HR8825)")
                stdscr.addstr(1, 0, "--------------------------------")
                stdscr.addstr(2, 0, f"Steps setting: {steps_setting}")
                stdscr.addstr(3, 0, f"Remaining steps (batch): {remaining_steps}")
                stdscr.addstr(4, 0, f"Batch direction: {batch_direction or '-'}")
                stdscr.addstr(5, 0, f"Continuous mode: {continuous_mode or 'off'}")
                stdscr.addstr(6, 0, f"Paused: {paused}")
                stdscr.addstr(8, 0,  "Keys: f/b batch | c/v continuous | p pause | s stop | +/- or [/]= steps | h help | q quit")
                stdscr.addstr(10, 0, f"Status: {status_msg}")
                stdscr.refresh()
            help_popup_shown = False
            while True:
                draw()
                # Drive motion
                if not paused:
                    if remaining_steps > 0 and batch_direction:
                        single_step(batch_direction)
                        remaining_steps -= 1
                        if remaining_steps == 0:
                            batch_direction = None
                            status_msg = "Batch complete."
                    elif continuous_mode in ('forward', 'backward'):
                        single_step(continuous_mode)
                # Read key
                ch = stdscr.getch()
                if ch == -1:
                    continue
                # Normalize to char if possible
                try:
                    key = chr(ch)
                except ValueError:
                    key = ''
                if key in ('q', 'Q'):
                    status_msg = "Quitting…"
                    break
                elif key in ('f', 'F'):
                    batch_direction = 'forward'
                    remaining_steps = steps_setting
                    continuous_mode = None
                    status_msg = f"Batch forward: {steps_setting} steps."
                elif key in ('b', 'B'):
                    batch_direction = 'backward'
                    remaining_steps = steps_setting
                    continuous_mode = None
                    status_msg = f"Batch backward: {steps_setting} steps."
                elif key in ('c', 'C'):
                    continuous_mode = 'forward'
                    batch_direction = None
                    remaining_steps = 0
                    status_msg = "Continuous FORWARD. Press 'p' to pause or 's' to stop."
                elif key in ('v', 'V'):
                    continuous_mode = 'backward'
                    batch_direction = None
                    remaining_steps = 0
                    status_msg = "Continuous BACKWARD. Press 'p' to pause or 's' to stop."
                elif key in ('p', 'P'):
                    paused = not paused
                    status_msg = "Paused." if paused else "Resumed."
                elif key in ('s', 'S'):
                    # stop any motion but keep settings
                    remaining_steps = 0
                    batch_direction = None
                    continuous_mode = None
                    status_msg = "Motion stopped."
                elif key in ('+',):
                    steps_setting = max(1, steps_setting + 10)
                    status_msg = f"Steps setting: {steps_setting}"
                elif key in ('-',):
                    steps_setting = max(1, steps_setting - 10)
                    status_msg = f"Steps setting: {steps_setting}"
                elif key in ('[',):
                    steps_setting = max(1, steps_setting - 1)
                    status_msg = f"Steps setting: {steps_setting}"
                elif key in (']',):
                    steps_setting = max(1, steps_setting + 1)
                    status_msg = f"Steps setting: {steps_setting}"
                elif key in ('h', 'H', '?'):
                    if not help_popup_shown:
                        help_popup_shown = True
                        popup = [
                            "Controls:",
                            "  f: batch FORWARD by current steps",
                            "  b: batch BACKWARD by current steps",
                            "  c: continuous FORWARD     v: continuous BACKWARD",
                            "  p: pause/resume           s: stop motion",
                            "  + / - : change steps by ±10   [ / ] : steps ±1",
                            "  q: quit",
                            "Press any key to close this help."
                        ]
                        # Simple modal
                        h, w = stdscr.getmaxyx()
                        box_w = max(len(line) for line in popup) + 4
                        box_h = len(popup) + 2
                        y0 = max(0, (h - box_h)//2)
                        x0 = max(0, (w - box_w)//2)
                        # Draw box
                        for i in range(box_h):
                            stdscr.addstr(y0 + i, x0, " " * box_w)
                        for i, line in enumerate(popup):
                            stdscr.addstr(y0 + 1 + i, x0 + 2, line)
                        stdscr.refresh()
                        stdscr.nodelay(False)
                        stdscr.getch()  # wait for any key
                        stdscr.nodelay(True)
                        help_popup_shown = False
            # End while
        except KeyboardInterrupt:
            pass
        finally:
            try:
                Motor1.Stop()
                Motor2.Stop()
            except Exception:
                pass
    curses.wrapper(_run)
if __name__ == "__main__":
    controller()
