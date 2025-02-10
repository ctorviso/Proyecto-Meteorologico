from urllib.parse import urlencode, urlparse

class Helpers:

    @staticmethod
    def replace_url_params(url, **kwargs) -> str:
        try:
            return url.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter: {e}")

    @staticmethod
    def combine_url_params(url: str, params: dict) -> str:
        if not params:
            return url

        parsed = urlparse(url)
        separator = "&" if parsed.query else "?"

        return f"{url}{separator}{urlencode(params)}"