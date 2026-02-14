class ECSWorld:
    def __init__(self):
        self._next_entity = 1
        self.components: dict[type, dict[int, object]] = {}

    def create_entity(self) -> int:
        eid = self._next_entity
        self._next_entity += 1
        return eid

    def add_component(self, entity: int, component: object) -> None:
        comp_type = type(component)
        if comp_type not in self.components:
            self.components[comp_type] = {}
        self.components[comp_type][entity] = component

    def get_component(self, comp_type: type):
        return self.components.get(comp_type, {})

    def remove_entity(self, entity: int) -> None:
        for comp_map in self.components.values():
            comp_map.pop(entity, None)
