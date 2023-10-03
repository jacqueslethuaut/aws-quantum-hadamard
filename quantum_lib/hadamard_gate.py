from braket.circuits import Circuit

def apply_hadamard_gate(circuit, target_qubit):
    """
    Apply a Hadamard gate to a specific qubit in a quantum circuit.

    Parameters:
    - circuit (Circuit): The quantum circuit to which the Hadamard gate will be applied.
    - target_qubit (int): The index of the qubit to which the Hadamard gate will be applied.

    Returns:
    - Circuit: The new circuit with the Hadamard gate applied.
    """
    circuit.h(target_qubit)
    return circuit
