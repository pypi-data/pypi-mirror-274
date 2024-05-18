from dotenv import load_dotenv
import os
from eth_account import Account
from eth_account.messages import encode_defunct

# warnings.filterwarnings("ignore", message="Network .* does not have a valid ChainId.")


class KeySigner:
    def __init__(self, eth_address):
        # Load environment variables
        load_dotenv()

        eth_address = eth_address.lower()

        # Use production or development settings based on availability
        env_key = f"_{eth_address}"
        self.private_key_hex = os.getenv(env_key)
        # if null, throw error
        if not self.private_key_hex:
            raise RuntimeError(f"Private key for {eth_address} is not set.")
        self.eth_address = eth_address

    def sign_message(self, message):
        if not self.private_key_hex:
            raise RuntimeError("Private key is not set, unable to sign messages.")
        message_encoded = encode_defunct(text=message)
        signed_message = Account.sign_message(message_encoded, self.private_key_hex)
        signature = signed_message.signature.hex()
        if not signature.startswith("0x"):
            signature = "0x" + signature
        return signature

    def validate_signed_message(self, signature, message) -> bool:
        if not self.eth_address:
            raise RuntimeError(
                "Ethereum address is not set, unable to verify messages."
            )
        try:
            message_encoded = encode_defunct(text=message)
            signer_address = Account.recover_message(
                message_encoded, signature=signature
            )
            if signer_address.lower() == self.eth_address.lower():
                return True
        except ValueError as e:
            print("Signature validation failed:", str(e))
        return False

    def get_eth_address(self):
        return self.eth_address


# # Example usage
# if __name__ == "__main__":
#     message = "This is a message to sign."
#     etherscan_signature = "0x4f3d05998a46efb6981557410d3add94b2952f6a9e642907c76910c3cda6bbc558657ed0837af6f4eb918ea940158e1f10446517c05fc6dc40879e2dc17a726e1b"
#     # Create the KeySigner instance
#     key_signer = KeySigner()
#     signature = key_signer.sign_message(message)
#     print("Signature:", signature)
#     is_legit = key_signer.validate_signed_message(signature, message)
#     print("Is legit:", is_legit)
#     print(f"Etherscan signature: {etherscan_signature}")
#     print(f"Is etherscan equivalent to signature? {signature == etherscan_signature}")
#     print("---done---")
