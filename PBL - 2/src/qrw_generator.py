from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def generate_qrw_bits(num_bits: int) -> str:
    """
    Generate a bitstring of length `num_bits` using a quantum random walk inspired method.
    """
    backend = AerSimulator()
    bits = []

    for _ in range(num_bits):
        qc = QuantumCircuit(2, 1)
        qc.h(0)            # Coin flip: superposition
        qc.cx(0, 1)        # Conditional move
        qc.measure(1, 0)   # Observe result

        qc_transpiled = transpile(qc, backend)
        result = backend.run(qc_transpiled, shots=1).result()
        counts = result.get_counts()
        bits.append(next(iter(counts)))  # Get '0' or '1'

    return ''.join(bits)


# Example use
if __name__ == "__main__":
    sample = generate_qrw_bits(16)
    print(f"Quantum Random-Walk bitstring (16 bits): {sample}")
