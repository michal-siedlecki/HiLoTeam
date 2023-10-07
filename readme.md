# This is fork of HiLo app
#### source: https://github.com/Dawkap94/HiLoTeam 

The main goal of HiLo app is to create a bidirectional proxy server which allows to establish a SSH connection in easy way.
The connection allows to communicate and manage IOT devices in secure way over the internet
HiLo app can be used to create secure and easy to configure transmission of sensitive data over various endpoins in many industries
such as Medicine, Industry and Science

## Use case scenario
#### User wants to have IOT device data visible over the internet in a secure way

1. User asks HiLo team for creating is account (we want to have control)
2. HiLo team sends him credentials and download link
3. User logs in with its credentials and the RSA keys pair is generated at the server site
4. The private key is attached to the custom IOT OS build.
5. The public key is saved in user's ssh folder, so he can ssh into the server.

## Installation 
If you want to have your own HiLo server instance you need to follow these steps:
#### Prerequisites
* Remote server
* IOT device - Raspberry PI 
