import numpy as np
import math
import rebound

def setupParticles():

	aNeptune = sim.particles[4].a
	a_initial = np.random.uniform(1.82 * aNeptune, 1.86 * aNeptune, numberOfTestParticles)
	e_initial = np.random.uniform(0, 1, numberOfTestParticles)

	i_initial = np.random.rayleigh(rayleighScale, numberOfTestParticles)
	i_initial /= np.max(i_initial); i_initial *= (np.pi / 2) / i_initial.max()  # scale to 0-90 degrees

	M_initial = np.random.uniform(-(np.pi), np.pi, numberOfTestParticles)
	omega_initial = np.random.uniform(-(np.pi), np.pi, numberOfTestParticles)
	Omega_initial = np.random.uniform(-(np.pi), np.pi, numberOfTestParticles)

	particleNumber = 0
	for (a, e, i, M, omega, Omega) in zip(a_initial, e_initial, i_initial, M_initial, omega_initial, Omega_initial):
		particleNumber += 1
		sim.add(a = a, hash = 'p{0:04d}'.format(particleNumber), e = e, inc = i, M = M, omega = omega, Omega = Omega)
		
	sim.N_active = numberOfActiveParticles

numberOfActiveParticles = 5 # sun & major planets

useInitialCheckpoint = False

initialCheckpoint = 'data/simCheckpoints/checkpoint.bin'
initialIntegrationRun = 1
numberOfTestParticles = 3000
rayleighScale = 0.1

integrationTime = 1e4 # 1e7

if not useInitialCheckpoint:
	sim = rebound.Simulation()
	sim.units = ('yr', 'AU', 'Msun')

	sim.add("Sun")
	sim.particles[0].hash = "Sun"
	sim.add("Jupiter")
	sim.particles[1].hash = "Jupiter"
	sim.add("Saturn")
	sim.particles[2].hash = "Saturn"
	sim.add("Uranus")
	sim.particles[3].hash = "Uranus"
	sim.add("Neptune")
	sim.particles[4].hash = "Neptune"

	#sim.save('4_major_planets.bin')

	sim.move_to_com()
	sim.integrator = "whfast"
	sim.t = 0
	sim.dt = 0.1
	sim.collision_resolve = "merge"

	setupParticles()

else:
	sim = rebound.Simulation().from_file(initialCheckpoint)
	

integrationRun = initialIntegrationRun

heliocentricMaxDistance = 1000.
heliocentricMinDistance = 5.
maxD = heliocentricMaxDistance ** 2
minD = heliocentricMinDistance ** 2

outputPoints = int(integrationTime / 1000)

times = np.linspace(sim.t, sim.t + integrationTime, outputPoints)

for i, time in enumerate(times):
	try:
		sim.integrate(time)
		
		fileName = '{0:.0f}'.format(sim.t)
		
		sim.save('data/simResults/' + fileName)
		
		neptuneMeanLongitude = sim.particles[4].l

		with open('data/simCopyPlanets/' + fileName, "a") as out:
			for index, p in enumerate(sim.particles[1:5]):
			  out.write(','.join(map(str,
				(int(sim.t), p.hash.value, index, p.x, p.y, p.z, p.vx, p.vy, p.vz, p.a, p.e, p.inc, p.Omega, p.omega, p.pomega, p.l)
				)) + '\n')
			  
		with open('data/simCopyParticles/' + fileName, "a") as out:
			for p in sim.particles[5:]:
			  out.write(','.join(map(str,
				(int(sim.t), p.hash.value, p.a, p.e, p.inc, p.Omega, p.omega, p.pomega, p.l, p.f, 5 * p.l - 2 * neptuneMeanLongitude - 3 * p.pomega)
				)) + '\n')
				
		print('Current result {0:.0f}.bin'.format(sim.t))
	except (rebound.Escape, rebound.Encounter) as error:
		pass    

sim.save("data/simCheckpoints/checkpoint.bin".format(integrationRun))

print('Particles remaining : {0:d}'.format(sim.N - numberOfActiveParticles))
print('Integration time : {0:.2f}  Myr'.format(sim.t / 1e6))
print('Integration run: {0:d}'.format(integrationRun))



