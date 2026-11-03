# Castle Home: the full guide

Full prompt and guide. A home screen for Android TV built around a castle at night: the castle's windows flicker, mist drifts over the lake, and a snowy owl sits on the app you've selected and flies to the next one as you move. Scroll down to a candle-lit library where the eight Harry Potter films are leather-bound books that turn to face you, and down again to a moonlit greenhouse with one beast for each Fantastic Beasts film. This guide has the steps to install the finished APK and make it yours (your apps on the dock, your streaming service for the films), every prompt used to make the pictures, and the prompts to build it yourself with a coding assistant, starting from cleaning up the TV. If you'd rather have a coding assistant set it all up for you, use [`PROMPT.md`](PROMPT.md).

A fan-made project for personal use. Not affiliated with or endorsed by Warner Bros., Wizarding World or J.K. Rowling. The film posters come from TMDB (themoviedb.org) and the app logos belong to Netflix, Amazon, JioHotstar, Sony, Google and Apple. The castle, bookshelf, greenhouse, beasts and owl were generated with AI (Nano Banana, GPT Image and Seedance, through Higgsfield). Don't sell it or publish the APK on an app store.

## 1. What you get

- **The castle (home):** a castle at night across a lake. Its windows flicker like candlelight, mist drifts over the water, the stars twinkle, the lake glints, and now and then a shooting star crosses the sky. The view breathes slowly, and every move along the dock gives a small push in and the faintest wobble.

- **The dock:** up to six of your apps and HDMI inputs, in candle gold, laid out like a regular TV home screen. It starts with Netflix, Prime Video, JioHotstar, PlayStation, YouTube and Apple TV (whichever your TV has); Netflix, Prime Video, JioHotstar, YouTube, Apple TV and a PlayStation get their gold logos, and any other app gets its name in the same gold. The selected one grows, glows warmly and shows its name. The clock and date are at the top left.

- **The owl:** a realistic snowy owl perches on the selected app. Move, and it crouches, takes off and flies to the next one, facing the way it flies. Between moves it sits, breathes and now and then looks around.

- **The library (one step down):** the eight Harry Potter films as leather-bound books on the middle shelf of an old bookcase, with a candle, an hourglass, a globe and glowing potions. The selected book turns to face you, its cover aged to match the room, with a brass plaque under it. OK swings the cover open and opens the film where you watch it (section 6).

- **The greenhouse (two steps down):** a moonlit glasshouse with a coin-hoarding creature on a stump, a long-tailed cat on a moonlit stone and a newborn fawn in a nest, one for each Fantastic Beasts film. Lantern light moves to the selected beast while the others fall into shadow, and the film's title appears. OK opens the film.

- **Customise:** the gear at the top right (press Up from the dock) opens a panel to pick the dock's apps and where the films open. It also opens by itself the first time.

- **Smoothness:** about 60 frames per second on an ordinary 1080p TV (tested on a MediaTek TV with 1.8 GB of memory).

## 2. What's in this repository

| File or folder | What it is |
|---|---|
| `README.md` | The short version: what it is, install, the remote. |
| `GUIDE.md` | This guide. Also as a PDF in `docs/`. |
| `PROMPT.md` | A prompt for a coding assistant that asks what you watch and where, sets Castle Home up for you, builds it and installs it on your TV. |
| `hogwarts/` | The home screen: one web page (`index.html`), its settings (`config.js`), the pictures (castle, shelf, greenhouse, window light, mist), the owl's sprite sheets and source clips, the book covers and the gold logos. |
| `hogwarts/tools/` | The scripts that made the layers from the pictures, and the one that makes the TV copy (section 9). |
| `hogwarts-tv/` | The Android TV app: a full-screen WebView around the page, with a small bridge to the TV. |
| `build.sh` | Builds the APK (and installs it with `./build.sh install`). |
| `docs/` | Screenshots and the PDF guide. |

On the [Releases](../../releases/latest) page: **Castle Home.apk** (ready to install) and **Castle Home - assets.zip**, every original picture and clip at full resolution (the 4K castle, shelf and greenhouses, the four greenhouse takes, both beast takes, the owl stills and clips with and without background, the posters, the logos in white and gold).

## 3. Install the APK

Works on: Android TV and Google TV, Android 7 or newer, with Android System WebView kept up to date from the Play Store. Built and tested on a 1080p Android 10 TV. The file is **Castle Home.apk**.

### Option A: with a USB stick or the "Send files to TV" app (no computer commands)

