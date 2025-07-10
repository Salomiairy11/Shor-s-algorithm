import streamlit as st
import math
import random
from math import gcd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Shor's Algorithm RSA Breaking Demo", layout="wide")

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(a, m):
    """Find modular inverse of a modulo m"""
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # Modular inverse doesn't exist
    return (x % m + m) % m

def is_prime(n):
    """Simple primality test"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_period_classical(a, n):
    """Find period of a^x mod n classically (for small numbers)"""
    if gcd(a, n) != 1:
        return None
    
    period = 1
    current = a % n
    
    while current != 1:
        current = (current * a) % n
        period += 1
        if period > n:  # Safety check
            return None
    
    return period

def generate_rsa_keys(p, q):
    """Generate RSA keys from two primes"""
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e (commonly 65537, but we'll use 3 for simplicity)
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    
    # Calculate d
    d = mod_inverse(e, phi)
    
    return (n, e), (n, d), phi

def rsa_encrypt(message, public_key):
    """Encrypt message using RSA"""
    n, e = public_key
    return pow(message, e, n)

def rsa_decrypt(ciphertext, private_key):
    """Decrypt ciphertext using RSA"""
    n, d = private_key
    return pow(ciphertext, d, n)

def simulate_quantum_period_finding(a, n):
    """Simulate quantum period finding (classical simulation)"""
    # For demonstration, we'll show the quantum process conceptually
    # then use classical method for actual computation
    
    # This would be done quantumly in reality
    period = find_period_classical(a, n)
    
    # Simulate quantum measurements and their probabilities
    measurements = []
    if period:
        # Simulate multiple quantum measurements
        for _ in range(10):
            # Quantum measurement would give multiples of 2^m/period
            # We simulate this with some randomness
            measurement = random.randint(0, 1023)  # 2^10 - 1
            fraction = measurement / 1024
            measurements.append((measurement, fraction))
    
    return period, measurements

def continued_fraction_convergents(fraction, max_denominator=1000):
    """Find continued fraction convergents"""
    convergents = []
    
    # Simple continued fraction algorithm
    a0 = int(fraction)
    if a0 == fraction:
        return [(a0, 1)]
    
    # For simplicity, we'll just try small denominators
    best_error = float('inf')
    best_convergent = (0, 1)
    
    for denom in range(1, max_denominator + 1):
        numer = round(fraction * denom)
        if denom != 0:
            error = abs(fraction - numer / denom)
            if error < best_error:
                best_error = error
                best_convergent = (numer, denom)
                convergents.append((numer, denom))
    
    return convergents[:5]  # Return first 5 convergents

# Main Streamlit App
st.title("How Shor's Algorithm Breaks RSA Encryption")
st.markdown("---")

# Sidebar for parameters
st.sidebar.header("🔧 Parameters")
st.sidebar.markdown("*Choose small primes for demonstration*")

p = st.sidebar.selectbox("Prime p:", [3, 5, 7, 11, 13, 17, 19, 23], index=2)
q = st.sidebar.selectbox("Prime q:", [3, 5, 7, 11, 13, 17, 19, 23], index=4)

if p == q:
    st.sidebar.error("p and q must be different!")
    st.stop()

# Generate RSA keys
n = p * q
public_key, private_key, phi = generate_rsa_keys(p, q)

# Introduction
st.header("Step 1: RSA Encryption Setup")
col1, col2 = st.columns(2)

with col1:
    st.subheader("RSA Key Generation")
    st.write(f"**Prime p:** {p}")
    st.write(f"**Prime q:** {q}")
    st.write(f"**n = p × q:** {n}")
    st.write(f"**φ(n) = (p-1)(q-1):** {phi}")
    st.write(f"**Public key (n, e):** ({public_key[0]}, {public_key[1]})")
    st.write(f"**Private key (n, d):** ({private_key[0]}, {private_key[1]})")

with col2:
    st.subheader("Encrypt a Message")
    message = st.number_input("Enter message (number < n):", min_value=1, max_value=n-1, value=2)
    ciphertext = rsa_encrypt(message, public_key)
    st.write(f"**Original message:** {message}")
    st.write(f"**Encrypted message:** {ciphertext}")
    
    # Verify decryption works
    decrypted = rsa_decrypt(ciphertext, private_key)
    st.write(f"**Decrypted message:** {decrypted}")
    if decrypted == message:
        st.success("RSA encryption/decryption works!")

st.markdown("---")

# The Challenge
st.header("🤔 The Challenge: Breaking RSA")
st.markdown(f"""
**The Problem:** Given only the public key (n={n}, e={public_key[1]}) and ciphertext {ciphertext}, 
can we find the original message {message}?

**Classical Approach:** Factor n = {n} into p × q
- For small n={n}, this is easy: {p} × {q} = {n}
- For large n (1000+ digits), this would take longer than the age of the universe!

