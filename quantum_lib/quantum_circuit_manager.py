# MIT License

# Copyright (c) 2023 Jacques Le Thuaut


import asyncio
from braket.aws import AwsDevice
from braket.circuits import Circuit, gates
from .quantum_circuit import QuantumCircuit

class QuantumCircuitManager:
    def __init__(self, config):
        self.s3_folder = (config['S3']['BucketName'], config['S3']['Prefix'])
        self.device = AwsDevice(config['Quantum']['DeviceARN'])
        self.shots = config['Quantum']['Shots']
        self.circuit = QuantumCircuit(2)
        self.latest_task = None 


    async def run_circuit(self):
        task = self.device.run(self.circuit.get_circuit(), self.s3_folder, shots=self.shots)
        status = task.state()
        while status in ['CREATED', 'QUEUED', 'RUNNING']:
            await asyncio.sleep(5)  # Non-blocking sleep
            status = task.state()
        result = task.result()
        return result.measurement_counts


    def apply_gates(self, target_qubit, entangle=False):
        """
        Apply gates to the internal QuantumCircuit object.
        If entangle is True, it will add a CNOT gate to entangle qubits.
        """
        self.circuit.apply_gates(target_qubit, entangle)

    def run_circuit(self) -> str:
        """
        Run the circuit on the specified device and return the task ARN.
        """
        task = self.device.run(self.circuit.get_circuit(), shots=1000)
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