1. Copy **Castle Home.apk** to a USB stick, or send it to the TV with the **Send files to TV** app (phone and TV both need it).

1. On the TV, open a file manager, for example File Commander or X-plore from the Play Store.

1. Select the APK. When the TV asks, allow that file manager to **Install unknown apps**, then go back and select the APK again.

1. If Play Protect warns that the app isn't from the Play Store, choose **Install anyway**.

1. **Castle Home** now appears in your apps. Open it from there anytime.

### Option B: with adb from a computer

1. On the TV, enable Developer options: Settings → Device Preferences → About, then press **Build** 7 times.

1. In Settings → Device Preferences → Developer options, turn on **USB debugging** (on some TVs, Network debugging).

1. On the computer, install Android platform-tools (it includes adb), then run:

```bash
adb connect YOUR-TV-IP:5555
adb install "Castle Home.apk"
```

Accept the "Allow USB debugging?" prompt on the TV the first time.

## 4. Make it your home screen (optional)

You can simply open Castle Home from your apps. To make the remote's Home button go to it:

- If the TV asks which home app to use after you press Home, pick **Castle Home**, then **Always**.

- Most Android TV and Google TV models never ask. Use adb (see Option B), as follows.

First note your current launcher, so you can switch back later:

```bash
adb shell cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME
```

Switch to Castle Home on Android 10 or newer:

```bash
adb shell cmd role add-role-holder android.app.role.HOME app.tvhome.hogwarts 0
```

Switch to Castle Home on Android 7 to 9:

```bash
adb shell cmd package set-home-activity app.tvhome.hogwarts/.HomeAlias
```

To switch back, run the same command with your old launcher's package name (from the first command), or simply uninstall Castle Home:

```bash
adb uninstall app.tvhome.hogwarts
```

When you're done with adb, turn USB / Network debugging off again.

## 5. Using it with the remote

- **Left / Right:** move along the dock (the owl flies along), the books, or the beasts.

- **Down / Up:** castle → library → greenhouse, and back. On the castle, **Up** goes to the gear at the top right; OK there opens Customise.

- **OK:** open the selected app, or open the selected film. An HDMI input on the dock (a PlayStation, say) switches the TV to it.

- **Back:** up one section, or out of the Customise panel. On the castle it closes the app (if Castle Home is your home screen, it does nothing).

- **Home:** back to the castle, from anywhere.

When it starts, the screen fades in from black over a second or two while it prepares all three sections.

## 6. Make it yours

**On the TV.** Press **Up** on the castle to reach the gear at the top right, then **OK**. The Customise panel opens (it also opens by itself the first time):

- **The dock:** every app on your TV and every HDMI input, as tiles. OK adds one to the dock (it gets a number: its place from the left) or takes it off. Six at most.
- **The films open in:**
  - **JioHotstar, each film directly** (India): straight into each film. Shown when JioHotstar is installed.
  - **Your TV's search, any country:** the TV's own search for the film's title. On Google TV it lists where the film streams where you live; on older Android TV sets it shows the film's results (trailers, related films) from the apps that take part in search. The safe choice outside India.
  - **Any app you put on the dock, its search:** opens that app's search for the title (or the app itself, if it doesn't take searches).
- **Done** (or Back) keeps it; **Start again** goes back to the starting dock.

The choices are kept by the app on the TV, so they survive restarts and updates.

**In the files.** `hogwarts/config.js` is the starting point for every new install: the dock (`dock`), where the films open (`films`), direct links per app (`links`), and whether the panel opens by itself the first time (`askOnFirstRun`; set it to `false` once the file is already set up for your TV). To send the films straight into your service, add a block of links for it (keys `hp1` to `hp8` and `fb1` to `fb3`, the film order) with the links that service's website gives for each film, set `films` to its package, and rebuild (section 9). [`PROMPT.md`](PROMPT.md) has a coding assistant find those links for your country and do the rest.

## 7. Troubleshooting

- **A film opens on "Who's watching?":** JioHotstar asks for a profile when it wasn't already running. Pick one and the film starts.

- **A film doesn't open, or opens the wrong page:** the JioHotstar links are for India (hotstar.com/in) and were checked on 1 November 2026. If a title moves, update its address in `hogwarts/config.js` (`links`) and rebuild (section 9). Outside India, choose **Your TV's search** in Customise.

- **An HDMI input does nothing:** pick it again in Customise, from the list of your TV's own inputs. The starting dock looks for a port whose HDMI-CEC device name has "PlayStation" in it; if your console doesn't report its name, it won't be found and is left off.

