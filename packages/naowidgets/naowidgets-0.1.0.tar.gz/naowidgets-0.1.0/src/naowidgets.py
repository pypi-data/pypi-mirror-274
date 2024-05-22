import asyncio
import traceback

import ipywidgets as widgets
from IPython.display import display

###########################
# A few general utilities

def as_widget(func):
    "Decorator that immediatly runs a top-level coroutine and shows it's result in a widget."
    log_widget = widgets.HTML(
        layout={'width': '99%'}
    )
    
    def _log(*args, color='black'):
        log_messages = ''
        lines = " ".join(map(str, args))
        for line in lines.split('\n'):
            log_messages += f'<span style="color: {color};">{line}</span>\n'
        log_widget.value += f'<pre style="font-family: monospace; margin: 0;">{log_messages}</pre>'
        
    async def wrapped():
        try:
            await func(_log)
        except Exception:
            err_msg = traceback.format_exc()
            _log(err_msg, color='red')
            
    task = asyncio.ensure_future(wrapped())
    display(log_widget)

def show(fut):
    """For one-line calls to NAOqi functions, so the output is captured and shown in a text widget.

    usage:
    show(nao.ALTextToSpeech.getLanguage())

    Only use this as the top-level in a notebook.
    """
    async def func(print):
        print(await fut)
    return as_widget(func)

###########################
# More specific widgets for motion control

def _set_toggle_cb(toggle_button, async_func):
    toggle_button.observe(lambda c: asyncio.create_task(async_func(c.new)), 'value')

class StiffnessToggle:
    def __init__(self, nao, joints, label):
        self.nao = nao
        self.joints = joints
        self.label = label
        self.button = widgets.ToggleButton(value=False)
        self.widget = self.button
        _set_toggle_cb(self.button, self.set_stiffness_async)

    async def init_async(self):
        stiffs = await self.nao.ALMotion.getStiffnesses(self.joints[0])
        is_stiff = bool(stiffs[0])
        self.button.value = is_stiff
        await self.set_stiffness_async(is_stiff)

    async def set_stiffness_async(self, is_on):
        label = "🔒" if is_on else "⚪"
        self.button.description = f'{self.label}: {label}'
        self.button.button_style = 'info' if is_on else 'warning'
        await self.nao.ALMotion.setStiffnesses(self.joints, 1.0 if is_on else 0.0)

class HandToggle:
    def __init__(self, nao, hand):
        self.nao = nao
        self.hand = hand
        self.button = widgets.ToggleButton(value=False)
        self.widget = self.button
        _set_toggle_cb(self.button, self.set_hand_open_async)

    async def init_async(self):
        angles = await self.nao.ALMotion.getAngles(self.hand, True)
        is_open = bool(angles[0])
        self.button.value = is_open
        await self.set_hand_open_async(is_open)

    async def set_hand_open_async(self, is_open):
        label = "Open" if is_open else "Closed"
        await self.nao.ALMotion.setStiffnesses([self.hand], 1.0)
        self.button.description = f'{self.hand}: {label}'
        await self.nao.ALMotion.setAngles(self.hand, 1.0 if is_open else 0.0, 0.5)

