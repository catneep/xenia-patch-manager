class SessionData:
  def __init__(self, toml_dict= None):
    self.fullpath = None
    self.filepath = None
    self.patches = None
    self.toml_dict = toml_dict
  
  def set_fullpath(self, name: str):
    self.fullpath = name

  def get_fullpath(self) -> str | None:
    return self.fullpath
  
  def set_filepath(self, name: str):
    self.fullpath = name

  def get_filepath(self) -> str | None:
    return self.fullpath

  def set_toml(self, toml):
    self.toml_dict = toml
  
  def get_toml(self) -> dict | None:
    return self.toml_dict

  def set_patches(self, patches: tuple):
    self.patches = patches

  def get_patches(self) -> tuple | None:
    return self.patches
