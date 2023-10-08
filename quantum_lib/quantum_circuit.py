# MIT License

# Copyright (c) 2023 Jacques Le Thuaut

from braket.circuits import Circuit

class QuantumCircuit:
    def __init__(self, num_qubits):
        self.circuit = Circuit()
        self.num_qubits = num_qubits

    def apply_hadamard_gate(self, target_qubit):
        if target_qubit >= self.num_qubits:
            raise ValueError("Invalid qubit index")
        self.circuit.h(target_qubit)

    def apply_gates(self, target_qubit, entangle=False):
        """
        Apply gates to the quantum circuit.
        If entangle is True, it will add a CNOT gate to entangle qubits.
        """
        self.apply_hadamard_gate(target_qubit)
        
        if entangle:
            if target_qubit >= self.num_qubits - 1:
                raise ValueError("Cannot entangle the last qubit with a non-existent qubit")
            
            control_qubit = target_qubit  
            target_qubit_for_cx = target_qubit + 1  
            
            # Apply a CNOT gate to create an entangled state
            self.circuit.cnot(control=control_qubit, target=target_qubit_for_cx)

    def get_circuit(self):
        return self.circuit
