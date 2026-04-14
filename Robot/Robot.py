from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import UltrasonicSensor
import socketserver
"""
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
"""

#region VARIABLES
robot_ip_address = "100.75.155.137"

motor_outputs = {"A": OUTPUT_A,
          "B": OUTPUT_B,
          "C": OUTPUT_C,
          "D": OUTPUT_D}

left_output, right_output = OUTPUT_B, OUTPUT_C
left_motor, right_motor = LargeMotor(left_output), LargeMotor(right_output)

T = 100  # Time between requests in ms (informational)
dt = 50  # Extra time to avoid motion discontinuity (ms)

max_speed = 1049
#endregion

"""
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
"""

#region FONCTION STATIC
def max(a,b):
    if a > b:
        return a
    return b

def normalize(value):
    """
    :param value: value à faire rentrer dans l'intervalle ]-1050, 1050[
    """
    v1, v2 = value
    m = max(abs(v1), abs(v2))
    if m > max_speed:
        if m != 0:
            return (v1/m * max_speed, v2/m * max_speed)
        else:
            return (0,0)
    return value

def connect_motors(left: str, right: str) -> None:
    """
    :param left: A, B, C, D output for left motor
    :param right: A, B, C, D output for right motor
    :return: None
    """
    global left_output, right_output, left_motor, right_motor

    # Validate input parameters
    if not (left in motor_outputs.keys()) or not (right in motor_outputs.keys()):
        print("Invalid motor output format")
        raise NotImplemented

    # change les entrées
    left_output = motor_outputs[left]
    right_output = motor_outputs[right]

    # Reinitialize motor objects with new outputs
    left_motor = LargeMotor(left_output)
    right_motor = LargeMotor(right_output)

def drive(left_speed : int, right_speed : int) -> None:
    """
    :param left_speed: left motor speed
    :param right_speed: right motor speed
    :return: None
    """
    global left_motor, right_motor, T, dt

    left_speed, right_speed = normalize((left_speed, right_speed))

    # Run motors at given speeds
    left_motor.run_timed(speed_sp = left_speed, time_sp = T + dt)
    right_motor.run_timed(speed_sp = right_speed, time_sp = T + dt)

def interpret(msg : str) -> None:
    """
    :param msg: cmd à exécuter
    :return: None
    """
    # Robot may queue requests; always process the latest one
    msg = msg.split(';')[-2]

    cmd = msg[:3]
    print(msg)

    if cmd == "MOV":
        str_left_speed, str_right_speed = msg[4:].split(' ')
        drive(int(str_left_speed), int(str_right_speed))

    elif cmd == "CON":
        left, right = msg[4:].split(' ')
        connect_motors(left, right)

    elif cmd == "NOP":
        drive(0, 0)

    elif cmd == "ERE":
        print("Error request received")
        drive(0, 0)
        Handler_TCPServer.launched = False

    elif cmd == "WIN":
        print("Route completed")
        s = Sound()
        s.speak('it deserves a twenty out of twenty')
        s.tone([(592, 550, 300), (592, 550, 300)])
        Handler_TCPServer.win = True
        Handler_TCPServer.launched = False

    elif cmd == "BIP":
        s = Sound()
        s.tone([(392, 350, 100), (392, 350, 100), (392, 350, 100)])

    else:
        print("Unknown command: ", cmd, "")
        raise NotImplemented

def stream_distance():
    us = UltrasonicSensor()
    while True:
        print(str(us.distance_centimeters))

#endregion

"""
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
"""

class Handler_TCPServer(socketserver.BaseRequestHandler):
    launched = True
    win = False

    def handle(self):

        #Boucle principale d'exécution
        while Handler_TCPServer.launched:

            # Receive a command
            data = self.request.recv(1024)

            if data:
                data.strip()
                # On décode l'instruction en un string
                data = data.decode()
                # On interprète la cmd
                interpret(data)
                # On confirme la reception de la cmd
                self.request.sendall("Command received".encode()) # À vérifier en pratique

        if Handler_TCPServer.win:
            print("Success")
            print("Done")
            stream_distance()

if __name__ == "__main__":
    stream_distance()

    HOST, PORT = robot_ip_address, 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    tcp_server.serve_forever()


