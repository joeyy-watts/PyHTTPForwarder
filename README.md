## PyHTTPForwarder
A simple script to forward HTTP requests to targets in a local network, based on the target's MAC address.

### Usage
For each target, add a line to the config `mac_addrs.conf` in the following format:
```
AA0000000000:1111
AA0000000011:1122
<target mac address>:<port to hit>
```

Any HTTP requests sent to the device running this server will then be forwarded to the target corresponding to the port you hit.


### Developer's Note
My home network setup limits static IP settings to only 8 devices and I got tired of trying to configure mDNS. It sometimes works, and most of the time instead of making my life easier, it has made my life a pain.

Thus, the PyHTTPForwarder was born. I just setup a Raspberry Pi running ngrok, running this script. So I can just send requests to my IoT devices via this Raspberry Pi.

Not the most elegant solution, and most likely not the correct way. But it is the easiest for me to deal with at this skill level (I don't want to spend more time wrangling my network configs and re-learn my Computer Network course)
