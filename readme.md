# Geofencing with mobile Apps and Openhab

This application might help you to enable presence detection with your mobile phone, 
a geofence and OpenHab.

It has support for two mobile applications (iOS)
- Geofency https://itunes.apple.com/za/app/geofency-time-tracking/id615538630?mt=8 
- Locative (not under development anymore but still useful)
  - iOS https://github.com/LocativeHQ/ios-app
  - Android  https://github.com/LocativeHQ/android-app

Both applications allow to define a webhook to call a defined url with a username and password.

Note:
 I wrote the same functionality in Java 2 years ago. You can find it https://github.com/oliverwehrens/locative-openhab.
 This is my first try to do anything in Python, so don't be so hard on my code ;-). I know there are some checks
 missing for non existing config files but I decided to publish it anyway.

# Client Configuration

In both application when you define the geofence you have to name it (No spaces please). This location name along with the
username will be part of the switch in OpenHab.

## Geofency

The URL for entering and leaving the geofence at your location is the same. The last part of the url needs to be '/geofency'.
Geofency sends data in the POST request which indicates the direction of moving in or out. As mentioned POST request
is supported (not POST json encoded). At the Account define a username and a password.


## Locative

Locative supports GET requests. The URL for both entering and leaving the geofence is the same. The last part of the url needs to be '/locative'.
You need to define the http basic authentication with username and password.


# Openhab Config

You need to define what the base url for your OpenHab installation will be. This
is the content of the openhab-config.txt

Add the full Base Url for your Openhab installation, e.g.

http://192.168.1.35:8080

In Openhab you need an switch following this pattern:

Presence_\<username>_\<location>

e.g.

Switch Presence_John_home "Presence John via Geofence" (gPresence)

Every time you enter or leave the geofence this switch will be toggled.


# Generate users.txt

Users are authenticated via a users.txt file. This file is not supplied but this code,
you have to create it yourself. The syntax is simple

\<NAME\>  \<SHA1 ENCODED PASSWORD\>

To get the sha1 encoded password run 'generate_passwords.py' to get the output for users.txt
This is a sha1, utf-8 encoded string, e.g.

John b2684f613a70ba2124facf489b1d9ef3c0548017

Ass this line to the users.txt file.


# Build the image

If you created the users.txt file and modified the openhab-config.txt you are ready to build the image.

docker build -t locative-server:latest .

# Save image

If you build the image somewhere else you can save it locally, copy it to your server and import it there.

e.g.

docker save geofence-server:latest > geofence-server

and

docker import ./geofence-server owehrens/geofence-server

# Run the image

Once it is on your server you can run it like this:

docker run -d -p 5000:5000 geofence-server:latest

# Security

I would strongly recommend to run a SSL enabled connection in front of it if you plan to make it available to the
public internet (which is the whole idea).

One choice could be running the caddy webserver just before it and enable "Let's encrypt" for this URL.

A Caddyfile could look something like this:

```
my.super.domain:443 {
  tls me@super.domain
}

my.super.domain:443/geofence {
   proxy / my.internal_ip_of_the_geofence_server:5000
}
```

This would proxy all calls to https://my.super.domain:443/geofence/{locative,geofency} to the geofence server.
You would need to enter those urls in the corresponding client.


