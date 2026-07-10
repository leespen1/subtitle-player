# Subtitle Player

A small, self-contained web app for reading movie subtitles on your phone while
the movie plays on a TV. Load an `.srt` or `.vtt` file, press play the moment the
movie starts, and adjust the sync to line up with the dialog. Everything runs in
your browser; nothing is uploaded anywhere.

**Live:** https://spencerlee.net/subtitle-player/

I made this so I could watch movies on a TV while in another country that
doesn't have English subtitles on their streaming platforms. There are many
apps for overlaying subtitles onto a video on your computer or phone, but
surprisingly I couldn't find a single one that handles *only subtitles.*

It turns out that subtitle files are incredibly simple plaintext (*as they
should be!*), so it was very simple to make a subtitle player using a small
amount of HTML/JavaScript, which can be hosted on a static site.

## Install as an app (PWA)

The player ships as an installable Progressive Web App. Open the live URL in a
mobile browser and choose **Add to Home Screen**; it then launches full-screen
with its own icon and runs entirely offline, indistinguishable from a native app
in daily use. On desktop Chrome an install icon appears in the address bar.
