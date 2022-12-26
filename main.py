# Python3.10.6
from src.commands import account
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    account(prog_name="main")
