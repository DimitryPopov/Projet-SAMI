import math, random, sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'PC//src'))

import src.mocap_node as mcn
import time, TCPClient, typing

"""
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
"""

#region VARIABLES
coordonnee: typing.TypeAlias = tuple[float, float]

pc_name = "PC170" # PC name as in config file
robot_name = "Lego7" # Robot name
robot_address = "100.75.155.137" # Robot IP address

motor_speed_volt = 100
pwm = 80
def inverse_pwm(x):
    return x * 1050 / 100

client = TCPClient.TCPClient()

waypoints = [(1.0, 1.0), (4.0, 4.0)]
N = len(waypoints)

T = 0.100  # Request interval in seconds
distance_min = 0.05  # Threshold distance to consider waypoint reached

mymcn = mcn.MocapNode(pc_name)  # Connect to motion capture cameras
#endregion

"""
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
"""

#region FONCTION STATIC
def distance(position1 : coordonnee, position2 : coordonnee) -> float:
    """
    :param position1: First point
    :param position2: Second point
    :return: Euclidean distance between the two points
    """
    x1, y1 = position1
    x2, y2 = position2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def nearest_neighbor(points : list[coordonnee]) -> list[coordonnee]:
    """
    :param points: list of 2D points
    :return: path computed by nearest neighbor heuristic
    """
    n = len(points)
    visited = [False] * n
    path = []

    current = 0 # départ et arrivée du path
    path.append(current)
    visited[current] = True

    for _ in range(n - 1):
        min_dist = float('inf')
        next_node = None

        for i in range(n):
            if not visited[i]:
                d = distance(points[current], points[i])
                if d < min_dist:
                    min_dist = d
                    next_node = i

        current = next_node
        path.append(current)
        visited[current] = True

    path.append(path[0])

    return [points[i] for i in path]


def distance_matrix(points : list[coordonnee]) -> list[list[float]]:
    """
    :param points: list of 2D points
    :return: distance matrix for the given point set
    """
    n = len(points)
    dist_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = distance(points[i], points[j])

    return dist_matrix

def tour_length(tour : list[int], dist_matrix : list[list[float]]) -> float:
    """
    :param tour: ordered list of point indices
    :param dist_matrix: matrice des distances des points étudiés
    :return: total length of the current tour
    """
    n = len(tour)

    return sum(dist_matrix[tour[i]][tour[(i + 1) % n]] for i in range(n))

def swap(tour : list[int], i : int, k : int) -> list[int]:
    """
    :param tour: ordered list of point indices
    :param i: index of first point
    :param k: index of second point
    :return: tour with segment [i,k] reversed
    """
    return tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]

def two_opt(points : list[coordonnee]) -> list[coordonnee]:
    """
    :param points: list of 2D points
    :return: 2-opt optimized tour
    """
    n = len(points)
    dist_matrix = distance_matrix(points)
    best = [i for i in range(n)]
    best_dist = tour_length(best, dist_matrix)
    amelioration = True

    while amelioration:
        amelioration = False
        for i in range(1, n - 2):
            for k in range(i + 1, n - 1):
                new_tour = swap(best, i, k)
                new_dist = tour_length(new_tour, dist_matrix)

                if new_dist < best_dist:
                    best = new_tour
                    best_dist = new_dist
                    amelioration = True


    return [points[i] for i in best]


def travelling_salesman(points : list[coordonnee]) -> list[coordonnee]:
    """
    :param points: list of 2D points
    :return: TSP-optimized route
    """
    return two_opt(nearest_neighbor(points))

def set_start_position(points : list[coordonnee], start_point : coordonnee) -> list[coordonnee]:
    """
    :param points: Liste de points rangée dans l'ordre du voyageur de commerce
    :param start_point: Points de départ du robot
    :return: Liste conservant l'ordre des points, mais commençant par start_point
    Si start_point n'appartient pas à la liste donnée en paramètre alors, il renvoie simplement la liste
    """
    n = len(points) # Taille de la liste
    i = 0 # Indexe de l'start_point

    # On corrige l'index de l'start_point
    while i < n and points[i] != start_point:
        i += 1

    # Si i = n alors la liste ne contient pas le point start_point
    if i == n:
        print("Le point start_point n'appartient pas à la liste de point donnée en paramètre")
        return points

    # Sinon, on coupe la liste en deux suivant la position du point start_point et on inverse les deux morceaux
    return points[i:] + points[:i]