class PoseSaver:
    def __init__(self, nao, joints):
        self.nao = nao
        self.joints = joints
        self.poses = []
        self.layout = widgets.Layout(width='auto', height='40px')  # Common layout for buttons

        # Buttons for top row
        self.add_pose_button = widgets.Button(description='Add pose 📌', layout=self.layout)
        self.clear_button = widgets.Button(description='Clear ❌', layout=self.layout)
        self.play_all_button = widgets.Button(description='Play all ▶️', layout=self.layout)

        # Setting callbacks
        self.add_pose_button.on_click(lambda _: asyncio.create_task(self.append_pose_async()))
        self.clear_button.on_click(self.clear_poses)
        self.play_all_button.on_click(lambda _: asyncio.create_task(self.replay_async(0.0, 0.5)))  # Example delay and speed

        # Top row
        self.top_row = widgets.HBox([self.add_pose_button, self.clear_button, self.play_all_button])

        # Pose list display
        self.pose_display = widgets.VBox([])
        self.update_pose_display()

        # Main widget layout
        self.widget = widgets.VBox([self.top_row, self.pose_display])

    async def append_pose_async(self):
        current_pose = await self.nao.ALMotion.getAngles(self.joints, True)
        self.poses.append(current_pose)
        self.update_pose_display()

    def clear_poses(self, _):
        del self.poses[:]
        self.update_pose_display()

    async def replay_async(self, delay_between, fraction_speed):
        await self.nao.ALMotion.setStiffnesses(self.joints, 1.0)
        for pose in self.poses:
            await self.nao.ALMotion.angleInterpolationWithSpeed(self.joints, pose, fraction_speed)
            await asyncio.sleep(delay_between)

    def create_copy_button(selmf, pose, button_id):
        # Serialize the pose data into a string format for JavaScript
        pose_str = str(pose).replace("'", "\\'").replace('"', '\\"')
        # Make a HTML that looks like a widget
        button_html = f"""
        <button id="{button_id}" onclick="
            navigator.clipboard.writeText('{pose_str}').then(function() {{
                document.getElementById('{button_id}').innerText = '✔️';
                setTimeout(function(){{ document.getElementById('{button_id}').innerText = '📋'; }}, 500);
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});"
            class="p-Widget jupyter-widgets jupyter-button"  # Use ipywidgets classes
            style="height: 40px; width: auto; padding-left: 10px; padding-right: 10px;
                   padding-top: 0px; padding-bottom: 0px; line-height: var(--jp-widgets-inline-height);
                   background-color: var(--jp-layout-color2); color: var(--jp-ui-font-color1); 
                   border: none; box-shadow: none; user-select: none; cursor: pointer;">
        📋
        </button>
        """
        # height 100% seems to sometimes work
        return button_html

    def update_pose_display(self):
        rows = []
        for idx, pose in enumerate(self.poses, start=1):
            label = widgets.Label(value=f'Pose {idx}', layout=self.layout)
            # Generate a unique ID for each copy button
            button_id = f"copy_button_{idx}"
            # Create the HTML widget for the copy button
            copy_button_html = self.create_copy_button(pose, button_id)
            copy_button_widget = widgets.HTML(value=copy_button_html)
            copy_button_widget.layout.margin = "0px"
            set_button = widgets.Button(description='🔧', tooltip='Set', layout=self.layout)
            set_button.on_click(self.make_set_pose_callback(pose)) # Can't be done inline or variable changes
            delete_button = widgets.Button(description='🗑️', tooltip='Delete', layout=self.layout)
            delete_button.on_click(self.make_delete_pose_callback(idx-1))
            row = widgets.HBox([label, set_button, copy_button_widget, delete_button])
            rows.append(row)
        self.pose_display.children = rows

    def make_set_pose_callback(self, pose):
        return lambda b: asyncio.create_task(self.set_pose_async(pose))

    async def set_pose_async(self, pose):
        await self.nao.ALMotion.angleInterpolationWithSpeed(self.joints, pose, 0.5)

    def make_delete_pose_callback(self, index):
        def delete_pose(_):
            del self.poses[index]
            self.update_pose_display()
        return delete_pose

def make_banner(title):
    banner = widgets.HTML(value=f"<div style='width: 100%; background-color: lightblue; text-align: center; padding: 0px;'>{title}</div>")
    banner.layout.margin = '0px'
    return banner

ARM_JOINT_SUFFIXES = ['ShoulderPitch', 'ShoulderRoll', 'ElbowYaw', 'ElbowRoll', 'WristYaw']

