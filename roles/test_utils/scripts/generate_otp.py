#!/usr/bin/env python3
import pyotp
import sys
import time

if __name__ == "__main__":
    # The script expects the secret key as the first argument
    if len(sys.argv) != 2:
        print("Usage: python3 generate_otp.py <secret_key>", file=sys.stderr)
        sys.exit(1)
    
    secret_key = sys.argv[1]
    
    try:
        # Generate the TOTP
        totp = pyotp.TOTP(secret_key)
        otp_code = totp.now()
        
        # Print the OTP to standard output for Ansible to capture
        print(otp_code)
        
    except Exception as e:
        print(f"Error generating OTP: {e}", file=sys.stderr)
        sys.exit(1)
