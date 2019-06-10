# Supported mobile Applications

- geofency
- locative

# Openhab Config

Add the full Base Url for your Openhab installation, e.g.

http://192.168.1.35:8080

In Openhab you need an switch following this pattern:

Presence_\<name>_\<location>

e.g.

Switch Presence_John_home "Presence John via Locative" (gPresence)



# Generate users.txt

Run 'generate_passwords.py' to get the output for users.txt
This is a sha1, utf-8 encoded string, e.g.

John b2684f613a70ba2124facf489b1d9ef3c0548017


# Build the image

docker build -t locative-server:latest .

# Save image

docker save locative-server:latest > locative-server

# Run the image

docker run -d -p 5000:5000 locative-server:latest

