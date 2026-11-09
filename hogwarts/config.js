// Hogwarts TV's settings: the apps on the dock and where the films open.
// On the TV, the Customise panel (the gear at the top right, or Up from the dock) changes these and keeps its own copy;
// this file is the starting point for a new install, and the one to edit before you build. PROMPT.md fills it in for you.
// BaghdadyLive takes no web links: its MainActivity follows a "resume_route" extra (the route its Watch Next row uses),
// so each film is an intent: link to its player route, by the film's TMDB id, title and year.
function baghdady(tmdb, title, year) {
  const route = `player/movie/${tmdb}?title=${encodeURIComponent(title)}&year=${year}&season=&episode=`;
  return "intent:#Intent;action=android.intent.action.VIEW;component=com.baghdady.live/.MainActivity;" +
         `S.resume_route=${encodeURIComponent(route)};end`;
}

window.CASTLE = {
  // Open the Customise panel by itself the first time Hogwarts TV starts, so someone who only installed the APK can
  // pick their own apps and service on the TV. Set it to false when this file is already set up for the TV (PROMPT.md
  // does): the panel then stays behind the gear until someone opens it.
  askOnFirstRun: false,

  // Up to six, left to right. `pkg` is an app's package name, or "input:<name>" for an HDMI port: the port whose
  // HDMI-CEC device name contains <name> (or whose TV input id is exactly <name>). Anything not on the TV is skipped.
  dock: [
    { pkg: "com.netflix.ninja", label: "Netflix" },
    { pkg: "com.google.android.youtube.tv", label: "YouTube" },
    { pkg: "com.baghdady.live", label: "BaghdadyLive" },
    { pkg: "com.mbm_soft.darpromax", label: "DAR PRO MAX" },
    { pkg: "net.mbc.shahidTV", label: "MBC Shahid" },
  ],

  // Where OK on a book or a beast takes you:
  //   an app's package: straight to the film if `links` below has it for that app, else that app's own search
  //   "search":         the TV's own search, which shows where each film streams in your country
  // If the app isn't installed, the TV's search is used.
  films: "com.baghdady.live",

  // Direct links to each film, per app. Keys: hp1 to hp8 (the Harry Potter films in order), fb1 to fb3 (Fantastic Beasts).
  // Each is opened in that app with an ordinary "view this link" request, so use the links the app's own website gives
  // for the film. Add a block for your service and set `films` to its package.
  links: {
    "com.baghdady.live": {                     // BaghdadyLive (checked 2026-11-09): starts the film in its player
      hp1: baghdady(671,    "Harry Potter and the Philosopher's Stone", 2001),
      hp2: baghdady(672,    "Harry Potter and the Chamber of Secrets", 2002),
      hp3: baghdady(673,    "Harry Potter and the Prisoner of Azkaban", 2004),
      hp4: baghdady(674,    "Harry Potter and the Goblet of Fire", 2005),
      hp5: baghdady(675,    "Harry Potter and the Order of the Phoenix", 2007),
      hp6: baghdady(767,    "Harry Potter and the Half-Blood Prince", 2009),
      hp7: baghdady(12444,  "Harry Potter and the Deathly Hallows: Part 1", 2010),
      hp8: baghdady(12445,  "Harry Potter and the Deathly Hallows: Part 2", 2011),
      fb1: baghdady(259316, "Fantastic Beasts and Where to Find Them", 2016),
      fb2: baghdady(338952, "Fantastic Beasts: The Crimes of Grindelwald", 2018),
      fb3: baghdady(338953, "Fantastic Beasts: The Secrets of Dumbledore", 2022),
    },
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
