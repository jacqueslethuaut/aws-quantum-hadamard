# aws-quantum-hadamard

Notice : do not forget to create temporary credentials with the aws-vault in my case but you can adapt to your configuration

<pre><code> 
aws-vault exec jack -- env | grep AWS_ > .env
</code></pre>

Then run the cell with 
<pre><code> 
load_dotenv('.env')
</code></pre>

## Hadamard Gate
A Hadamard gate is a one-qubit gate that performs a specific linear transformation, creating a superposition of its basis states. The mathematical representation is:

$$H = \frac{1}{\sqrt{2}} 
\begin{pmatrix}
1 & 1 \\
1 & -1
\end{pmatrix}$$

Mathematically, the action of a Hadamard gate on a qubit $∣ \psi \rangle$ can be expressed as:

$$
H ∣ \psi \rangle = \frac{1}{\sqrt{2}} ( ∣ 0 \rangle + e^{i \phi} ∣ 1 \rangle )
$$

where $\phi$ is the phase of $∣\psi\rangle$.<br>
<br>
The Hadamard gate is particularly interesting because it transforms the basis states $∣0\rangle$ and $∣1\rangle$ into superpositions.<br>
<br>
Something like that:
$$
H ∣ 0 \rangle = \frac{1}{\sqrt{2}} ( ∣ 0 \rangle + ∣ 1 \rangle )
$$
and
$$
H ∣ 1 \rangle = \frac{1}{\sqrt{2}} ( ∣ 0 \rangle - ∣ 1 \rangle )
$$
The Hadamard gate is often used at the beginning of quantum algorithms to create a superposition of basis states, which then evolve differently due to subsequent quantum gates, thereby enabling the parallelism inherent in quantum computing. <br>
<br>
Reminder : Superposition refers to the ability of a quantum system to exist in multiple states simultaneously. <br>
For a single qubit $∣ \psi \rangle$,  the principle of superposition allows it to be in a linear combination of its basis states $∣ 0 \rangle$ and $∣ 1 \rangle$ 
$$
∣ \psi \rangle = \alpha ∣ 0 \rangle + \beta ∣ 1 \rangle
$$
with $|\alpha|^2+|\beta|^2=1$, $\alpha$ and $\beta$ are complex numbers

## Hadamard and Entanglement
Entanglement is a phenomenon where the states of two or more qubits become correlated in such a way that the state of one qubit immediately influences the state of another, no matter the distance separating them. An example of an entangled state for two qubits is the Bell state:
$$
∣ \Psi^+ \rangle = \frac{1}{\sqrt{2}} ( ∣ 00 \rangle + ∣ 11 \rangle )
$$
In this state, if you measure the first qubit and find it in state $∣ 0 \rangle$ , the second qubit will also be in state $∣ 0 \rangle$, and vice versa.<br>
<br>
Entanglement is often created by first putting one or more qubits into a superposition and then applying a gate that correlates them. <br>
<br>

1. Start with two qubits in the state $∣ 00 \rangle$ 
2. Apply a Hadamard gate H to the first qubit, creating a superposition:
$$
H ∣ 0 \rangle = \frac{1}{\sqrt{2}} ( ∣ 0 \rangle + ∣ 1 \rangle )
$$ 
        The system state becomes:
$$
\frac{1}{\sqrt{2}} ( ∣ 0 \rangle + ∣ 1 \rangle ) \otimes ∣ 0 \rangle = \frac{1}{\sqrt{2}} ( ∣ 00 \rangle + ∣ 10 \rangle )
$$
3. Apply a CNOT gate with the first qubit as control and the second as target. The CNOT gate flips the second qubit if the first qubit is $| 1 \rangle$ . After this step, the system becomes entangled: 

$$
∣ \Psi^+ \rangle = \frac{1}{\sqrt{2}} ( ∣ 00 \rangle + ∣ 11 \rangle )
$$

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

