Spotify:
- Get Recently played tracks == https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recently-played
    - How are the recently played songs calculated? -- tested on the 17/06/22


| Test | Result | Context | Comments on Action |
| ----------- | ----------- | ---- | ---- |
| Does a song get added to the recently played list if it is playing| No, seems to either the application is closed or if the song is finished playing | | |
| Does a song get added to the recently played list if the song is not completed but a new song is started| No, the song is not added to recently played | |
| How quickly does a song get added to the recently played list after a song is completed | Immediate | |
| -- What does the time given played at represent (stared song or end of song)| The result is at the time of the song ending or application closed |||
| What does closing the session of the spotify app have on the recently played list| The song is classed as a played song at the time of closing the spotify application but not added to recently played song till the application is opened again | Noticed that the same song can be played twice or three times. This was triggered by closing the app or the computer going to sleep||
|||||
<br>
    - Will the limit of receiving the 50 latest songs be an issue?
<br>
- Spotify authorisation == https://developer.spotify.com/documentation/general/guides/authorization/
