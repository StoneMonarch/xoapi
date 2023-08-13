class VirtualMachine:
    def __init__(self, uuid: str, name: str, description: str, state: str, tags: list[str], ips: dict, vbds: list[str], ops: dict, host: str, pool: str):
        self.uuid = uuid
        self.name = name
        self.desc = description
        self.state = state
        self.tags = tags
        self.ips = ips
        self.vbds = vbds
        self.ops = ops
        self.host = host
        self.pool = pool
