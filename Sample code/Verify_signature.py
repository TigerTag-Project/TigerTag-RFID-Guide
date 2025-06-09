from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.exceptions import InvalidSignature
import binascii

# --- Step 1: Generate private/public key pair ---
# This simulates the signing process (in reality, only TigerTag signs data)
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Export PEM for display (optional, so you can embed it elsewhere)
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
print("🔐 Public Key PEM:\n", public_pem.decode())

# --- Step 2: Create test UID + block4 + block5 ---
uid_hex = "04AABBCCDDEE1122"  # Sample UID in hex format
uid_bytes = binascii.unhexlify(uid_hex)
block4 = bytes([0x5B, 0xF5, 0x92, 0x64])  # Header block
block5 = bytes([0x00, 0x00, 0x00, 0x00])  # Extra data block
message = uid_bytes + block4 + block5

# --- Step 3: Hash the message ---
digest = hashes.Hash(hashes.SHA256())
digest.update(message)
hashed = digest.finalize()

# --- Step 4: Sign the message hash ---
# This simulates the signature on the TigerTag
signature_der = private_key.sign(hashed, ec.ECDSA(hashes.SHA256()))
r, s = decode_dss_signature(signature_der)
signature_raw = r.to_bytes(32, 'big') + s.to_bytes(32, 'big')  # Stored as raw r+s like on real tag

# --- Step 5: Verification using public key ---
try:
    # Rebuild DER signature from raw format
    r = int.from_bytes(signature_raw[:32], 'big')
    s = int.from_bytes(signature_raw[32:], 'big')
    rebuilt_signature_der = encode_dss_signature(r, s)

    # Verify signature using public key and hash
    public_key.verify(rebuilt_signature_der, hashed, ec.ECDSA(hashes.SHA256()))
    print("✅ Signature is VALID!")
except InvalidSignature:
    print("❌ Signature is INVALID!")