# ACI-Health
A hardware based "monitor" for Cisco ACI infrastructure.

### What does it do?
 Let's start with a short description of what the device does. It's designed to show current "health status" of ACI infrastructure. Using the API it "reads" the current "System Health" score of the fabric and displays it on a 4x8 LED multicolour display. The "size" and colour of the display will reflect the health score of the fabric.

![alt text](https://github.com/Kris-Sekula/ACI-Health/blob/master/display.png "Health Score Display")
 
 In the first example we see that if the health score is "100" all rows, starting from bottom lit up in green. As the health score decreases the number of lit up rows decreases at the same time the colour changes, by the time the health score reaches 25, only two rows lit up red and so on.

### What are the use cases? 
 The device is a prof of concept. The "vision" for this device is to be installed in for example CTO's office, so that he/she can have a quick view of the organisation's datacenter network status without having to login to a computer/phone or any other device. Just a quick "glance" at the display will reveal the network status.
 It's also a great example of the flexibility of API built into the ACI product. I personally use it as a demo device when presenting ACI to customers, it serves a "monitoring" function telling me if the fabric is "ready for another demo".
     
### How it's done?

#### Hardware.
 The device is based on "Raspberry Pi Zero" embedded linux computer. The computer uses a wi-fi dongle plugged via a USB hub to connect to wireless network. The "screen" is an of-the-shelf available module. Power is provided via a micro USB cable (either from a "phone" style charger or using a USB-A-to-micro-USB cable plugged to a computer).

![alt text](https://github.com/Kris-Sekula/ACI-Health/blob/master/hw.png "Hardware details")

#### Software.
 The code that controls the gadget is written in python and the main monitoring script (monitor.py) is called on boot of the raspberry pi. I'm not a python guru so don't expect amazing code :) It's a good starting point for experiments with the API built into ACI.
