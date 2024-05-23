class Info:
    
    title: dict[str, str]
    icon: dict[str, str]
    url: dict[str, str]
    
    def __init__(self, title: dict[str, str] = {}, icon: dict[str, str] = {}, url: dict[str, str] = {}) -> None:
        """DOCSTRING"""
        self.title = title
        self.icon = icon
        self.url = url

    def update(self, key: str, window_handle, value: str) -> None:
        """Update info"""
        if not hasattr(self, key):
            raise KeyError

        getattr(self, key)[window_handle] = value

    def to_dict(self) -> dict[str, dict[str, str]]:
        """DOCSTRING"""
        return {"title": self.title, "icon": self.icon, "url": self.url}