**Quantum Approach:** Use Shor's algorithm to find factors efficiently!
""")

st.markdown("---")

# Shor's Algorithm Steps
st.header("Step 2: Shor's Algorithm in Action")

# Step 1: Choose random a
st.subheader("Step 2.1: Choose Random Base")
possible_a = [i for i in range(2, n) if gcd(i, n) == 1]
a = st.selectbox("Choose base a (coprime to n):", possible_a, index=0)

col1, col2 = st.columns(2)
with col1:
    st.write(f"**Chosen a:** {a}")
    st.write(f"**gcd(a, n) = gcd({a}, {n}):** {gcd(a, n)}")
    if gcd(a, n) == 1:
        st.success("a and n are coprime!")
    else:
        st.error("Need gcd(a, n) = 1")

with col2:
    st.info("**Why coprime?** If gcd(a, n) > 1, we already found a factor!")

# Step 2: Quantum Period Finding
st.subheader("Step 2.2: Quantum Period Finding")

if st.button("Run Quantum Period Finding"):
    st.markdown("### Quantum Circuit Simulation")
    
    # Show the quantum process
    with st.expander("Quantum Process Details"):
        st.markdown(f"""
        **Quantum Setup:**
        - Initialize {math.ceil(math.log2(n))} qubits for workspace
        - Initialize {2*math.ceil(math.log2(n))} qubits for counting
        - Create superposition over all possible exponents
        
        **Quantum Computation:**
        - Compute f(x) = {a}^x mod {n} for all x simultaneously
        - Apply Quantum Fourier Transform to extract period
        """)
    
    # Classical simulation of quantum period finding
    period, measurements = simulate_quantum_period_finding(a, n)
    
    if period:
        st.success(f"**Period found:** r = {period}")
        
        # Show powers of a
        powers_data = []
        for i in range(period * 2):
            power_val = pow(a, i, n)
            powers_data.append({"x": i, "a^x mod n": power_val})
        
        df = pd.DataFrame(powers_data)
        
        # Plot the periodic function
        fig = px.line(df, x="x", y="a^x mod n", title=f"Powers of {a} mod {n} (showing periodicity)")
        fig.add_vline(x=period, line_dash="dash", line_color="red", 
                     annotation_text=f"Period = {period}")
        st.plotly_chart(fig, use_container_width=True)
        
        # Verify period
        st.write(f"**Verification:** {a}^{period} mod {n} = {pow(a, period, n)}")
        
        # Step 3: Factor extraction
        st.subheader("Step 2.3: Extract Factors")
        
        if period % 2 == 0:
            st.success("Period is even!")
            
            a_to_r_half = pow(a, period // 2, n)
            st.write(f"**a^(r/2) mod n:** {a}^{period//2} mod {n} = {a_to_r_half}")
            
            if a_to_r_half != n - 1:
                st.success("✅ a^(r/2) ≢ -1 (mod n)")
                
                # Calculate factors
                factor1 = gcd(a_to_r_half - 1, n)
                factor2 = gcd(a_to_r_half + 1, n)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**gcd({a_to_r_half} - 1, {n}):** {factor1}")
                    st.write(f"**gcd({a_to_r_half} + 1, {n}):** {factor2}")
                
                with col2:
                    if factor1 > 1 and factor1 < n:
                        st.success(f"🎉 Found factor: {factor1}")
                    if factor2 > 1 and factor2 < n:
                        st.success(f"🎉 Found factor: {factor2}")
                
                # Verify factorization
                if factor1 * factor2 == n:
                    st.success(f"✅ **Factorization verified:** {n} = {factor1} × {factor2}")
                elif factor1 > 1 and n % factor1 == 0:
                    other_factor = n // factor1
                    st.success(f"✅ **Factorization found:** {n} = {factor1} × {other_factor}")
                    factor2 = other_factor
                elif factor2 > 1 and n % factor2 == 0:
                    other_factor = n // factor2
                    st.success(f"✅ **Factorization found:** {n} = {factor2} × {other_factor}")
                    factor1 = other_factor
                
                st.markdown("---")
                
                # Step 4: Break RSA
                st.header("💥 Step 3: Breaking RSA Encryption")
                
                if factor1 > 1 and factor2 > 1 and factor1 * factor2 == n:
                    st.success("🔓 **RSA Successfully Broken!**")
                    
                    # Reconstruct private key
                    p_found, q_found = factor1, factor2
                    phi_calculated = (p_found - 1) * (q_found - 1)
                    d_calculated = mod_inverse(public_key[1], phi_calculated)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("🔑 Reconstructed Private Key")
                        st.write(f"**Factors found:** {p_found}, {q_found}")
                        st.write(f"**φ(n) calculated:** {phi_calculated}")
                        st.write(f"**Private exponent d:** {d_calculated}")
                    
                    with col2:
                        st.subheader("🔓 Decrypt the Message")
                        decrypted_message = rsa_decrypt(ciphertext, (n, d_calculated))
                        st.write(f"**Encrypted message:** {ciphertext}")
                        st.write(f"**Decrypted message:** {decrypted_message}")
                        
                        if decrypted_message == message:
                            st.success("🎉 **Original message recovered!**")
                        else:
                            st.error("❌ Decryption failed")
                
            else:
                st.error("❌ a^(r/2) ≡ -1 (mod n), try different a")
        else:
            st.error("❌ Period is odd, try different a")
    else:
        st.error("❌ Could not find period")

# Summary
st.markdown("---")
st.header("📊 Summary: Classical vs Quantum")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🐌 Classical Factoring")
    st.markdown(f"""
    - **Method:** Trial division, quadratic sieve, etc.
    - **Time for n={n}:** Milliseconds
    - **Time for 2048-bit n:** > Age of universe
    - **Scalability:** Exponential
    """)

with col2:
    st.subheader("⚡ Quantum Factoring (Shor's)")
    st.markdown(f"""
    - **Method:** Quantum period finding + QFT
    - **Time for n={n}:** Microseconds
    - **Time for 2048-bit n:** Hours/Days
    - **Scalability:** Polynomial
    """)

st.markdown("---")
st.info("""
🧠 **Key Insight:** Shor's algorithm doesn't directly factor numbers. Instead, it finds the period of 
modular exponentiation, which can be used to extract factors. The quantum speedup comes from the 
Quantum Fourier Transform's ability to detect periods in superposition.
""")

st.markdown("---")
st.markdown("*This demo uses small numbers for educational purposes. Real RSA uses 2048+ bit numbers.*")