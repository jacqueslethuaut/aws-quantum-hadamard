# MIT License

# Copyright (c) 2023 Jacques Le Thuaut


import asyncio
from braket.aws import AwsDevice
from braket.circuits import Circuit, gates
from .hadamard_gate import apply_hadamard_gate

class QuantumCircuitManager:
    def __init__(self, config):
        self.s3_folder = (config['S3']['BucketName'], config['S3']['Prefix'])
        self.device = AwsDevice(config['Quantum']['DeviceARN'])
        self.shots = config['Quantum']['Shots']
        self.circuit = Circuit()
        self.latest_task = None 


    async def run_circuit(self):
        task = self.device.run(self.circuit, self.s3_folder, shots=1000)
        status = task.state()
        while status in ['CREATED', 'QUEUED', 'RUNNING']:
            await asyncio.sleep(5)  # Non-blocking sleep
            status = task.state()
        result = task.result()
        return result.measurement_counts


    def create_basic_circuit(self) -> Circuit:
        """
        Create a basic quantum circuit.
        """
        circuit = Circuit()
        return circuit


    def apply_gates(self, circuit: Circuit, target_qubit, entangle=False):
        """
        Apply gates to the given circuit.
        If entangle is True, it will add a CNOT gate to entangle qubits.
        """
        apply_hadamard_gate(circuit, target_qubit)
        
        if entangle:
            control_qubit = target_qubit  
            target_qubit_for_cx = target_qubit + 1  
            
            # Apply a CNOT gate to create an entangled state
            circuit.cnot(control=control_qubit, target=target_qubit_for_cx)

    def run_circuit(self, circuit: Circuit) -> str:
        """
        Run the circuit on the specified device and return the task ARN.
        """
        task = self.device.run(circuit, shots=1000)
        self.latest_task = task
        return task.id


    def get_results(self) -> dict:
        """
        Retrieve the results of the latest task.
        """
        if self.latest_task is None:
            return {"error": "No task has been run yet"}

        # Wait for the task to be completed and get results
        self.latest_task.state()
        result = self.latest_task.result()

        # Process the result as needed
        measurement_counts = result.measurement_counts
        return measurement_counts

