This is a sensor data oscilloscope for xkit.

### History
- V1.0.0
  - Real-time sensor data plotting
  - Supports plotting up to 16 data
  - Support plotting selection
  - Supports saving collected data as csv format file
  - UDPServer or MulticastReceiver

### Install
```sh
pip install quat
```

### Dependencies
- PySide6
- PythonQwt
- numpy
- genlib

### Run
**UDP Server (default port 7321)**
```sh
smon
```

**MulticastReceiver (default group 239.8.7.6, default port 7321)**
```sh
smon --mcast
```

**options**  
--mcast
--group=\<group\> (default 239.8.7.6)
--iport=\<port\>  (default 7321)
--log=\<stream | file>

### Client Implementations
- UDPClient or MulticastSender

**sensor data format**
  ```sh
  x, y, z, ...
  ```

**Example**
  ```python
  import time
  from genlib.upd import UDPClient
  from pop.ext import IMU

  imu = IMU()
  udp = UDPClient()
  
  SMON_IP = '192.168.0.100'
  SMON_PORT = 7321

  while True:
      w, x, y, z = imu.read(IMU.QUATERNION)
      data = "{},{},{},{},".format(w, x, y, z)
      x, y, z = imu.read(IMU.ACCELERATION)
      data += "{},{},{},".format(x, y, z)
      x, y, z = imu.read(IMU.GYROSCOPE) 
      data += "{},{},{},".format(x, y, z)
      x, y, z = imu.read(IMU.MAGNETIC)
      data += "{},{},{},".format(x, y, z)
      x, y, z = imu.read(IMU.EULER)
      data += "{},{},{}".format(x, y, z)

      udp.sendTo(data.encode(), (SMON_IP, SMON_PORT))
      time.sleep(20/1000)  
  ```