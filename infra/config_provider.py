import json


class ConfigProvider:

    @staticmethod
    def load_config_json():
        try:
            with open(r"C:\IDE's\PyCharm Community Edition 2024.1.1\python-projects\linkedin-api-testing"
                      r"\config.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found.")

    @staticmethod
    def load_secret_json():
        try:
            with open(r"C:\IDE's\PyCharm Community Edition 2024.1.1\python-projects\linkedin-api-testing"
                      r"\secret.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found.")
