import json
from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

@dataclass
class Album:
  title: str
  artist: str
  year: int
  
  def to_json(self):
    """
    Return album in json format
    """
    d = {'title': self.title, 'artist': self.artist, 'year': self.year}
    return json.dumps(d, indent=4)
  
  def print_album(self):
    """Print album using rich console"""
    console = Console(soft_wrap=True)
    table = Table(title="1001 Albums You Must Hear Before You Die")
    table.add_column("Album title")
    table.add_column("Artist")
    table.add_column("Year")
    table.add_row(
      self.title,
      self.artist,
      str(self.year)
    )

    console.print(table)