- **"That app isn't on this TV":** it was uninstalled; take it off the dock in Customise.

- **"This TV has no search to open":** the TV's search app is switched off (some cleanups do that). Choose an app's search in Customise instead.

- **Not smooth:** update Android System WebView from the Play Store, and restart the TV once. On TVs with less than 1.5 GB of memory it may drop below 60 fps.

- **Play Protect warning:** expected for any app installed from outside the Play Store.

## 8. The full prompts (build it yourself with a coding assistant)

Three steps: clean up the TV, make the pictures, then build the home screen. (To install this one and set it up for you instead, use [`PROMPT.md`](PROMPT.md).) Paste each prompt into Claude Code with your TV connected over adb (Network debugging on, TV and computer on the same Wi-Fi). Copy everything between the two lines.

### Step 1: Clean up (debloat) the TV

The easiest way is [cleanyourtv](https://github.com/Gathin23/cleanyourtv): paste its [`PROMPT.md`](https://github.com/Gathin23/cleanyourtv/blob/main/PROMPT.md) into a coding assistant and it does this safely for most Android TV and Google TV brands. Castle Home was built on a TV cleaned that way. The prompt below is the one used on that TV, if you'd rather do it by hand.

Optional, and fully reversible: nothing is uninstalled, only switched off. The list at the end is what was disabled on the TV this was built on (a OnePlus TV); other brands have different packages, so the assistant will look at yours first.

━━━━━━━━━━ PROMPT START ━━━━━━━━━━

```text
My Android TV is cluttered and slow. It's connected over adb (I'll run adb pair / adb connect myself; don't ever type my pairing codes). Clean it up safely, and keep everything reversible.

BEFORE ANYTHING
- Take a full backup into backup/<date>/ and point backup/latest at it: package lists (all, enabled, disabled, third-party), getprop, every setting (global, secure, system), the current HOME configuration and the TV's inputs.
- Write tools/tv (adb pointed at the TV, finding it on the network by itself) and tools/disable (disables packages for user 0, one pm call per package, and logs each one with time and batch in debloat-log.txt).

RULES
- Only ever disable for user 0 (pm disable-user --user 0). Never uninstall anything.
- Work in batches, and after each batch check that Home, the inputs/HDMI, Live TV, the remote (including its Netflix key), Wi-Fi, Bluetooth and the Play Store still work.
- Never touch: Live TV and the HDMI/TV input services, the Input/Source menu and channel scan, the TV API and picture-quality services, the remote-control services and the Netflix-key observer, Bluetooth, the keyboard, the Play Store and Play Services, setup/OOBE and the factory menu.

BATCHES
1. Telemetry: the manufacturer's push/analytics services, remote diagnostics, Google feedback and bug-report senders.
2. Content and ads: Play Auto Installs (pushes promoted apps), the manufacturer's content feed, partner rows for the stock launcher, the recommendations service.
3. Background nags: "TV manager" cleaners and smart-home services I don't use.
4. Log upload services.
5. The stock launcher, only after another home screen is installed and set as Home (on some firmware Home keeps going to the stock launcher while it's enabled).

AFTERWARDS
- restore.sh: re-enables every package disabled since the backup (or one package: ./restore.sh com.package.name; --dry-run to preview) and gives Home back to the stock launcher.
- A README listing what was disabled, why, and what was deliberately kept.

For reference, on a OnePlus TV (Android TV 10) these were disabled: com.heytap.mcs, com.heytap.tv.remotediagnosing, com.google.android.feedback, com.google.android.tv.bugreportsender, android.autoinstalls.config.OnePlus, com.oneplus.tv.launcher, com.mediatek.android.leanbacklauncher.partnercustomizer, com.google.android.tvrecommendations, com.heytap.tv.assistant.oneplus, oneplus.smarthome, com.heytap.rom.service and (last) com.google.android.tvlauncher.
```

━━━━━━━━━━ PROMPT END ━━━━━━━━━━

### Step 2: Make the pictures

All of these are in **assets/01 backgrounds** and **assets/03 owl** already. Use these prompts to make your own versions. Costs are Higgsfield credits; the whole project used about 113.

**The castle** (Nano Banana; upload two to four photos of the castle you want, from similar angles):

```text
Using the attached reference images, recreate this exact castle: keep its architecture, towers, spires, rooflines and placement on the cliff identical. Only change the time, the weather and the camera.

Scene: the castle at night, seen from far across the lake in a wide, cinematic establishing shot. The castle sits slightly right of centre on its rocky cliff, with dark mountains and pine forest around it. Hundreds of windows glow warm amber and gold, like candlelight. A pale moon sits behind thin, slow-moving clouds and catches the edges of the towers with a cool silver rim light. Low mist drifts over the black, glassy lake, and the lit windows reflect in long, soft streaks on the water. A few faint stars show through the clouds. The mood is quiet, mysterious and moody, with no people, no boats, no text and no logos.

Camera and look: shot on an ARRI Alexa 65 with a wide prime lens, deep focus, natural film grain, and a high dynamic range that keeps detail in both the shadows and the glowing windows. The colour grade is a cinematic teal and deep-blue night against warm tungsten-orange windows, with rich but controlled contrast, lifted blacks with a slight blue tint, and gentle halation around the brightest lights. It should feel like a frame from a big-budget fantasy film, photoreal, not painted, not CGI-looking.

Format: 16:9 landscape, ultra high resolution. Keep the left third of the frame darker and calmer (sky, mist and water) so text and menus can sit over it.
```

**The bookshelf** (Nano Banana):

```text
An ultra-realistic photograph of an old wizard's library bookcase at night, shot straight-on and centred at eye level with the middle shelf, so the shelves run perfectly horizontal with no tilt and minimal perspective distortion.

The bookcase: a tall, heavy antique bookcase in dark aged walnut and oak, with visible wood grain, worn edges, carved side pillars and a carved crown moulding along the top. The back panel is dark vertical wooden planks. Three shelves are visible: a top shelf, a middle shelf and a lower shelf.

The middle shelf (most important): it fills the centre of the frame. Its middle 65% must be COMPLETELY EMPTY: bare wooden shelf and back panel only, with nothing standing in the gap. Only at the far left and far right ends of this shelf are there a few old leather-bound books, leaning slightly, with worn spines and faded, unreadable gold tooling.

The top shelf: stacks of antique leather books, lying flat and standing, plus a brass candlestick with a lit, dripping wax candle, an antique brass hourglass with golden sand, a small worn globe, and rolled parchment scrolls.

The lower shelf: glass potion bottles and apothecary jars with cork stoppers, some glowing faintly emerald green, violet and amber from within. Also old books, a brass key, dried herbs and a small stack of parchment.

Lighting: warm candlelight is the main light, coming from the upper left, with soft flickering amber glow and deep, moody shadows. The light falls off into darkness at the edges and corners. A few dust motes float in the candlelight. Rich contrast, inky shadows, warm highlights on the wood edges and brass.

Camera and look: shot on an ARRI Alexa Mini LF with a 50 mm lens at f/4, so the whole bookcase is sharp. Natural film grain, cinematic colour grade with warm amber and gold highlights, deep brown and teal-tinted shadows, and gentle halation around the candle flame. Photoreal: real materials, real dust, real wear. Not illustrated, not CGI.

No people, no readable text, no titles on spines, no logos.

Format: 16:9 landscape, ultra high resolution.
```

If it puts books in the gap, reply: "Keep everything else identical, but remove every object from the middle 65% of the middle shelf. It must be completely empty."

**The greenhouse** (Nano Banana 2.1, 16:9, 4K; about 3 credits each, four takes):

```text
Ultra-realistic cinematic wide shot, eye level, inside an old Victorian glasshouse greenhouse on the grounds of a remote Scottish castle, at night. Tall arched iron-framed glass walls and a glass roof, some panes fogged and a few cracked, overgrown with ivy. Cold silvery moonlight pours through the roof in soft volumetric beams; low drifting mist hugs the stone floor. A few old brass lanterns with warm amber candlelight hang from the ironwork, casting small pools of warm light. Strange, lush, magical-looking plants everywhere: giant ferns, twisting vines, oversized leaves, pale glowing flowers, a few hanging seed pods with a faint teal bioluminescent glow, and tiny drifting fireflies. Three clear, empty, well-lit spots spread across the middle of the frame, each waiting for a small creature: on the left a gnarled mossy tree stump with roots, in the centre a low round mossy stone platform in a pool of moonlight, on the right a large woven nest of twigs on a mossy stone ledge. These three spots are empty. The bottom fifth of the image is darker and calm (stone floor and mist) with no important detail. Night-time, moody, deep teal and blue shadows with warm amber accents, rich cinematic colour grading, shot on an ARRI Alexa with an anamorphic 35mm lens, shallow haze, fine film grain, high dynamic range, crisp detail. No people, no animals, no creatures, no text, no logos.
```

**The beasts** (Nano Banana 2.1, 16:9, 4K, with your chosen greenhouse attached as the reference):

```text
Keep this exact greenhouse image unchanged: same camera, framing, lighting, colour grade, and every plant, lantern, stone, stump and nest in exactly the same place. Only add three small magical creatures, one in each of the three empty spots, photorealistic, lit by the scene's own cool moonlight and warm lantern light, each casting a soft contact shadow, at a natural scale that fits its spot: (1) sitting upright on top of the mossy tree stump on the left: a small fluffy creature with velvety black fur, a long flat platypus-like bill, tiny clawed paws and shiny dark eyes, clutching a gold coin to its chest; (2) on the round mossy stone platform in the centre, in the pool of moonlight: a graceful cat-like beast about the size of a large lynx, with a lion-like face framed by a ruff of long fur in muted jewel tones, a long flowing feathery tail curled around its paws, sitting proudly and looking toward the camera; (3) curled up inside the woven twig nest on the right: a tiny newborn deer-like creature with pale, faintly glowing silvery-teal scales along its back, soft dark eyes and small antler buds, resting. Same night-time moody atmosphere, mist and fireflies. No people, no text, no logos.
```

**The owl** (GPT Image 2.5, 1:1, four takes; 0.25 credits each):

```text
Photorealistic wildlife photograph of a snowy owl with almost pure white plumage, only a few faint light-grey flecks on the wing tips, bright golden-yellow eyes, small black beak, thick fluffy feathered feet. The owl stands upright on a plain flat surface, body angled three-quarters to the right, head turned to look straight at the camera, wings neatly folded. Full body visible, centred horizontally and small in the frame: the owl fills only the lower-middle third of the image, its feet at about 85% of the image height, with lots of empty space above it and to both sides. Seamless flat dark slate-blue studio background (#1c232c), even, no gradient, no vignette, no props, no branch, no text. Lighting: cool silvery moonlight key from the upper left and a soft warm amber candle-glow rim light from the lower right. Crisp individual feather detail, sharp focus, natural colours, full-frame camera, 85mm lens.
```

**The owl sitting** (Seedance 2.5, 720p, 1:1, 5 seconds, no audio; the chosen owl still as both the start frame and the end frame, so it loops; about 35 credits):

```text
Locked-off static camera on a tripod, no camera movement, no zoom. The flat dark slate-blue background stays perfectly unchanged. The snowy owl stands on the same spot for the whole clip with its feet planted: it blinks slowly, turns its head smoothly to glance to the left, then turns back to look at the camera, gives one small gentle ruffle of its chest feathers and settles back into exactly the starting pose. Calm, subtle, natural, photorealistic motion with crisp feather detail. No other objects, no text.
```

**The owl hopping** (Seedance 2.5, 720p, **16:9**, 4 seconds, no audio; about 28 credits). Put the same owl still on a wider 16:9 canvas first, smaller (about 30% of the height, feet at 80%), with the background extended, and use that as both the start and the end frame. In a square frame the wingbeats get cut off.

```text
The snowy owl quickly crouches, then springs up and forward to the right with its wings opening wide in two strong, graceful flaps, glides briefly, and lands softly, folding its wings neatly and settling into exactly the starting pose, looking at the camera. The camera tracks sideways with the owl so it stays horizontally centred in the frame the whole time; the flat dark slate-blue background is plain and featureless so it looks unchanged. The owl stays small in the frame: its full wingspan always fits inside the frame with empty space around the wing tips, never touching the edges. The whole hop takes about one and a half seconds, then the owl stands still. Photorealistic feather and wing motion, natural weight on landing. No other objects, no text.
```

Then run both clips through Higgsfield's video background remover (about 1 credit each). It returns the owl on pure black, without transparency; the build makes the see-through version from that plus the original clip.

**The book covers:** the eight film posters from TMDB (themoviedb.org, the Harry Potter collection, w780 size), numbered 1 to 8 in film order. The build ages them to match the bookshelf photo.

### Step 3: Build Castle Home

Put the pictures in a folder first: castle.png, shelf.png, the greenhouse with beasts, covers 1–8.jpg, the owl still, the two owl clips and their background-removed versions. This is the complete brief, including every refinement and everything learned getting it smooth on a TV. It's the brief for the first version, with its fixed dock and JioHotstar links; this repository has since moved those into settings (the Customise panel and `config.js`, section 6), so to make your own variation, start from this repository rather than from scratch.

━━━━━━━━━━ PROMPT START ━━━━━━━━━━

```text
Build me a home screen for my Android TV themed on a wizarding castle at night, called Castle Home. Build it first as an HTML prototype I can preview in Chrome, then package that same page as its own Android TV app (a full-screen WebView loading the page from the APK), so my current launcher is never touched. Design everything on a 1920×1080 stage and scale it to the screen.

THE PICTURES (in my folder): castle.png (the castle at night), shelf.png (a bookcase whose middle shelf is empty), greenhouse_beasts.png (a greenhouse with three creatures), covers 1–8.jpg (the Harry Potter film posters), the owl still, owl idle and hop clips, and the same clips with the background removed (owl on pure black). Prepare lighter copies (about 2560 px wide for the browser, 1936 px for the TV) and keep the originals.

SECTION 1, THE CASTLE (home)
- The castle photo fills the screen. Make it feel alive using the photo itself:
  - Window candlelight: find the warm, bright window pixels (and their reflections) and make a glow layer from them, split into two interleaved sets of vertical stripes that flicker independently, like candles. Crop the layer to where there's light.
  - Mist: a soft, tileable band drifting slowly across the lake.
  - Stars: find the photo's own small bright dots in the open sky (above the spires) and twinkle them. Now and then (every 15–30 s) a faint shooting star crosses the sky on the left, never over the castle.
  - Lake: small warm glints shimmering in the castle's reflection, and a few cool ones under the moon.
  - A slow moonglow pulse.
- Camera: a slow breath (about ±1% zoom over 22 s, a few pixels of drift). On every move along the dock: a spring-driven push in of about 1% that eases back out, about 0.2° of wobble that rocks back twice, and a small pan toward the selected icon.
- The dock, laid out like a regular TV home screen: Netflix, Prime Video, JioHotstar, PlayStation (an HDMI input), YouTube and Apple TV as logos only, no tiles, in six 292 px cells with 84 px side padding, about 830 px down. Sized by visual weight, about 17% smaller than a typical launcher's. Tint the white logos candle gold #F0C29C (the colour of the castle's lit windows, lifted 30% toward white). The selected logo grows to 1.18× on a slightly bouncy spring, gets a warm glow and a warm pool of light under it, and its name fades in below.
- The clock and date at the top left in a serif face; Wi-Fi, Inputs and Settings outline icons at the top right; a small "The Library ⌄" hint at the bottom.
- Shade the bottom of the screen so the logos read over the lake.

THE OWL
- A realistic snowy owl perches on the selected logo, feet on the logo's top edge at its middle (measure each logo; on Prime Video it sits in the dip of the smile). It stands about 128 px tall.
- Sitting: hold still with a subtle breathing scale, and every few seconds play the idle clip (a blink and a glance around) once.
- Moving: play the hop clip at 1.7× speed and move the owl along an arc from the old logo to the new one during the airborne frames (measure take-off and touch-down from the clip; trim the still lead-in). Face the way it's going (mirror for left). If I press again mid-air, steer to the new logo without a jump; if I press again as it lands, spring straight off again. A few small sparkles where it lands.
- Make the owl's see-through frames from the background remover's output: anything not pure black is owl; fill only small enclosed gaps (eyes, beak, between the talons), never large ones, or background boxed in by a wing turns solid. Fade anything touching the frame edge. Take the colour from the original clip.
- Draw the owl from sprite sheets on canvases (one per clip, each sized and pinned at the feet), not from see-through video, which is unreliable in TV web views. Scale each clip so the standing owl is the same height, and record where its feet are. For the TV, trim every frame to its outline and pack them tightly.

SECTION 2, THE LIBRARY (one step down)
- The bookshelf photo fills the screen. The eight films stand as real 3D books (CSS 3D) in the empty middle of the middle shelf, sized like the photo's own books (about 200×300 px covers), thicker through the series.
- Spines: leather in each film's colour, aged toward dark brown, with gold bands, the Roman numeral, the title running vertically and a small star, lit from the candle above.
- One continuous, critically damped spring drives the selection. The selected book turns from spine-out to facing me (turned slightly, so its pages show), steps forward and lifts a little, and the row parts to make room, staying centred in the gap. A sheen sweeps across the cover when it lands. A brass plaque on the shelf edge under it reads "III · Prisoner of Azkaban · 2004". The books only turn out once the scroll into the library has arrived.
- Covers: age the posters so they belong in the photo: pull the colours part of the way toward the photo's old books, lift the blacks and soften the highlights, a little less saturation, warm candlelight, a soft bloom and a warm haze, slight softness, cloth-and-paper mottling, fine grain, a few hairline scuffs, darker grimy edges, rubbed corners and a lighter worn rim, and light falling off from the upper left.
- Life: the candle's glow flickers, the potions on the lower shelf pulse green, violet and amber, dust floats in the light, and a few sparks drift off a book as it turns.
- OK: the cover swings open with a burst of sparks, the screen fades to the film's title and "Opening on JioHotstar…", and the film starts.

SECTION 3, THE GREENHOUSE (two steps down)
- The greenhouse photo with its three creatures, one per Fantastic Beasts film: the coin hoarder on the stump (I, Where to Find Them, 2016), the long-tailed cat on the stone (II, The Crimes of Grindelwald, 2018) and the newborn in the nest (III, The Secrets of Dumbledore, 2022).
- The lantern-light reveal: everything but the selected creature sinks into darkness (about 66%), with a warm pool of light on it. Both fall off along a smootherstep curve with many stops, so there is no visible ring at the edge. The light glides between creatures on a spring, and the camera leans slightly toward it with the same push-in and wobble as the castle.
- The film's name under it: "FANTASTIC BEASTS · II · 2018" small, then the title large in gold, swapped while faded out.
- Life: the lanterns flicker, the teal seed pods pulse, fireflies drift and blink, low mist moves across the floor, and a faint shimmer of magic circles the selected creature.

NAVIGATION
- Left/Right: along the dock, the books or the creatures. Down/Up: castle → library → greenhouse and back, sliding with a little parallax, the scenes meeting in shadow rather than on a hard line. OK opens. Back goes up one section; at the castle it closes the app, unless the app is the home screen (then nothing). Home always returns to the castle.
- Hints at the edges ("The Library ⌄", "Home ⌃", "The Greenhouse ⌄", "← → browse · OK watch on JioHotstar").

OPENING THINGS (the TV app's bridge to the page: TV.launch(name) and TV.openFilm(url))
- Dock apps by package: Netflix com.netflix.ninja, Prime Video com.amazon.amazonvideo.livingroom, JioHotstar in.startv.hotstar, YouTube com.google.android.youtube.tv, Apple TV com.apple.atve.androidtv.appletv (the TV launch intent, or the normal one). PlayStation: switch to its HDMI input (TvContract.buildChannelUriForPassthroughInput with my TV's input id).
- Films: an ACTION_VIEW intent for https://www.hotstar.com/in/movies/<slug>/<id> sent to in.startv.hotstar, which goes straight into the film. Look up each film's current address on hotstar.com.

THE TV APP
- A separate package (app.tvhome.hogwarts), Java, no extra libraries, a full-screen black-background WebView with JavaScript, file access to its own assets, and the page's console going to logcat.
- In the TV's app list. A home-screen entry (an activity alias) that's off in debug builds, so it never competes with my launcher until I switch it on from adb, and on in the signed release build. Debug builds are testOnly so adb can switch that entry on and off.
- A build script that copies the page into the app with TV-sized pictures (refusing to build if the page's script doesn't parse), builds it, waits until I haven't touched the physical remote for 45 seconds, installs it and opens it. Never send keys or install while I'm using the remote. A script to switch the home screen to it and back.
- Log a frame-time report every 5 seconds so you can measure smoothness on the TV.

MAKE IT SMOOTH ON THE TV (this took it from about 8 to about 60 frames per second on a 1.8 GB MediaTek TV)
- Fit the stage with CSS zoom on the TV, not transform: scale(); under a transform the TV renders every moving layer at four times the pixels and runs out of graphics memory.
- No CSS animations: move everything from one requestAnimationFrame loop.
- Give everything that changes every frame its own layer (will-change), so the photos underneath are never re-drawn. Move things with transforms, never with left/top or margins.
- On the TV: no blend modes and no filters on moving layers, and bake static shading into the pictures.
- Crop overlay layers to where they have content; keep canvases small; draw soft things (dust, fireflies, the spotlight) at half or quarter resolution; slow particles update every other frame and pause during section scrolls.
- At start-up, behind a nearly black curtain, decode every picture and show each section for a few frames (library, greenhouse, castle) so nothing re-decodes or re-renders on the first visit; draw one hop frame too. Keep the neighbouring sections ready and switch off only the far one. No camera push-in during section scrolls on the TV.
- Keep the total picture memory small (pack the owl frames, covers at 400×600).
- The page handles every arrow key itself (preventDefault, even unused ones) and has no click handlers on the TV, otherwise the web view moves its own focus and draws a gold box.
- Skip style writes that haven't changed, and redraw the owl only when its frame changes.

Preview everything in Chrome first (screenshots of each section), then put it on my TV and measure.
```

━━━━━━━━━━ PROMPT END ━━━━━━━━━━

### Follow-up prompts, in the order the look was refined

1. "For the main home screen, I want to use the castle image, with the icons at the bottom just like my default home screen, in a scene that feels ambient and slightly dynamic. Slightly zoom in and out with a very, very subtle wobble as I move between the apps."

1. "Then the bookshelf section when we scroll down: the eight books in the empty middle shelf, each turning toward the screen when selected, opening the film on JioHotstar."

1. "Add a haze effect or texture to the book covers so they match the bookshelf photo."

1. "Generate a realistic white owl, similar to Hedwig. As I move between the icons, it hops, or slightly flies, and sits on the next icon."

1. "When the owl flies, a greyed-out background appears around it, and its wings get cut off when it flaps."

1. "Make the app icons 15–20% smaller, and colour them like the castle's lights, a little lighter."

1. "A third section for the Fantastic Beasts films: a Hogwarts-style garden with the beasts, at night. As I move between the beasts, highlight the film's name, linked to the film."

1. "Don't animate the beasts, but the spotlight needs to be softer; I can see the hardness of the circle."

1. "Deploy it on the TV." Then: "It's laggy and heavy on the TV, the owl isn't smooth, and moving between sections is horrible. Make it smoother."

1. "Some icons get a highlight box, and the Deathly Hallows books don't go into their films; check every book is connected to the right film."

## 9. Rebuilding from the source

| Path | What it is |
|---|---|
| `hogwarts/index.html` | The whole home screen (one page). Preview it with `python3 -m http.server 8765 --directory hogwarts` and open `http://localhost:8765/`; add `?tv` to see the TV version. Jump around with `#lib`, `#gh`, `#app=0..5`, `#f=0..7`, `#b=0..2`. In a browser the Customise panel shows a sample list of apps. |
| `hogwarts/config.js` | The starting dock, where the films open, and the direct film links (section 6). |
| `hogwarts/tools/` | The picture tools, run in this order: `gen_layers.py` (window light, mist, resized photos), `gen_points.py` (stars and lake glints), `crop_windows.py`, `age_covers.py`, `tint_logos.py`, `owl_pad.py` (the hop's wide start frame), `owl_alpha.py idle` and `owl_alpha.py hopwide 0.5 9`, `owl_sprites.py`. `tv_assets.py` (the TV copy) is run by `build.sh`. The full-size originals are in the assets zip on the Releases page. |
| `hogwarts-tv/` | The Android TV app (Java, no libraries): `MainActivity.java` is the WebView and the bridge (`TV.launch`, `TV.openFilm`, `TV.search`, `TV.apps`, `TV.inputs`, `TV.icon`). |
| `build.sh` | `./build.sh` builds the APK; `./build.sh install` also installs it on the TV adb is connected to. |

**You need:** JDK 17 and the Android SDK (platform 35; Android Studio has both), Python 3 with Pillow and NumPy, and Node.js (it checks the page's script before a build). The picture tools also need OpenCV (`pip install opencv-python-headless`) and ffmpeg on your PATH.

```bash
echo "sdk.dir=$HOME/Library/Android/sdk" > hogwarts-tv/local.properties     # where your Android SDK is
./build.sh
```

Without a key, the release build is signed with your debug key, which is fine for your own TV. To sign it with your own release key:

```bash
mkdir -p hogwarts-tv/release
keytool -genkeypair -keystore hogwarts-tv/release/castle-release.jks -alias castle -keyalg RSA -keysize 2048 -validity 10000
```

and create `hogwarts-tv/release/keystore.properties` with `storeFile=release/castle-release.jks`, `storePassword=…`, `keyAlias=castle` and `keyPassword=…`. Keep that key private (`.gitignore` keeps `hogwarts-tv/release/` out of git). The APK on the Releases page is signed with the author's own key, so a build signed with yours can't update it in place: uninstall it first.

## 10. Credits used

About 113 Higgsfield credits in total: owl stills 1, sitting clip 35, hop 28 (plus a first square take, 28), background removal 3, greenhouse 12 (four takes), beasts 6 (two takes). The castle and bookshelf were made separately with Nano Banana.
