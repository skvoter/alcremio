## alcremio - minimalistic sweet media player companion
Ultimate QT client for playerctl for those who loves mini-players

It is not a replacement of spotify/vlc/youtube apps or else, it's mini-player companion

Visual reference: [dvx/lofi](https://github.com/dvx/lofi)

**alcremio** heavily uses [altdesktop/playerctl](https://github.com/altdesktop/playerctl)



![ here's sweet alcremie! ^_^](/home/skvoter/petprojects/alcremio/alcremie.png)



### Plan for further development

#### Services

1. ##### alcremio
   
   QT mini-player supporting playerctl data as backend

   ` python pyQt pyGObject (or pgi) `
   
   - pyQt application
   - playerctl client
   
2. ##### alcremio-spotify (python)

   Enhanced spotify support with help of the API

   ` spotipy`

   - use playerctl + spotifyapi

   - normal volume changer and offset

   - change artwork url or use api for that (playerctl returns low quality one)

3. ##### alcremio-youtube (needs playerctl-youtube browser extension)

   ` playerctl-youtube-server`

   Support for youtube mixtapes, streams and podcasts , usual videos are supported via the browser extension

   - Use timestamp recognition
   - Use album artwork
   - Inspect youtube api (!)

   ###### After alcremio-recognition installed

   - Use audio recognition (shazam-like apis?)
   - If recognized, toggle Stream Image/Album Artwork

4. ##### alcremio-stream-playback

   > not sure about it, may use cvlc instead

   Custom simple command-line player for streaming mpeg streams and being supported in playerctl (also can use cvlc instead this one) 

   - **alcremio-recognition** is needed to show track meta and artwork

   - client utility (maybe using cvlc) for playing streams like radio or mixtapes

#### Modules

1. ##### playerctl-youtube

   Browser extension for parsing youtube video metadata to the MPRIS D-Bus Interface allowing to support simple youtube playback

2. ##### playerctl-youtube-server

   Python service enabling communication with extension though allowing playback control

3. ##### alcremio-recognition

   Module using some shazam-like recognition (look into yandex, echo etc), making stream and radio playback possible

#### Design Ideas

1. Extra pop-out window with title on hover (calculate position)
2. Controls on blurred artwork
3. Resizable

#### Miscellanious

1. Cool-looking readme
2. Site on github pages
3. Alcremie-related logo!
4. Donates?
5. Blog post everything before public release....
6. Engage open-source community after every feature release

> **P.S.** Pokemon are sweet!
