import tkinter as tk
from tkinter import messagebox
import random
import time

from authorisation import load_users, save_users

class SequenceMemoryTest:

    def __init__(self, root, username, return_callback):

        self.root = root
        self.username = username
        self.return_callback = return_callback
