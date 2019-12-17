import numpy as np
from numpy import sin, cos
from collections import namedtuple
from matplotlib import pyplot as plt
from dataclasses import dataclass

@dataclass
class Particle:
    x: float
    y: float
    theta: float
    weight: float

@dataclass
class Landmark:
    x: float
    y: float
    id: int
    
EPS = 1E-90

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
        self.landmarks = []
        self.landmarks.append(Landmark(10, 10, 1))
        self.landmarks.append(Landmark(15, 10, 2))
        self.landmarks.append(Landmark(20, 20, 3))

    def predict(self, delta_t, std_pos, velocity, yaw_rate):
        for i in range(len(self.particles)):
            if abs(yaw_rate > 1e-6):
                self.particles[i].x += velocity / yaw_rate * (sin(self.particles[i].theta + yaw_rate * delta_t) - sin(self.particles[i].theta))
                self.particles[i].y += velocity / yaw_rate * (cos(self.particles[i].theta) - cos(self.particles[i].theta + yaw_rate * delta_t))
            else:
                self.particles[i].x += delta_t * velocity * cos(self.particles[i].theta)
                self.particles[i].y += delta_t * velocity * sin(self.particles[i].theta)
            self.particles[i].theta += delta_t * yaw_rate
            
            self.particles[i].x += np.random.normal(self.particles[i].x, std_pos[0], 1)
            self.particles[i].y += np.random.normal(self.particles[i].y, std_pos[0], 1)

    def dataAssociation(self, predicted, observations):
        for iobs in range(len(observations)):
            distance = np.inf
            for pred in predicted:
                temp_dist = np.linalg.norm(np.asarray(pred)-np.asarray(observations[iobs]))
                if temp_dist < distance:
                    distance = temp_dist
                    observations[iobs].id = pred.id
            if distance==np.inf:
                raise RuntimeError
    
    def pov2map(self, thing, povthing):
        xM = cos(povthing.theta) * thing.x - sin(povthing.theta)*thing.y + povthing.x
        yM = sin(povthing.theta) * thing.x + cos(povthing.theta)*thing.y + povthing.y
        return (xM, yM)

    def updateWeights(self, sensor_range, std_landmark):
        for ipart in range(len(self.particles)):
            self.particles[ipart].weight = 1
            self.weights[ipart] = 1
            lmark_M = self.landmarks
            for lmark in self.landmarks:
                # Make subset of landmarks depending on sensor range
                pass

            obs_M = []
            for obs in self.observations:
                obs_M.append(Landmark(*(self.pov2map(obs, self.particles[ipart]), (0,))))
            
            self.dataAssociation(lmark_M, obs_M)
            
            # Now that observations and landmarks are associated, compute the weight
            for obs in obs_M:
                for lmark in lmark_M:
                    sig_x = std_landmark[0]
                    sig_y = std_landmark[1]

                    exponent = -((obs.x - lmark.x) * (obs.x - lmark.x) / (2 * sig_x * sig_x) +
                                 (obs.y - lmark.y) * (obs.y - lmark.y) / (2 * sig_y * sig_y)) 

                    Pxy = 1 / (2 * np.pi * sig_x * sig_y) * np.exp(exponent)
                    if (Pxy < EPS): Pxy = EPS
                    self.particles[ipart].weight *= Pxy
                    self.weights[ipart]          *= Pxy

    def resample(self):
        probs = [part.weight for part in self.particles]
        self.particles = list(np.random.choice(self.particles, size=len(self.particles), p=probs))


if __name__ == "__main__":
    PF = ParticleFilter(10,-10,90,[3,3,5],10)
    # Initially, we observe everything exactly, add noise later...
    # obsv = [o for o in PF.landmarks.keys()]
    
    dt = 1
    velocity = 1    # m/s
    theta = 0       # rad 
    yaw_rate = 0    # not turning
    std_pos = [1,1] # noise

    PF.observations.append(Landmark(0,20,0))
    PF.observations.append(Landmark(5,20,0))
    PF.observations.append(Landmark(10,30,0))
    
    xs = [p.x for p in PF.particles]
    ys = [p.y for p in PF.particles]
    plt.scatter(xs,ys,color='r')

    oxs = [p.x for p in PF.observations]
    oys = [p.y for p in PF.observations]
    plt.scatter(oxs,oys,color='b')

    lxs = [p.x for p in PF.landmarks]
    lys = [p.y for p in PF.landmarks]
    plt.scatter(lxs,lys,color='k')

    plt.show()

    PF.predict(delta_t = dt, std_pos = std_pos, velocity = velocity, yaw_rate = yaw_rate)

    def update_obs(obs, delta_t, velocity, theta):
        # Observation moves on the opposite side of the particle 
        for o in obs:
            o.x = o.x - delta_t*velocity*cos(theta)
            o.y = o.y - delta_t*velocity*sin(theta)

    for i in range(5):
        xs = [p.x for p in PF.particles]
        ys = [p.y for p in PF.particles]
        plt.scatter(xs,ys,color='r')
        
        update_obs(PF.observations, delta_t=dt, velocity=velocity, theta=theta)
        oxs = [p.x for p in PF.observations]
        oys = [p.y for p in PF.observations]
        plt.scatter(oxs,oys,color='b')

        lxs = [p.x for p in PF.landmarks]
        lys = [p.y for p in PF.landmarks]
        plt.scatter(lxs,lys,color='k')

        plt.show()
    pass


