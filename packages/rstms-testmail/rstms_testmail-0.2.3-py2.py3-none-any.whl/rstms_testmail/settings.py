import json
from pathlib import Path


class Settings:
    def __init__(self, **kwargs):
        profile = kwargs.pop("profile", "")
        write_profile = kwargs.pop("write_profile", "")

        dir = kwargs.pop("dir", "~")
        if dir in ["~", None]:
            dir = Path.home()
        else:
            dir = Path(dir)
        self.dir = dir

        self.file = dir / f".{profile}_settings"

        old_settings = self.read()

        self._settings = {}

        for k, v in kwargs.items():
            if v is None:
                v = old_settings.get(k, None)
            self._settings[k] = v
            setattr(self, k, v)

        if write_profile:
            self.write(self._settings, dir / f".{write_profile}_settings")

    def delete(self):
        self.file.unlink()
        return

    def profiles(self):
        profiles = []
        label, _, _ = self.file.name.partition("_")
        for item in self.file.parent.iterdir():
            if not item.is_file():
                continue
            prefix, _, tail = item.name.partition("_")
            if prefix != label:
                continue
            name, _, _ = tail.partition("_")
            if name:
                profiles.append(name)
        return profiles

    def read(self):
        if self.file.is_file():
            content = self.file.read_text()
        else:
            content = "{}"
        return json.loads(content)

    def write(self, settings, file):
        file.write_text(json.dumps(settings, indent=2))

    def dict(self):
        return self._settings
