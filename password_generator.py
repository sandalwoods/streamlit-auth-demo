# generate_passwords.py
import streamlit_authenticator as stauth

def generate_password_hashes():
    """Generate hashed passwords for your users"""
    
    # List of plain text passwords
    passwords = ['admin123', 'password456', 'securepass789']
    
    # Generate hashes using the new API
    hashed_passwords = stauth.Hasher.hash_list(passwords)
    # hashed_passwords = stauth.Hasher(passwords).generate()
    
    # Print the results
    print("Hashed passwords for config.yaml:")
    print("-" * 40)
    
    users = ['admin', 'jsmith', 'mjones']
    for i, (user, hashed) in enumerate(zip(users, hashed_passwords)):
        print(f"{user}: {hashed}")
    
    return hashed_passwords

if __name__ == "__main__":
    generate_password_hashes()