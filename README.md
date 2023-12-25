# Thrym
An OpenCV-based robot for Ragnarock players

## Read carefully before using
Thrym is an open-source project provided "as is," without warranty of any kind, express or implied. By using Thrym, you agree that:

1. The project is provided for educational and informational purposes only.
2. The developers and contributors of Thrym make no representations or warranties of any kind concerning the safety, suitability, or accuracy of the project.
3. You are solely responsible for your use of Thrym and any consequences that may arise from it.
4. The developers and contributors of Thrym will not be liable for any direct, indirect, special, incidental, or consequential damages, whether based on contract, tort, or any other legal theory, arising out of your use or inability to use the project.
5. Thrym is not intended for use in any high-risk activities where the failure of the project could lead to harm, injury, or death. You agree not to use Thrym for such purposes.
6. The developers and contributors of Thrym are not responsible for any unauthorized or inappropriate use of the project.
7. You understand that Thrym may have bugs, errors, or other issues, and you use it at your own risk.

**By using Thrym, you acknowledge and agree to these terms. If you do not agree with these terms, you should not download, use, modify, distribute, share, and/or refer others to Thrym.**

Do not cause trouble in the community. **Your actions have consequences.**

## What?
This single Python script will "play" the game for you, so you have at least one "person" to play against. It's basically a dummy player that will actually put up some semblance of a fight.

The point of this robot is NOT to play the game perfectly, it's just to play it well enough to not feel lonely.

## Why?
I live in a region where this game is really (and I do mean REALLY) not well-known. I often had to wait until midnight just to play with others, even then many will (not "would") have latency issues or will eventually need to leave to do their things, leaving me with nobody to play. This was not good, so I have developed a solution.

## How?
This uses OpenCV to detect the notes and decide which keys to press. It uses various ways to try and optimize the process, such as using LUT (Lookup Table) and using masks to cut away sections that don't require processing.

## Cool, what do I need?
You need the following to use this robot.
1. A full copy of Ragnarock on Steam (PC)
2. (Optional) Additional DLCs to play
3. Another computer or a VR headset on another computer to join the multiplayer match
4. Second copy of Ragnarock on Steam (PC) to run on the computer/headset you'll use to play the game
5. Python libraries: `vidgear, opencv-python, pyautogui, pygetwindow, numpy`
6. Python 3.10 or newer

## Note
- Using this bot to cheat on the leaderboards will not end well.
- This is strictly for entertainment purposes and must not be used for any other purposes, including but not limited to, fraud and cheating.
- This script uses a lot of CPU processing power. You may need a better processor to run both the game and this script. I used AMD Ryzen 5 5600X for the development and testing rig.
- The author is not responsible for any damages or trouble you may encounter by choosing to use this script.


