from Particles import *
from ParticleFunctions import *
from animations import *
import math

def movement(N, n, x_min = -20, x_max = 20, y_min = -20, y_max = 20, vx_max = 5, vy_max = 5): #master function for driving the simulation. N is the number of collision to simulate, n is the number of particles
    particles = Particle_Array(n, x_min,x_max, y_min, y_max, vx_max, vy_max) #create a particle array object containing all of the particles
    #init(particles.array)
    prev_col = (9999999999, 999999999)#keeping the previous collision so that we won't calculate it again
    #hit = 0 |number of hits, relavent when N is not in the functionn
    ttime = 0 #total time
    #keepitup = True| relavent only when N is not in the function
    #while keepitup:| relavent only when N is not in the function
    Ek1 = 0
    for p in particles.array:
        Ek1 += 0.5 * (p.vx**2 + p.vy**2)
    fig1, axs = plt.subplots(6, 1, constrained_layout = True)
    for _ in range(N + 1):
        collision_disc = find_collision_disc(particles.array,prev_col)
        collision_wall = find_collision_wall(particles.array) #optional room size
        if collision_wall[0] < collision_disc[0]: #checks if the nearest collision is with a wall
            time = collision_wall[0] #time until the nearest collision
            ttime += time #add time to the total time
            particles.step(time) #move particles to their position at the new time
            change_velo_wall(particles.array[collision_wall[1]]) #call function to change the velocity of the disc that had just colided
            prev_col = (9999999999, 999999999)
        else:
            print('collision!', _)
            time = collision_disc[0]  # time until the nearest collision
            ttime += time  # add time to the total time
            particles.step(time)  # move particles to their position at the new time
            if particles.array[collision_disc[1][0]].x < particles.array[collision_disc[1][1]].x: #gives collision_disc the two particles in order - right one first (important for sin calculation in the function)
                change_velo_disc(particles.array[collision_disc[1][0]],particles.array[collision_disc[1][1]],particles)  # call function to change the velocities of the two discs that have just colided
            else:
                change_velo_disc(particles.array[collision_disc[1][1]], particles.array[collision_disc[1][0]],particles)
            prev_col = collision_disc[1]  # updates the collision that was just calculated to be the previus collision


        if _ % (N/5) == 0:
            bar_pos = []
            bar = []
            for i in range(50):
                bar_pos.append(i / 5)
                bar.append(0)
            for p in particles.array:
                bar[int((p.vx**2 + p.vy**2)**0.5 * 5)] += 5 / n
            axs[int(_/(N/5))].bar(bar_pos, bar, width= 10 / 50, align='edge')
            axs[int(_/(N/5))].set_title('maxwell - boltzmann after {} collisions'.format(_))
            k = 10 ** (-23)
            Eavg = Ek1 / n
            m = 1
            for x in range(0, 1000):
                plt.plot(x / 100, 4 * math.pi * (m / (2 * math.pi * Eavg))**1.5 * (x/100)**2 * math.e ** ((- m * (x/100)**2) / (2 * Eavg)), 'r,')
#            print(sum(bar))
            plt.show()



    for d in range(N):
        animateit(particles.array,particles,d,25)
    min_len = []
    for z in particles.array:
        min_len.append(len(z.anim))
#    print('missed frames:', max(min_len)-min(min_len))
#    print(particles.array)
#    fig = animation()
#    just_graph(particles.array)
#    ls = particles.array
#    ani = animat.FuncAnimation(fig, animate, frames=min(min_len),fargs=(ls),interval=15, blit=True)
#    ani.save('mymovie4.mp4', fps=30)
    Ek2 = 0
    for p in particles.array:
        Ek2 += 0.5 * (p.vx**2 + p.vy**2)
    print("Ek1 be: {} Ek2 be: {} difference: {} done!".format(Ek1,Ek2,Ek2-Ek1))


movement(20000, 400)

