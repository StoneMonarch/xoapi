class Host:
    def __init__(self, hostname: str, name_description: str, name_label: str, memory: dict, power_state: bool, resident_vms: list[str], reboot_required: bool, tags: list[str], uuid: str, pool: str):
        self.hostname = hostname
        self.name_description = name_description
        self.name_label = name_label
        self.memory = memory
        self.power_state = power_state
        self.resident_vms = resident_vms
        self.reboot_required = reboot_required
        self.tags = tags
        self.uuid = uuid
        self.pool = pool
