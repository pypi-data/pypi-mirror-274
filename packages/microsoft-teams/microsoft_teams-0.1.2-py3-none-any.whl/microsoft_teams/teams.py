import requests

class MicrosoftTeams:
    def __init__(self, url: str):
        self.url = url

    def send_message(self, title: str, msg: str) -> bool:
        """
        Send a message to a Microsoft Teams channel.

        Parameters:
        - title (str): The title of the message.
        - msg (str): The content of the message.

        Returns:
        - bool: True if the message was sent successfully, False otherwise.
        """
        # Construct the message to send to Microsoft Teams
        teams_message = {
            "@context": "https://schema.org/extensions",
            "@type": "MessageCard",
            "themeColor": "0076D7",
            "title": title,
            "text": msg
        }

        try:
            # Send the message to Microsoft Teams
            response = requests.post(self.url, json=teams_message)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message: {e}")
            return False