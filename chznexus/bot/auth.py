import requests
from bs4 import BeautifulSoup

class ChapatizClient:
    def __init__(self):
        self.session = requests.Session()
        self.login_token = None

    def fetch_login_token(self, redirect_url="https://www.chapatiz.com/login/"):
        url = f"https://id.chapatiz.com/login?redirect_url={requests.utils.quote(redirect_url)}"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Referer": "https://www.chapatiz.com/",
        }
        resp = self.session.get(url, headers=headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        token_input = soup.find("input", {"name": "login_token"})
        if not token_input:
            raise RuntimeError("Login token not found in login page")
        self.login_token = token_input["value"]
        return self.login_token

    def login(self, email, password, redirect_url="https://www.chapatiz.com/login/"):
        if not self.login_token:
            self.fetch_login_token(redirect_url)

        url = "https://id.chapatiz.com/login"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Origin": "https://id.chapatiz.com",
            "Referer": f"https://id.chapatiz.com/login?redirect_url={requests.utils.quote(redirect_url)}",
        }
        payload = {
            "login_token": self.login_token,
            "login_email": email,
            "login_password": password,
            "login_redirectUrl": redirect_url,
            "login_submit": "Se connecter",
            "login_formSubmitted": "true",
        }
        resp = self.session.post(url, headers=headers, data=payload)
        resp.raise_for_status()

        # After login, the server redirects to /gameLogin?redirect_url=...
        # We can grab that redirect URL or follow it manually
        if "gameLogin" in resp.url:
            print(f"Logged in! Redirected to: {resp.url}")
        else:
            raise RuntimeError("Login may have failed or unexpected redirect.")

        return resp

    def get_session(self):
        # Return current session for reuse
        return self.session
