# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import zmq, msgpack, time


#convenience functions
def send_recv_notification(req, n):
    # REQ REP requirese lock step communication with multipart msg (topic,msgpack_encoded dict)
    print('send_recv_notification({})'.format(n))

    req.send_multipart((('notify.%s'%n['subject']).encode(), msgpack.dumps(n)))
    return req.recv()

def get_pupil_timestamp(req):
    req.send(b't') #see Pupil Remote Plugin for details
    return float(req.recv())


class PupilController(QObject):

    ready = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        #create a zmq REQ socket to talk to Pupil Service/Capture
        ctx = zmq.Context()
        self.req = ctx.socket(zmq.REQ)
        self.req.connect('tcp://localhost:50020')

        self.start_pupil();

    def start_pupil(self):
        # set start eye windows
        n = {'subject':'eye_process.should_start.0','eye_id':0, 'args':{}}
        print(send_recv_notification(self.req, n))
        n = {'subject':'eye_process.should_start.1','eye_id':1, 'args':{}}
        print(send_recv_notification(self.req, n))
        time.sleep(2)

        # Emit the signal.
        self.ready.emit()

    @pyqtSlot(int, int)
    def start_calib(self, frameWidth, frameHeight) :

        # set calibration method to hmd calibration
        n = {'subject':'start_plugin','name':'HMD_Calibration', 'args':{}}
        print(send_recv_notification(self.req, n))

        # start calibration routine with params. This will make pupil start sampling pupil data.
        n = { 'subject':'calibration.should_start',
              'hmd_video_frame_size':(frameWidth, frameHeight),
              'outlier_threshold':35 }
        print(send_recv_notification(self.req, n))

        self.ready.emit()


