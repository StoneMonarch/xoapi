class Pool:
    def __init__(self, ha_enabled: bool, hasrs: list[str], master: bool, tags: list[str], description: str, name: str, uuid: str):
        self.ha_enabled = ha_enabled
        self.hasrs = hasrs
        self.master = master
        self.tags = tags
        self.description = description
        self.name = name
        self.uuid = uuid
