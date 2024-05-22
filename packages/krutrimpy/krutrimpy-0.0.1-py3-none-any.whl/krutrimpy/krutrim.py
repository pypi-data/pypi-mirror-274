import requests


class Response:
    def __init__(self, _response):
        self.request_object = _response
        self.full_response = self.request_object.json()
        self.response = self.full_response['choices'][0]['message']['content']

    def __str__(self):
        return f"{self.response}"

    def __repr__(self):
        return f"{self.response}"


class Krutrim:
    def __init__(self, key):
        self.key = key
        self.base_url = "https://cloud.olakrutrim.com/v1/chat/completions"
        self.model = "Krutrim-spectre-v2"

    def _request(self, _messages):
        _headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        _data = {
            "model": self.model,
            "messages": _messages
        }
        r = requests.post(self.base_url, json=_data, headers=_headers)
        r.raise_for_status()
        return r

    def send(self, message: str | list, role: str = 'assistant'):
        """
        Send a message or a list of messages to Krutrim and retrieve a response.

        Args:
            message (str or list): The message or list of messages to send to Krutrim.
            role (str, optional): Can be "system", "user", or "assistant". "assistant" by default.

        Returns:
            Response: A Response object containing the response from Krutrim.

        Raises:
            429 Too Many Requests: You're asking too much too fast! Slow down and try again later.
            500 Internal Server Error: Something went wrong on our end. Try again later, or contact us if it keeps happening.
            502 Bad Gateway: We got a bad response from someone helping us. It might be temporary, so try again.
            503 Service Unavailable: We're taking a break or a bit busy. Wait a bit and try again

        Example usage:
            >>> obj = Krutrim()
            >>> response = obj.send("What is the capital of France?")
            >>> print(response) 

            >>> messages = ["What's the weather today?", "Tell me a joke."]
            >>> response = obj.send(messages, role='user')
            >>> print(response)
        """

        if type(message) is list:
            _messages = [{'role': role, 'content': x} for x in message]
        else:
            _messages = [{'role': role, 'content': message}]

        r = self._request(_messages)
        return Response(r)
