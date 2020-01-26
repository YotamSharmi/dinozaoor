import math
import numpy as np

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def find_collision_wall(p_array, Lx = 100, Ly = 100):  # returns the time it takes to collide with the nearest wall
    particles = []
    times = []
    time_x, time_y = 999999999, 999999999
    for p in p_array:
        if p.vx > 0: #if the particle is moving right - calculate time to hit the right wall
            time_x = ((Lx / 2 - p.x) / (p.vx))
        elif p.vx < 0: #if the particle is moving left - calculate time to hit the left wall
            time_x = (-(Lx / 2 + p.x) / (p.vx))
        if p.vy > 0: #if the particle is moving up - calculate time to hit the "roof"
            time_y = ((Ly / 2 - p.y) / (p.vy))
        elif p.vy < 0: #if the particle is moving down - calculate time to hit the "floor"
            time_y = (-(Ly / 2 + p.y)) / (p.vy)
        times.append(min(time_x, time_y)) #appends the smaller of the two times - collision with a vertical wall (x axis calculation), or a horisontal wall (y axis calculation)
    return [min(times), times.index(min(times))] #returns the smallest (earliest) time from the list, and the index of that time which is the index of the particle with that time


def find_collision_disc(p_array, prev):  # return the time it will take for the earliest collision
    times = [99999]
    particles = [(99999, 99999)]
    for i,p in enumerate(p_array):
        for j in range(i + 1, len(p_array)):
            x_rel = p_array[j].x - p.x  # reletive position
            y_rel = p_array[j].y - p.y
            vx_rel = p_array[j].vx - p.vx  # reletive velosity
            vy_rel = p_array[j].vy - p.vy
            if (i, j) != prev and vx_rel != 0:
                #the calculation assumes a point moving at the relative velocity of the two particles, and a stationary disc with a radius equal to twice the radius of 1 discs
                #the actual calculation is the point/points where the function of a circle (x^2 + y^2 = (2*R)^2) and the linear function of the trajectory of the point meet
                m = vy_rel / vx_rel  #slope of the point
                a = 1 + m**2
                b = -2*m**2 * x_rel + 2*m*y_rel
                c = m**2 * x_rel**2 - 2 * m * x_rel * y_rel + y_rel**2 - 4
               #a, b and c come from the quadratic equation when y (in the circle function) is replaced by the point function
                try:
                    d = math.sqrt(b**2 - 4*a*c)
                except ValueError:
                    continue
                x1_temp, x2_temp = (-b + d)/(2*a), (-b - d)/(2*a)
                y1_temp, y2_temp = m * (x1_temp - x_rel) + y_rel, m * (x2_temp - x_rel) + y_rel
                time = min(distance(x1_temp, y1_temp, x_rel, y_rel), distance(x2_temp, y2_temp, x_rel, y_rel)) / math.sqrt(vx_rel ** 2 + vy_rel ** 2)
                #if vx_rel >= 0 and x_rel <= x1_temp:
                #    if vy_rel >= 0 and y_rel <= y1_temp:
                #        times.append(time)
                #    elif vy_rel <= 0 and y_rel >= y1_temp:
                #        times.append(time)
                #elif vx_rel <= 0 and x_rel >= x1_temp:
                #    if vy_rel >= 0 and y_rel <= y1_temp:
                #        times.append(time)
                #    elif vy_rel <= 0 and y_rel >= y1_temp:
                if distance(p.x + p.vx * time, p.y + p.vy * time, p_array[j].x + p_array[j].vx * time, p_array[j].y + p_array[j].vy * time)-2 < 0.000001:
                    times.append(time)
                    particles.append((i, j))
    return [min(times), particles[times.index(min(times))]]



def change_velo_wall(p, Lx=100, Ly=100):
    #    if abs(posi_x[i]) == (Lx/2):
    if abs(abs(p.x) - (Lx / 2)) < 0.0001:
        p.vx = -p.vx
    #    elif abs(posi_y[i]) == (Ly/2):
    elif abs(abs(p.y) - (Ly / 2)) < 0.0001:
        p.vy = -p.vy


def change_velo_disc(p1, p2, particles):  # need to change the i and j to the correct position in the t
    d = distance(p1.x, p1.y, p2.x, p2.y)
    theta = math.asin((p2.y - p1.y) / d)
    rot_M = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    inv_rot_m = np.array([[math.cos(-theta), -math.sin(-theta)], [math.sin(-theta), math.cos(-theta)]])

    v1 = np.array([p1.vx, p1.vy]).T
    v2 = np.array([p2.vx, p2.vy]).T

    v1_tag = np.dot(rot_M, v1)
    v2_tag = np.dot(rot_M, v2)

    u1_tag = np.array([v2_tag[0], v1_tag[1]]).T
    u2_tag = np.array([v1_tag[0], v2_tag[1]]).T

    u1 = np.dot(inv_rot_m, u1_tag)
    u2 = np.dot(inv_rot_m, u2_tag)

    particles.velocity_change2(p1, p2, u1[0], u1[1], u2[0], u2[1])





#    h = math.sqrt(((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2))
#    sinA = abs(p2.y-p1.y)/h
#    cosA = abs(p2.x-p1.x)/h
#    delta_v = (cosA) * (p2.vx - p1.vx) - (sinA) * (p2.vy - p1.vy)
#    particles.velocity_change2(p1, p2, p1.vx + cosA * delta_v, p1.vy - sinA * delta_v, p2.vx - cosA * delta_v, p2.vy + sinA * delta_v)
#    #velo_x[p[0]] = velo_x[p[0]] + cosA * delta_v
#    #velo_x[p[1]] = velo_x[p[1]] - cosA * delta_v
#    #velo_y[p[0]] = velo_y[p[0]] - sinA * delta_v
#    #velo_y[p[1]] = velo_y[p[1]] + sinA * delta_v
