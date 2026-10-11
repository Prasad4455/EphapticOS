# Load the .env before anything in EphapticOS.shared reads settings (data_models.py
# builds an LLM config at import). One resolver for the whole process, shared
# with EphapticOS/__init__.py — see EphapticOS.shared.env_file for the search order.
from EphapticOS.shared.env_file import load_env_file

load_env_file()
