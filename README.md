# huemenorah

This repository stores code to be used in a piece for the New Center's upcoming exhibition entitled "[8 Nights 8 Windows](http://www.8nights8windows.com)" on view December 6 - 14, 2015. The piece, HueMenorah, will be installed at Boomerang's, 1407 Washington Street, in the South End.

Nine Raspberry Pi units will run a web browser and take real-time commands from a database running at Firebase.com.

The RP units will display a single webpage: [client.html](https://github.com/saulbaizman/huemenorah/blob/master/client.html). When updates are made to the Firebase database, events will fire in the browser and prompt the browser to load new content.

A tenth RP will hold all of the photos and share them via NFS. It will also run a script, [server.py](https://github.com/saulbaizman/huemenorah/blob/master/server.py), on a periodic basis (via cron) to update the content on the screens.
