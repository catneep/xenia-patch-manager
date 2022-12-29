from dataclasses import dataclass

@dataclass(frozen= False, order= False)
class Patch:
  name: str
  data: dict

  def toggle_state(self, state: bool) -> bool:
    print(f'toggled "{self.name}": {state}')
    self.data['is_enabled'] = state
    return state
