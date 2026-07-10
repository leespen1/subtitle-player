# Subtitle Player

A small, self-contained web app for reading movie subtitles on your phone while
the movie plays on a TV. Load an `.srt` or `.vtt` file, press play the moment the
movie starts, and adjust the sync to line up with the dialog. Everything runs in
your browser; nothing is uploaded anywhere.

**Live:** https://spencerlee.net/subtitle-player/

The player itself is a single `index.html` with all CSS and JavaScript inline,
so it can be hosted on any static host with no build step.

## Install as an app (PWA)

The player ships as an installable Progressive Web App. Open the live URL in a
mobile browser and choose **Add to Home Screen**; it then launches full-screen
with its own icon and runs entirely offline, indistinguishable from a native app
in daily use. On desktop Chrome an install icon appears in the address bar.
