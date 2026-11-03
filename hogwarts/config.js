// Hogwarts TV's settings: the apps on the dock and where the films open.
// On the TV, the Customise panel (the gear at the top right, or Up from the dock) changes these and keeps its own copy;
// this file is the starting point for a new install, and the one to edit before you build. PROMPT.md fills it in for you.
window.CASTLE = {
  // Open the Customise panel by itself the first time Hogwarts TV starts, so someone who only installed the APK can
  // pick their own apps and service on the TV. Set it to false when this file is already set up for the TV (PROMPT.md
  // does): the panel then stays behind the gear until someone opens it.
  askOnFirstRun: true,

  // Up to six, left to right. `pkg` is an app's package name, or "input:<name>" for an HDMI port: the port whose
  // HDMI-CEC device name contains <name> (or whose TV input id is exactly <name>). Anything not on the TV is skipped.
  dock: [
    { pkg: "com.netflix.ninja", label: "Netflix" },
    { pkg: "com.amazon.amazonvideo.livingroom", label: "Prime Video" },
    { pkg: "in.startv.hotstar", label: "JioHotstar" },
    { pkg: "input:playstation", label: "PlayStation" },
    { pkg: "com.google.android.youtube.tv", label: "YouTube" },
    { pkg: "com.apple.atve.androidtv.appletv", label: "Apple TV" },
  ],

  // Where OK on a book or a beast takes you:
  //   an app's package: straight to the film if `links` below has it for that app, else that app's own search
  //   "search":         the TV's own search, which shows where each film streams in your country
  // If the app isn't installed, the TV's search is used.
  films: "in.startv.hotstar",

  // Direct links to each film, per app. Keys: hp1 to hp8 (the Harry Potter films in order), fb1 to fb3 (Fantastic Beasts).
  // Each is opened in that app with an ordinary "view this link" request, so use the links the app's own website gives
  // for the film. Add a block for your service and set `films` to its package.
  links: {
    "in.startv.hotstar": {                     // JioHotstar, India (checked 2026-11-01): opens and starts playing
      hp1: "https://www.hotstar.com/in/movies/harry-potter-and-the-sorcerers-stone/1971000398",
      hp2: "https://www.hotstar.com/in/movies/harry-potter-and-the-chamber-of-secrets/1971000409",
      hp3: "https://www.hotstar.com/in/movies/harry-potter-and-the-prisoner-of-azkaban/1971000405",
      hp4: "https://www.hotstar.com/in/movies/harry-potter-and-the-goblet-of-fire/1971000404",
      hp5: "https://www.hotstar.com/in/movies/harry-potter-and-the-order-of-the-phoenix/1971000408",
      hp6: "https://www.hotstar.com/in/movies/harry-potter-and-the-half-blood-prince/1971000403",
      hp7: "https://www.hotstar.com/in/movies/harry-potter-and-the-deathly-hallows-part-1/1971000406",
      hp8: "https://www.hotstar.com/in/movies/harry-potter-and-the-deathly-hallows-part-2/1971000407",
      fb1: "https://www.hotstar.com/in/movies/fantastic-beasts-and-where-to-find-them/1971000401",
      fb2: "https://www.hotstar.com/in/movies/fantastic-beasts-the-crimes-of-grindelwald/1971000400",
      fb3: "https://www.hotstar.com/in/movies/fantastic-beasts-the-secrets-of-dumbledore/1971311440",
    },
  },
};
