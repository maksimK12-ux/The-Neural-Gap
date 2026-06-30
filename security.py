import json
import os
import hashlib
import secrets

USERS_FILE = "data/users.json"


def ensure_files_exist():
    """Creates required files if they do not exist."""

    if not os.path.exists("data"): # Creates the data folder if it doesn't already exist
        os.makedirs("data")

    if not os.path.exists(USERS_FILE):  # Creates an empty JSON file for storing user data
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)



def load_users():
    """Loads all users from the JSON database."""

    ensure_files_exist()

    with open(USERS_FILE, "r") as file:
        content = file.read().strip()  # Prevents errors if the JSON file is empty
        return json.loads(content) if content else {}

def save_users(users_data):
    """Saves all users to the JSON database."""

    with open(USERS_FILE, "w") as file:  #Writes the updated user data back to the JSON file
        json.dump(users_data, file, indent=4)



def hash_password(password, salt=None):
    """
    Creates a secure password hash.
    Uses SHA-256 with a random salt.
    """

    if salt is None:  # Generates a random salt if one isn't provided
        salt = secrets.token_hex(16)

    combined = password + salt # Combines the password with the salt before hashing

    hashed = hashlib.sha256(combined.encode()).hexdigest()  # Converts the password into a secure SHA-256 hash

    return hashed, salt



def verify_password(stored_hash, stored_salt, entered_password):
    """Verifies a password against the saved hash."""

    new_hash, _ = hash_password(entered_password, stored_salt) # Hashes the entered password using the original salt

    return new_hash == stored_hash # Returns True only if both hashes match

def get_user(username):

    users = load_users()

    return users.get(username) # Retrieves the requested user, or None if they don't exist