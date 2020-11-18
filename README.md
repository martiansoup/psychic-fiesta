# psychic-fiesta
Raspberry Pi + Neopixel christmas lights

## Introduction

Software to control some christmas lights (a strip of neopixels) connected to a Raspberry Pi Zero.

The neopixel strip should be connected to pin D18, and a button connected between D24 and 3.3V. The button will advance between different patterns.

A web server is included to allow editing the code without using a monitor or VNC.

## Limitations

This is for a specific setup, and contains hardcoded paths etc. that would need to be modified.
E.g. it is assumed that the repo is checked out at `/home/pi`.

## Acknowledgements

This makes use of [jQuery](https://jquery.com) and [CodeMirror](https://codemirror.net) for some aspects of the web interface. Both are licensed under the MIT License.
