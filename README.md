# aws-quantum-hadamard

Notice : do not forget to create temporary credentials with the aws-vault in my case but you can adapt to your configuration

> aws-vault exec jack -- env | grep AWS_ > .env

Then run the cell with load_dotenv('.env')


## Shot

The term "shots" in quantum computing refers to the number of times a quantum circuit is executed to collect statistical data. When you run a quantum algorithm on a real or simulated quantum device, the output is probabilistic. This is in stark contrast to classical computing, where running the same program with the same input will always produce the same output.

In the context of the quantum circuit, each "shot" corresponds to a single run of the circuit, followed by a measurement of the qubits. These measurements are probabilistic, and running the circuit multiple times (i.e., using multiple shots) will give you a distribution of outcomes.

## Number of Shots

The "right" number of shots depends on several factors, including the specific problem you're trying to solve, the precision you need in your results, and the computational resources available to you. Here's a general guideline:

Exploratory Phase: If you're just exploring or debugging a quantum circuit, a smaller number of shots (e.g., 100–1000) may be sufficient.

Statistical Significance: For results that require statistical significance, you may need a larger number of shots. This could range from thousands to millions of shots, depending on the problem. For example, in quantum chemistry calculations, one often needs a large number of shots to estimate expectation values accurately.

Resource Constraints: More shots require more computational resources, both in terms of time and money. Quantum hardware, whether actual quantum devices or high-fidelity simulators, can be expensive to use.

Error Mitigation: If you're using techniques for error mitigation, you might need to adjust the number of shots accordingly.

Problem-Specific Needs: Some algorithms or protocols may have specific requirements for the number of shots to achieve a certain confidence level or error rate.

