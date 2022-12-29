class SessionData:
  def __init__(self, toml_dict= None):
    self.filepath = None
    self.toml_dict = toml_dict
  
  def set_filepath(self, name: str):
    self.filepath = name

  def get_filepath(self) -> str | None:
    return self.filepath

  def set_toml(self, toml):
    self.toml_dict = toml
  
  def get_toml(self) -> dict | None:
    return self.toml_dict
