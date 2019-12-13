import numpy as np
from collections import namedtuple
Particle = namedtuple("Particle", "pos_x pos_y theta weight")


class ParticleFilter(object):
    def __init__(self, x, y, theta, std, n_particles):
        par_x = np.random.normal(x, std[0], n_particles)
        par_y = np.random.normal(y, std[1], n_particles)
        par_theta = np.random.normal(theta, std[2], n_particles)
        par_weight = np.ones_like(par_x)
        self.particles = []
        self.weights = []
        for x,y,t,w in zip(par_x, par_y, par_theta, par_weight):
            self.particles.append(Particle(x,y,t,w))
            self.weights.append(w)
        self.observations = []

    def predict(self, delta_t, std_pos, velocity, yaw_rate):
        for i in range(len(self.particles)):
            if abs(yaw_rate > 1e-6):
                self.particles[i].pos_x += velocity / yaw_rate * (np.sin(self.particles[i].theta + yaw_rate * delta_t) - np.sin(self.particles[i].theta))
                self.particles[i].pos_y += velocity / yaw_rate * (np.cos(self.particles[i].theta) - np.cos(self.particles[i].theta + yaw_rate * delta_t))
            else:
                self.particles[i].pos_x += delta_t * velocity * np.cos(self.particles[i].theta)
                self.particles[i].pos_y += delta_t * velocity * np.sin(self.particles[i].theta)
            self.particles[i].theta += delta_t * yaw_rate
            
            self.particles[i].pos_x += np.random.normal(self.particles[i].pos_x, std[0], 1)
            self.particles[i].pos_y += np.random.normal(self.particles[i].pos_y, std[0], 1)

    def dataAssociation(predicted):
        for iobs in range(len(self.observations)):
            distance = np.inf
            for ipred in range(len(predicted)):
                temp_dist = np.linalg.norm(np.asarray(predicted[ipred])-np.asarray(self.observations[iobs]))
                if temp_dist < distance:
                    distance = temp_dist
                    self.observations[iobs].id = predicted[ipred].id
            if distance==np.inf:
                raise RuntimeError "Could not find nearest point in dataAssociation"
    
    def updateWeights(sensor_range, std_landmark):
        for ipart in range(len(self.particles)):
            x = self.particles[ipart].pos_x
            y = self.particles[ipart].pos_y
            theta = self.particles[ipart].theta
            


                

if __name__ == "__main__":
    PF = ParticleFilter(1,2,90,[0.1,0.2,3],1)
    print(PF.particles)
    pass


