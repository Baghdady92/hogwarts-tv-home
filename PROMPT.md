# Set up Castle Home on your TV with a coding assistant

Paste the prompt below into a coding assistant that can run commands (Claude Code, or another) on a computer on the same Wi-Fi
as your TV. It asks you a few questions, sets Castle Home up for what you watch and where, builds it, installs it and checks
it on the TV.

Just want the app as it is? Install `Castle-Home.apk` from [Releases](../../releases/latest) instead, and change the dock
and the films on the TV with the gear at the top right ([GUIDE.md](GUIDE.md), sections 3 to 6).

**Before you start, on the TV:** Settings → Device Preferences → About, press OK on **Build** seven times, then go back to
Developer options and turn on **USB debugging** (and **Network debugging** if your TV shows it). Keep the TV on.

**Cleaning up the TV first is optional but worth it:** [cleanyourtv](https://github.com/Gathin23/cleanyourtv)'s
[`PROMPT.md`](https://github.com/Gathin23/cleanyourtv/blob/main/PROMPT.md) switches off the ads and the stock launcher's
feeds, and everything it does can be undone. Castle Home was built on a TV cleaned that way.

Copy everything between the two lines.

━━━━━━━━━━ PROMPT START ━━━━━━━━━━

```text
I want to install Castle Home (https://github.com/ikevinadams/hogwarts-tv-home), a wizarding-castle home screen for
Android TV, on my TV, set up for me. My TV is on the same Wi-Fi with Network/USB debugging on. I'll run adb pair and
adb connect myself when you ask; never type my pairing codes.

FIRST, ASK ME, one short question at a time (suggest answers when I'm unsure, and keep a running summary):
1. Which country I'm in.
2. Which streaming apps I use. Check a current source for my country (JustWatch, or the services' own sites) and tell
   me which of them have the eight Harry Potter films and the three Fantastic Beasts films, and suggest the best one.
   If none has them all, I can pick "the TV's own search", which finds each film wherever it streams.
3. Which apps I want on the dock, up to six, left to right. Start from what's installed on my TV (list the apps that
   have a TV launcher entry) and offer my HDMI inputs too, for a games console or a set-top box.
4. Whether Castle Home should be my home screen (the remote's Home button goes to it) or just an app I open.
Then summarise my answers and wait for my OK before changing anything.

THEN
- Clone the repository and read README.md and GUIDE.md.
- Check the TV: its model, its Android version (Castle Home needs Android 7 or newer), that Android System WebView is
  up to date, and the package names of the apps I chose.
- Edit hogwarts/config.js:
  - dock: my apps in my order, as { pkg, label }. An HDMI input is "input:<part of its HDMI-CEC device name>" (for
    example "input:playstation") or "input:<TV input id>" (adb shell dumpsys tv_input lists them).
  - films: the package of the service I chose, or "search" for the TV's own search.
  - askOnFirstRun: false (my answers are already in the file, so the TV shouldn't ask me again).
  - links: if my service's TV app opens a film from its web link, find the link for each of the eleven films in my
    country and add a block for that package (keys: hp1 to hp8 = the Harry Potter films in order, fb1 to fb3 = the
    Fantastic Beasts films). Test one on the TV first with
    adb shell am start -a android.intent.action.VIEW -d "<link>" <package>
    and check with a screenshot that it lands on the film. If the app ignores its links, leave links out for it:
    Castle Home then opens that app's own search for the film.
- Build it with ./build.sh. It needs JDK 17, the Android SDK (platform 35), Python 3 with Pillow and NumPy, and
  Node.js; tell me what's missing before installing anything on my computer.
- Before installing it, or sending any key press to the TV, check that I haven't pressed a button on the remote in
  the last minute, and wait if I have. Install with adb install -r.
- If I want it as my home screen: first note my current home app, so I can go back. Then on Android 10 or newer:
  adb shell cmd role add-role-holder android.app.role.HOME app.tvhome.hogwarts 0
  and on Android 7 to 9:
  adb shell cmd package set-home-activity app.tvhome.hogwarts/.HomeAlias
  Tell me the command that switches back.
- Check it on the TV with screenshots (adb exec-out screencap -p): the castle with my dock, the library and the
  greenhouse. Open one film and check it lands where it should.
- Finish by telling me how to change things later (on the castle, press Up to the gear at the top right, then OK),
  and remind me to turn USB / Network debugging off.

RULES
- Don't uninstall or disable anything on my TV, and don't change its settings beyond making Castle Home the home
  screen if I asked for that.
- Ask before installing anything on my computer.
```

━━━━━━━━━━ PROMPT END ━━━━━━━━━━

The prompts that made the castle, the owl, the library and the greenhouse, and the full brief Castle Home was built from,
are in [GUIDE.md](GUIDE.md), section 8.
