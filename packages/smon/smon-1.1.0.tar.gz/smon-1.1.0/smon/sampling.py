import time
import logging

import numpy as np
from PySide6.QtCore import QThread, Signal

import genlib.udp as udp


class SamplingThread(QThread):
    MAX_DETECT_COUNT = 8
    MAX_CHANNEL = 16
    SAMPLE_RANGE = 170 #100
    
    samplingSignal = Signal(object)
    changeUiSignal = Signal(bool)
    changeChannelLenSignal = Signal(int)
        
    def __init__(self, mainWindow, group, iport, mcast, log_name):
        super().__init__()
            
        mainWindow.resetSignal.connect(self.onReset)
        mainWindow.changeCurveSignal.connect(self.onChangeCurve)
        mainWindow.closeSignal.connect(self.onClose)
        
        if mcast:
            self.__socket = udp.MulticastReceiver(group=group, port=iport)
        else:
            self.__socket = udp.UDPServer(port=iport)

        self.__log_name = log_name  
        
        self.__channel_len = 0
        self.__curve_list = None
        self.__samples = None    
        self.__start_time = 0
        self.__is_run = True
        
    def onReset(self):
        self.__samples = np.array([[0.0] * self.SAMPLE_RANGE for _ in range(self.__channel_len + 1)])
        self.__start_time = time.time()
        
    def onClose(self):
        self.__is_run = False
        self.wait()
    
    def onChangeCurve(self, index, state):
        self.__curve_list[index] = state

    def __sammpling(self, data):          
        pdata = [time.time() - self.__start_time]
        pdata += [float(d) if self.__curve_list[i] else float(0) for i, d in enumerate(data)]
        
        self.__samples[:, -1:] = np.array(pdata).reshape(self.__channel_len + 1, 1)
        self.samplingSignal.emit(self.__samples)
        self.__samples = np.roll(self.__samples, -1, 1)
            
    def run(self):
        detect_count = 0
        init_session_flags = True

        while self.__is_run:
            message = self.__socket.recvFrom(unpickling=True, timeout=0.1) #Optimal value for current serial speed (115200 bps)
            if message:
                data = message.payload.replace(',', ' ').split()

                if detect_count < self.MAX_DETECT_COUNT:
                    detect_count += 2

                if init_session_flags and detect_count >= self.MAX_DETECT_COUNT:
                        self.__channel_len = len(data)
                        self.__curve_list = [True] * self.__channel_len
                        self.onReset()            
                        self.changeChannelLenSignal.emit(self.__channel_len)                        
                        self.changeUiSignal.emit(True)                        
                        
                        init_session_flags = False
                elif not init_session_flags:
                    self.__sammpling(data)
            else:                
                if detect_count > 0:
                    detect_count -= 1
                
                logging.getLogger(self.__log_name).info(f"message <None>, {detect_count=}")
                
                if detect_count <= 0 and not init_session_flags:
                    self.changeUiSignal.emit(False)
                    init_session_flags = True

            self.usleep(100)