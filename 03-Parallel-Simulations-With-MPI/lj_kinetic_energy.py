import hoomd

# Initialize the simulation.
device = hoomd.device.CPU()
sim = hoomd.Simulation(device=device)
sim.create_state_from_gsd(filename='random.gsd')

# Set the operations for a Lennard-Jones particle simulation.
integrator = hoomd.md.Integrator(dt=0.005)
cell = hoomd.md.nlist.Cell()
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5
integrator.forces.append(lj)
nvt = hoomd.md.methods.NVT(kT=1.5, filter=hoomd.filter.All(), tau=1.0)
integrator.methods.append(nvt)
sim.operations.integrator = integrator

# Instantiate a ThermodyanmicQuantities object to compute kinetic energy.
thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(
    filter=hoomd.filter.All())
sim.operations.computes.append(thermodynamic_properties)

# Run the simulation.
sim.run(1000)

# Access the system kinetic energy on all ranks.
kinetic_energy = thermodynamic_properties.kinetic_energy

# Print the kinetic energy only on rank 0.
if device.communicator.rank == 0:
    print(kinetic_energy)