def get_robot_data() -> tuple[coordonnee, float]:
    """
    :return: robot 2D position and yaw angle
    """
    (x, y), direction = mymcn.getPos2DAndYaw(robot_name)
    return (x, y), direction[0]

def send_request(request : str) -> None:
    """
    :param request: command string to send to the robot
    :return: None
    """
    client.send(request)

def compute_motor_speeds(position : coordonnee, direction : float, next_point : coordonnee) -> tuple[int, int]:
    """
    :param position: robot position at time t
    :param direction: robot heading at time t
    :param next_point: next waypoint to reach
    :return: left and right motor speeds for interval [t, t+dt]
    """
    x_actuel, y_actuel = position
    x_consigne, y_consigne = next_point
    theta = direction


    # Controller constants
    k1 = 0.1
    k2 = 100 # convergence speed - do not modify
    k3 = 0.5 # must stay below 1
    k4 = 0.1
    k_s = 0.0045
    v_max = 5
    delta = 0.12
    # Compute controller variables
    x_thilde = x_consigne - x_actuel
    y_thilde = y_consigne - y_actuel
    theta_thilde = math.atan2(y_thilde, x_thilde) - theta
    d = math.sqrt(x_thilde * x_thilde + y_thilde * y_thilde)
    v = abs(d / (k1 + d) * v_max * math.cos(k4 * theta_thilde))
    #print(str(d) + " d")
    #print(str(theta_thilde)+ "theta_thilde")


    if d == 0:
        w = (v / 0.01) * math.sin(theta_thilde) + k2 * math.tanh(k3 * theta_thilde)
    else:
        w = ( v / d) * math.sin(theta_thilde) + k2 * math.tan(k3 * theta_thilde)

    # Final motor output
    left_motor_val = (delta / k_s) * (-(1 / 2) * w + (1 / delta) * v)
    right_motor_val = (delta / k_s) * ((1 / 2) * w + (1 / delta) * v)

    return int(left_motor_val), int(right_motor_val)
#endregion

"""
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
"""

def main(display : bool = False, waypoints_override = None) -> None:
    global waypoints, N
    """
    :param display: whether to show a live display of the robot path
    :param waypoints_override: Points que le robot doit visiter
    :return: None
    """

    # Initialize motion capture cameras
    mymcn.run()
    mymcn.updateModelInfo()

    # Connect to robot
    client.connect(robot_address, 9999)

    if waypoints_override:
        waypoints = waypoints_override
        N = len(waypoints)

    positions_log = [] # Robot position log
    requests_log = [] # Command log

    last_request_time = time.time() # Timestamp of last sent request
    n = 0 # Indexe du next_node sommet dans la liste

    running = True # Main loop flag

    # Apply TSP to the waypoint list
    waypoints = travelling_salesman(waypoints)

    start_time = time.time()
    print(n)
    # Main control loop
    while running:

        position, direction = get_robot_data()

        # Check if current waypoint is reached
        if distance(waypoints[n], position) < distance_min:
            # Stop the robot momentarily
            send_request("NOP;")
            time.sleep(0.1)
            send_request("BIP;")
            time.sleep(0.1)

            # Advance to next waypoint
            n += 1
            print(n)

            if n >= N:
                running = False # End main loop
                n -= 1


        if display:
            # display(positions_log, requests_log)
            raise NotImplemented

        if time.time() - last_request_time >= T:
            # Compute next motor command
            left_speed, right_speed = compute_motor_speeds(position, direction, waypoints[n])
            next_request = "MOV " + str(left_speed) + " " + str(right_speed) + ";"

            # Send the command
            send_request(next_request)

            # Update request timestamp
            last_request_time = time.time()

            # Log sent command
            requests_log.append((next_request, last_request_time))

        # Log robot state
        positions_log.append((position[0], position[1], direction, time.time()))

        #print(requests_log)
        print(waypoints)
        print(positions_log)


        # Small delay to avoid flooding the position log
        time.sleep(0.01)

    time.sleep(1)
    send_request("WIN;")

    print("WIN")

    print(time.time() - start_time)

    time.sleep(3)

    # Close robot connection
    client.close()

    # Stop motion capture
    mymcn.stop()


if __name__ == "__main__":
    # Stop the robot momentarily en cas de problème avec l'ordinateur
    l = [[random.random() * 2 + 0.5, random.random() * 2 + 0.5] for i in range(10)]
    try:
        main(waypoints_override = l)
    except Exception as e:
        send_request("ERE;")
        print("PC crash: " + str(type(e)) + str(e))
