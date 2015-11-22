import telegram
import subprocess as sp
import fnmatch
import os

rt = telegram.BotRoutines()


class AdminCommands:

    def __init__(self):
        self.caller_id = 1

    @staticmethod
    def check_uptime(caller_id):
        rt.send_text(caller_id, "Checking uptime on RPi2 at home")
        uptime = sp.check_output(["uptime"])
        print uptime
        rt.send_text(caller_id, uptime)

    @staticmethod
    def check_inet_interface(caller_id):
        rt.send_text(caller_id, "Inet interfaces on RPi2")
        inet = sp.check_output("ip link", stderr=sp.STDOUT, shell=True)
        print inet
        rt.send_text(caller_id, inet)

    @staticmethod
    def check_camera_connection(caller_id):
        camera = ''
        rt.send_text(caller_id, "Checking if camera is connected to RPi2")
        devs = os.listdir("/dev")
        for dev in devs:
            if fnmatch.fnmatch(dev, "video*"):
                camera = "/dev/" + dev
                rt.send_text(caller_id, "Found camera at %s" % camera)
                break
        if camera == '':
            rt.send_text(caller_id, "No cameras found")

    @staticmethod
    def check_kernel_version(caller_id):
        rt.send_text(caller_id, "Kernel version on RPi2")
        kernel = sp.check_output(["uname", "-a"])
        print kernel
        rt.send_text(caller_id, kernel)
