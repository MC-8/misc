import numpy as np
from math import sin, cos, exp
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
    
EPS = 1E-6

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
                self.particles[i].x = self.particles[i].x  +  velocity / yaw_rate * (sin(self.particles[i].theta + yaw_rate * delta_t) - sin(self.particles[i].theta))
                self.particles[i].y = self.particles[i].y  +  velocity / yaw_rate * (cos(self.particles[i].theta) - cos(self.particles[i].theta + yaw_rate * delta_t))
            else: 
                self.particles[i].x = self.particles[i].x  +  delta_t * velocity * cos(self.particles[i].theta)
                self.particles[i].y = self.particles[i].y  +  delta_t * velocity * sin(self.particles[i].theta)
            self.particles[i].theta = self.particles[i].theta  +  delta_t * yaw_rate
            self.particles[i].x = self.particles[i].x + np.random.normal(self.particles[i].x, std_pos[0], 1)
            self.particles[i].y = self.particles[i].y + np.random.normal(self.particles[i].y, std_pos[1], 1)

    def dataAssociation(self, predicted, observations):
        for iobs in range(len(observations)):
            distance = np.inf
            for pred in predicted:
                temp_dist = np.linalg.norm(np.asarray((pred.x, pred.y))-np.asarray((observations[iobs].x, observations[iobs].y)))
                if temp_dist < distance:
                    distance = temp_dist
                    observations[iobs].id = pred.id
            if distance==np.inf:
                raise RuntimeError
    
    def pov2map(self, thing, povthing):
        xM = cos(povthing.theta) * thing.x - sin(povthing.theta)*thing.y + povthing.x
        yM = sin(povthing.theta) * thing.x + cos(povthing.theta)*thing.y + povthing.y
        return xM[0], yM[0]

    def updateWeights(self, std_landmark):
        for ipart in range(len(self.particles)):
            self.particles[ipart].weight = 1
            self.weights[ipart] = 1
            lmark_M = self.landmarks
            for lmark in self.landmarks:
                # Make subset of landmarks depending on sensor range
                pass

            obs_M = []

            # For now we use map-observations, not POV versions
            for obs in self.observations:
                obs_M.append(Landmark(obs.x-self.particles[ipart].x, obs.y-self.particles[ipart].y, 0))

            self.dataAssociation(lmark_M, obs_M)
            
            # Now that observations and landmarks are associated, compute the weight
            for obs in obs_M:
                for lmark in lmark_M:
                    sig_x = std_landmark[0]
                    sig_y = std_landmark[1]

                    exponent = -((obs.x - lmark.x) * (obs.x - lmark.x) / (2 * sig_x * sig_x) +
                                 (obs.y - lmark.y) * (obs.y - lmark.y) / (2 * sig_y * sig_y)) 

                    Pxy = 1 / (2 * np.pi * sig_x * sig_y) * exp(exponent)
                    if (Pxy < EPS): Pxy = EPS
                    self.particles[ipart].weight *= Pxy
                    self.weights[ipart]          *= Pxy

    def resample(self):
        probs = [part.weight for part in self.particles]
        probs /= np.asarray(probs).sum()
        self.particles = list(np.random.choice(self.particles, size=len(self.particles), p=probs))


if __name__ == "__main__":
    gt = [2, -2, 0, 0, 0] # ground truth: x,y,velocity,theta,yawrate
    PF = ParticleFilter(gt[0], gt[1], gt[2], [1,1,1], 1000)
    
    dt = 1                           # time step [s]
    velocity = gt[2]       # m/s
    theta    = gt[3]       # rad 
    yaw_rate = gt[4]       # rad/s
    std_pos  = [1,1]                 # sensor noise stddev
    N_STEPS  = 100

    # Initially, we observe everything exactly (with respect to vehicle), TODO add noise to observation
    for l in PF.landmarks:
        PF.observations.append(Landmark(l.x - gt[0], l.y - gt[1], 0))

    def update_obs(obs, delta_t, velocity, theta):
        # Observation moves on the opposite side of the particle 
        for o in obs:
            o.x = o.x - delta_t*velocity*cos(theta)
            o.y = o.y - delta_t*velocity*sin(theta)

    def update_ground_truth(gt, delta_t):
        gt[0] += delta_t*gt[2]*cos(gt[3])
        gt[1] += delta_t*gt[2]*sin(gt[3])
        gt[3] += delta_t*gt[4]

    for i in range(N_STEPS):
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
        
        # Update everything
        PF.predict(delta_t = dt, std_pos = std_pos, velocity = velocity, yaw_rate = yaw_rate)
        PF.updateWeights(std_landmark = [2,2])
        PF.resample()
        maxweight = max([x.weight for x in PF.particles])
        best_guess = [x for x in PF.particles if x.weight==maxweight][0]
        print(f"Ground truth is \t{gt[0]}, {gt[1]}\n")
        print(f"Best guess is \t{best_guess.x}, {best_guess.y}\n")
        update_ground_truth(gt, delta_t = dt)
        update_obs(PF.observations, delta_t=dt, velocity=velocity, theta=theta)
    pass


