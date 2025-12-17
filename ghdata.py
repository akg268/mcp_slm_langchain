from dataclasses import dataclass
from pydantic import ConfigDict


@dataclass
class GhData:
    """Github data for creating the Github issue"""
    model_config = ConfigDict(extra='ignore')
    title:str #Title of the issue
    issue_desc:str # issue description
    category:str #category of the issue
    assigned_to:str #assigned to dev





