import json
import os
import hashlib
import secrets

USERS_FILE = "data/users.json"


def ensure_files_exist():
    """Creates required files if they do not exist."""

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)



def load_users():
    """Loads all users from the JSON database."""

    ensure_files_exist()

    with open(USERS_FILE, "r") as file:
        return json.load(file)



def save_users(users_data):
    """Saves all users to the JSON database."""

    with open(USERS_FILE, "w") as file:
        json.dump(users_data, file, indent=4)



def hash_password(password, salt=None):
    """
    Creates a secure password hash.
    Uses SHA-256 with a random salt.
    """

    if salt is None:
        salt = secrets.token_hex(16)

    combined = password + salt

    hashed = hashlib.sha256(combined.encode()).hexdigest()

    return hashed, salt



def verify_password(stored_hash, stored_salt, entered_password):
    """Verifies a password against the saved hash."""

    new_hash, _ = hash_password(entered_password, stored_salt)

    return new_hash == stored_hash