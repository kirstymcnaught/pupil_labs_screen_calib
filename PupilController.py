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
    ref_data = []

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
        self.ref_data = []

        # set calibration method to hmd calibration
        n = {'subject':'start_plugin','name':'HMD_Calibration', 'args':{}}
        print(send_recv_notification(self.req, n))

        # start calibration routine with params. This will make pupil start sampling pupil data.
        n = { 'subject':'calibration.should_start',
              'hmd_video_frame_size':(frameWidth, frameHeight),
              'outlier_threshold':35 }
        print(send_recv_notification(self.req, n))

        self.ready.emit()

    @pyqtSlot(int, int)
    def add_current_point_to_calib(self, screen_x, screen_y):
        t = get_pupil_timestamp(self.req)
        print('add calib point ({}, {});'.format(screen_x, screen_y))
        pos = (screen_x, screen_y)
        datum0 = { 'norm_pos':pos,'timestamp':t,'id':0 }
        datum1 = { 'norm_pos':pos,'timestamp':t,'id':1 }

        self.ref_data.append(datum0)
        self.ref_data.append(datum1)

    @pyqtSlot()
    def finish_calib(self):
        # Send ref data to Pupil Capture/Service:
        # This notification can be sent once at the end or multiple times.
        # During one calibraiton all new data will be appended.
        n = {'subject':'calibration.add_ref_data','ref_data':self.ref_data}
        print(send_recv_notification(self.req, n))

        # stop calibration
        # Pupil will correlate pupil and ref data based on timestamps,
        # compute the gaze mapping params, and start a new gaze mapper.
        n = {'subject':'calibration.should_stop'}
        print(send_recv_notification(self.req, n))

        time.sleep(2)
        n = {'subject':'service_process.should_stop'}
        print(send_recv_notification(self.req, n))




