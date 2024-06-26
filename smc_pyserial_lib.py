
import serial
import time


class SMC:
  
  def __init__(self, port, baud=115200, timeOut=0.1):
    self.ser = serial.Serial(port, baud, timeout=timeOut)


  def send_msg(self, msg_to_send):
    data = ""
    prev_time = time.time()
    while data=="":
      try:
        self.ser.write(msg_to_send.encode())   # send a single or multiple byte    
        data = self.ser.readline().decode().strip()
        if time.time()-prev_time > 2.0:
          raise Exception("Error getting response from arduino nano, wasted much time \n")
      except:
        print("Error getting response from arduino nano, wasted much time \n")
    return data


  def send(self, cmd_route, valA=0, valB=0):
    if cmd_route == "/mode":
      return False
    
    cmd_str = cmd_route+","+str(valA)+","+str(valB)
    data = self.send_msg(cmd_str)
    if data == "1":
      return True
    else:
      return False
  
  
  def get(self, cmd_route):
    data = self.send_msg(cmd_route).split(',')
    if len(data)==2:
      return float(data[0]), float(data[1])
    elif len(data)==1:
      return float(data[0])





  def sendTargetVel(self, targetVelA=0.0, targetVelB=0.0):
    isSuccess = self.send("/tag", targetVelA, targetVelB) # sends  targetA, targetB
    return isSuccess
  
  def sendPwm(self, pwmValA=0, pwmValB=0):
    isSuccess = self.send("/pwm", pwmValA, pwmValB) # sends  pwmValA, pwmValB
    return isSuccess
  
  def getMotorsVel(self):
    angVelA, angVelB = self.get("/vel")
    return angVelA, angVelB
  
  def getMotorsPos(self):
    angPosA, angPosB = self.get("/pos")
    return angPosA, angPosB
  
  def getMotorAData(self):
    angPos, angVel = self.get("/dataA")
    return angPos, angVel
  
  def getMotorBData(self):
    angPos, angVel = self.get("/dataB")
    return angPos, angVel
  