class VDI:
    def __init__(self, name_label: str, name_description: str, parent: str, size: int, tags: list[str], usage: int, sr: str, vbds: list[str], pool: str, uuid: str):
        self.name_label = name_label
        self.name_description = name_description
        self.parent = parent
        self.size = size
        self.tags = tags
        self.usage = usage
        self.sr = sr
        self.vbds = vbds
        self.pool = pool
        self.uuid = uuid
