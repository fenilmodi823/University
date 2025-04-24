import argparse
import logging
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from qrw_generator import generate_qrw_bits
from aes_qrw import encrypt_with_aes, decrypt_with_aes
from metrics import avalanche_effect, ciphertext_avalanche, compute_throughput, chi_square_test


def main():
    parser = argparse.ArgumentParser(description="Quantum-Enhanced AES Demo")
    parser.add_argument('--key-bits', type=int, default=128, choices=[64, 128, 256],
                        help='Length of AES key in bits')
    parser.add_argument('--message', type=str, default="Cybersecurity meets Quantum!",
                        help='Plaintext message or path to text file')
    parser.add_argument('--iterations', type=int, default=20,
                        help='Number of trials for performance & avalanche metrics')
    parser.add_argument('--show-plot', action='store_true',
                        help='Save distribution plots to results/ directory')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    logging.info("Starting quantum AES demo")

    # 1. Key generation
    key_bits = generate_qrw_bits(args.key_bits)
    logging.info(f"Generated quantum key ({args.key_bits} bits)")

    # 2. Single encrypt/decrypt
    start_enc = time.time()
    enc = encrypt_with_aes(args.message, key_bits)
    enc_time = time.time() - start_enc
    logging.info(f"Encryption complete in {enc_time:.4f}s")

    start_dec = time.time()
    dec = decrypt_with_aes(enc['ciphertext'], key_bits)
    dec_time = time.time() - start_dec
    logging.info(f"Decryption complete in {dec_time:.4f}s")

    print(f"Original Message: {args.message}")
    print(f"Encrypted (base64): {enc['ciphertext']}")
    print(f"Decrypted: {dec}")

    # 3. Metrics over multiple trials
    avals, c_avals, throughputs = [], [], []
    for _ in trange(args.iterations, desc="Metrics Trials"):
        t0 = time.time()
        encrypt_with_aes(args.message, key_bits)
        t1 = time.time()
        throughputs.append(len(args.message) / (t1 - t0))

        # Avalanche on key (reversed bits as demo)
        avals.append(avalanche_effect(key_bits, key_bits[::-1]))
        # Avalanche on ciphertext
        c_avals.append(ciphertext_avalanche(key_bits, args.message, encrypt_with_aes))

    print(f"Average Avalanche (key): {np.mean(avals):.2f}% ± {np.std(avals):.2f}%")
    print(f"Average Ciphertext Avalanche: {np.mean(c_avals):.2f}% ± {np.std(c_avals):.2f}%")
    print(f"Mean Throughput: {np.mean(throughputs):.2f} bytes/sec ± {np.std(throughputs):.2f}")

    # 4. Randomness Test
    chi2 = chi_square_test(key_bits)
    print(f"Chi-square for key randomness: {chi2:.2f}")

    # 5. Plots
    if args.show_plot:
        os.makedirs('results', exist_ok=True)
        plt.figure()
        plt.hist(avals, bins='auto')
        plt.title('Avalanche Effect Distribution')
        plt.xlabel('Percent Flips')
        plt.ylabel('Frequency')
        plt.savefig('results/avalanche_distribution.png')
        plt.close()

        plt.figure()
        plt.hist(c_avals, bins='auto')
        plt.title('Ciphertext Avalanche Distribution')
        plt.xlabel('Percent Flips')
        plt.ylabel('Frequency')
        plt.savefig('results/ciphertext_avalanche.png')
        plt.close()

        plt.figure()
        plt.plot(throughputs)
        plt.title('Throughput over Trials')
        plt.xlabel('Trial')
        plt.ylabel('Bytes/sec')
        plt.savefig('results/throughput.png')
        plt.close()

        logging.info("Plots saved to results/ directory")

if __name__ == '__main__':
    main()