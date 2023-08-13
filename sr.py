class StorageRepository:
    def __init__(self, physical_usage: int, name_description: str, name_label: str, size: int, tags: list[str], vdis: list[str], pool: str, uuid: str):
        self.physical_usage = physical_usage
        self.name_description = name_description
        self.name_label = name_label
        self.size = size
        self.tags = tags
        self.vdis = vdis
        self.pool = pool
        self.uuid = uuid
