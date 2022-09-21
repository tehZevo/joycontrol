import numpy as np

#mouse movement to joycon imu motion controls conversion
#based on
#https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/imu_sensor_notes.md
#https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md

#some notes:
#imu values are reported as 16 bit (2 byte) little endian
#dekunukem suggests that to convert from raw values to degrees per second, you multiply by 0.06103f (4000/65535)
#according to the imu spec, 15% is recommended to add to the dps value, so the factor becomes 0.070 (4588/65535)
#thus, our conversion becomes the opposite: to convert from degrees/s to raw value, we round(dps/0.0070)
#3 sets of data are sent per report
#each set contains 12 bytes, 2 each for accel x, y, z and gyro roll, pitch, yaw (i believe that's the correct order)

MILLI_G_SCALE = 1/0.244 #milli gs
DPS_SCALE = 1/0.070

def dps2bytes(dps):
    dps = dps * DPS_SCALE
    dps = np.clip(np.round(dps), -32768, 32767)
    dps = list(np.array([dps]).astype("<i2").tobytes())
    return dps

def millig2bytes(millig):
    millig = millig * MILLI_G_SCALE
    millig = np.clip(np.round(millig), -32768, 32767)
    millig = list(np.array([millig]).astype("<i2").tobytes())
    return millig

#create a single imu frame given x/y/z accel (milli-Gs) and roll/pitch/yaw gyro (degrees/s) data
def construct_imu_frame(x, y, z, roll, pitch, yaw):
    #TODO: check order of roll, pitch, yaw
    #TODO: handle flipping axis(axes?) for "other" joycon
    #convert milligs and dps to int16le bytes
    x, y, z = [millig2bytes(e) for e in [x, y, z]]
    roll, pitch, yaw = [dps2bytes(e) for e in [roll, pitch, yaw]]
    #concatenate byte lists
    imu_bytes = x + y + z + roll + pitch + yaw
    return imu_bytes