class NaoArmController:
    def __init__(self, nao, arm_side, side_name):
        self.nao = nao
        arm_joints = [(arm_side + suff) for suff in ARM_JOINT_SUFFIXES]
        self.all_arm_joints = arm_joints + [f"{arm_side}Hand"]

        # Sub-widgets
        self.stiffness_control = StiffnessToggle(nao, arm_joints, f"{arm_side}Arm")
        self.hand_control = HandToggle(nao, f"{arm_side}Hand")
        self.pose_saver = PoseSaver(nao, self.all_arm_joints)
        self.poses = self.pose_saver.poses

        # Banner
        self.banner = make_banner(f"{side_name} Arm Controller")

        # Layout
        self.buttons_layout = widgets.HBox([self.stiffness_control.widget, self.hand_control.widget])
        self.pose_layout = widgets.HBox([self.pose_saver.widget])
        self.main_layout = widgets.VBox([self.banner, self.buttons_layout, self.pose_saver.widget])
        self.main_layout.layout.border = '2px solid black'
        self.main_layout.layout.overflow = 'hidden'

        asyncio.ensure_future(self.stiffness_control.init_async())
        asyncio.ensure_future(self.hand_control.init_async())

        display(self.main_layout)

    def replay(self, delay_between=0.0, fraction_speed=0.5):
        asyncio.ensure_future(self.replay_async(delay_between, fraction_speed))

    async def replay_async(self, delay_between, fraction_speed):
        await self.stiffness_control.set_stiffness_async(True) # We want to also update the widget
        await self.pose_saver.replay_async(delay_between, fraction_speed)

class LeftArmController(NaoArmController):
    def __init__(self, nao):
        super().__init__(nao, "L", "Left")

class RightArmController(NaoArmController):
    def __init__(self, nao):
        super().__init__(nao, "R", "Right")

class NaoTorsoController:
    def __init__(self, nao):
        self.nao = nao
        left_arm_joints = [('L' + suff) for suff in ARM_JOINT_SUFFIXES] + ['LHand']
        right_arm_joints = [('R' + suff) for suff in ARM_JOINT_SUFFIXES] + ['RHand']
        head_joints = ['HeadYaw', 'HeadPitch']

        # Combining all joints for the torso controller
        self.all_joints = left_arm_joints + right_arm_joints + head_joints

        # Sub-widgets
        self.left_arm_stiffness = StiffnessToggle(nao, left_arm_joints[:-1], "Left")  # Excluding hand
        self.right_arm_stiffness = StiffnessToggle(nao, right_arm_joints[:-1], "Right")  # Excluding hand
        self.left_hand_control = HandToggle(nao, 'LHand')
        self.right_hand_control = HandToggle(nao, 'RHand')
        self.head_stiffness = StiffnessToggle(nao, head_joints, "Head")
        self.pose_saver = PoseSaver(nao, self.all_joints)
        self.poses = self.pose_saver.poses

        # Banner
        self.banner = make_banner("Torso Controller")

        # Layout
        self.head_layout = widgets.HBox([self.head_stiffness.widget])
        self.arm_controls_layout = widgets.VBox([
            widgets.HBox([self.left_arm_stiffness.widget, self.right_arm_stiffness.widget]),
            widgets.HBox([self.left_hand_control.widget, self.right_hand_control.widget])
        ])
        self.pose_layout = widgets.HBox([self.pose_saver.widget])

        self.main_layout = widgets.VBox([
            self.banner, self.head_layout, self.arm_controls_layout, self.pose_saver.widget
        ])
        self.main_layout.layout.border = '2px solid black'
        self.main_layout.layout.overflow = 'hidden'

        asyncio.ensure_future(self.left_arm_stiffness.init_async())
        asyncio.ensure_future(self.right_arm_stiffness.init_async())
        asyncio.ensure_future(self.left_hand_control.init_async())
        asyncio.ensure_future(self.right_hand_control.init_async())
        asyncio.ensure_future(self.head_stiffness.init_async())

        display(self.main_layout)

    def replay(self, delay_between=0.0, fraction_speed=0.5):
        asyncio.ensure_future(self.replay_async(delay_between, fraction_speed))

    async def replay_async(self, delay_between, fraction_speed):
        await asyncio.gather(
            self.left_arm_stiffness.set_stiffness_async(True),
            self.right_arm_stiffness.set_stiffness_async(True),
            self.head_stiffness.set_stiffness_async(True)
        )
        await self.pose_saver.replay_async(delay_between, fraction_speed)

