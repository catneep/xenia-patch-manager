class SessionData:
  def __init__(self, toml_dict= None):
    self.current_file = None
    self.parent_directory = None
    self.patches = None
    self.toml_dict = toml_dict

  def __repr__(self):
    return f"""SessionData()
    <<<
    \tCurrent file= '{self.current_file}'
    \tParent directory= {self.parent_directory}
    \tPatches({len(self.patches) if self.patches else 0})
    \tRoot TOML entries({len(self.toml_dict)  if self.toml_dict else 0}/4)
    >>>"""

  def set_current_file(self, name: str | None):
    if name:
      self.current_file = name.replace('\\','/')
    else:
      self.current_file = None
    print(self)

  def get_current_file(self) -> str | None:
    return self.current_file
  
  def set_parent_directory(self, name: str):
    self.parent_directory = name.replace('\\','/')

  def get_parent_directory(self) -> str | None:
    return self.parent_directory

  def set_toml(self, toml):
    self.toml_dict = toml
  
  def get_toml(self) -> dict | None:
    return self.toml_dict

  def set_patches(self, patches: tuple):
    self.patches = patches

  def get_patches(self) -> tuple | None:
    return self.patches
