# fridaylabs/fridaylabs.py

import requests

class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class FridayLabs:
    def __init__(self, api_key, api_url, verbose=False):
        self.api_key = api_key
        self.api_url = api_url
        self.verbose = verbose

    def chat_completion(self, model, messages, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }

        if self.verbose:
            print(f"{Colors.HEADER}{Colors.BOLD}Sending Request to FridayLabs API...{Colors.ENDC}")

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            if self.verbose:
                print(f"{Colors.OKGREEN}{Colors.BOLD}Request successful!{Colors.ENDC}")
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            if self.verbose:
                print(f"{Colors.FAIL}{Colors.BOLD}HTTP error occurred: {Colors.ENDC}{http_err}")
                self.suggest_solution(response)
            if response.status_code == 403:
                return {"error": "Access to this model is restricted. Please check your access rights."}
            raise

        except requests.exceptions.RequestException as req_err:
            if self.verbose:
                print(f"{Colors.FAIL}{Colors.BOLD}Request error occurred: {Colors.ENDC}{req_err}")
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. Check your network connection.{Colors.ENDC}")
                print(f"{Colors.WARNING}2. Verify the API URL: {self.api_url}{Colors.ENDC}")
                print(f"{Colors.WARNING}3. Ensure your API key is correct.{Colors.ENDC}")
            raise

        except Exception as err:
            if self.verbose:
                print(f"{Colors.FAIL}{Colors.BOLD}An unexpected error occurred: {Colors.ENDC}{err}")
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. Check the payload for correctness.{Colors.ENDC}")
                print(f"{Colors.WARNING}2. Verify the API endpoint is correct.{Colors.ENDC}")
                print(f"{Colors.WARNING}3. Ensure the server is running and accessible.{Colors.ENDC}")
            raise

    def suggest_solution(self, response):
        if self.verbose:
            print(f"{Colors.FAIL}Response content: {response.content}{Colors.ENDC}")

            status_code = response.status_code
            if status_code == 400:
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. Check the request payload for errors.{Colors.ENDC}")
                print(f"{Colors.WARNING}2. Ensure all required fields are included.{Colors.ENDC}")
            elif status_code == 401:
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. Verify your API key is correct.{Colors.ENDC}")
                print(f"{Colors.WARNING}2. Ensure your API key has the necessary permissions.{Colors.ENDC}")
            elif status_code == 403:
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. Ensure your API key has the required access rights.{Colors.ENDC}")
                print(f"{Colors.WARNING}2. Contact support if the issue persists.{Colors.ENDC}")
            elif status_code == 404:
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. Verify the API endpoint URL: {self.api_url}{Colors.ENDC}")
                print(f"{Colors.WARNING}2. Check the API documentation for the correct URL.{Colors.ENDC}")
            elif status_code == 500:
                print(f"{Colors.WARNING}Possible solutions:{Colors.ENDC}")
                print(f"{Colors.WARNING}1. The server might be down, try again later.{Colors.ENDC}")
                print(f"{Colors.WARNING}2. If the issue persists, contact support.{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}An error occurred with status code: {status_code}{Colors.ENDC}")
                print(f"{Colors.WARNING}Refer to the API documentation for more details.{Colors.ENDC}")
