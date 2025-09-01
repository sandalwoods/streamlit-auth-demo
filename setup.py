# setup.py - Run this first to set up your authentication system
import streamlit_authenticator as stauth
import yaml
import os

def generate_hashed_passwords():
    """Generate hashed passwords for initial users"""
    print("🔐 Generating hashed passwords...")
    
    # Define your initial users and their plain text passwords
    users_passwords = {
        'admin': 'admin123',
        'jsmith': 'password456', 
        'mjones': 'securepass789'
    }
    
    # Get all passwords as a list
    passwords = list(users_passwords.values())
    usernames = list(users_passwords.keys())
    
    # Generate hashed passwords in batch using the new API
    hashed_passwords_list = stauth.Hasher.hash_list(passwords)
    
    # Create dictionary mapping usernames to hashed passwords
    hashed_passwords = {}
    for username, hashed in zip(usernames, hashed_passwords_list):
        hashed_passwords[username] = hashed
        print(f"✅ Generated hash for {username}")
    
    return hashed_passwords

def create_config_file():
    """Create the initial config.yaml file"""
    print("📝 Creating config.yaml file...")
    
    # Generate hashed passwords
    hashed_passwords = generate_hashed_passwords()
    
    # Create configuration dictionary
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@example.com',
                    'name': 'Administrator',
                    'password': hashed_passwords['admin']
                },
                'jsmith': {
                    'email': 'john.smith@example.com',
                    'name': 'John Smith',
                    'password': hashed_passwords['jsmith']
                },
                'mjones': {
                    'email': 'mary.jones@example.com',
                    'name': 'Mary Jones',
                    'password': hashed_passwords['mjones']
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'st_123',
            'name': 'streamlit_auth_cookie'
        },
        'pre_authorized': [
            'admin@example.com'
        ]
    }
    
    # Save to YAML file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    print("✅ config.yaml created successfully!")
    return config

def verify_installation():
    """Verify that all required packages are installed"""
    print("🔍 Verifying installation...")
    
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
        
        import streamlit_authenticator
        print("✅ Streamlit-authenticator installed")
        
        import yaml
        print("✅ PyYAML installed")
        
        import bcrypt
        print("✅ bcrypt installed")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
   create_config_file() 