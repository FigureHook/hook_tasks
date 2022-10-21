class PlurkFormatHelper:
    @staticmethod
    def link(text: str, url: str) -> str:
        return f"{url} ({text})"

    @staticmethod
    def bold(text) -> str:
        return f"**{text}**"

    @staticmethod
    def italic(text: str) -> str:
        return f"*{text}*"
