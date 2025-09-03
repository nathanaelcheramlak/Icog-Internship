from hyperon import MeTTa

def get_schedule(graph_atoms):
    """
    Schedule tasks based on priority and deadlines using Kahn's algorithm for topological sorting.
    Returns a list of task IDs in the order they should be executed.
    """
    space = MeTTa()
    with open("metta/schedule.metta") as f:
        schedule_code = f.read()
    
    # Get graph atoms from metta
    for atom in graph_atoms:
        parsed_atom = space.parse_single(atom)
        space.space().add_atom(parsed_atom)
    print("Atoms in input space:", [str(atom) for atom in space.space().get_atoms()])

    scheduled_atoms = space.parse_all(schedule_code)
    for atom in scheduled_atoms:
        space.space().add_atom(atom)

    print("Atoms in scheduling space:", [str(atom) for atom in space.space().get_atoms()])
    scheduled_tasks = space.run("!(schedule)")
    print("Schedule:", scheduled_tasks)
    return scheduled_tasks

# metta = MeTTa()
# metta.space().add_atom(metta.parse_single("(Name Nathanael)"))
# get_schedule(metta)