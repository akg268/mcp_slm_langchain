from fastmcp import FastMCP
import random
from ghdata import GhData
mcp = FastMCP("myorg-mcp-server")

@mcp.tool(description= "Get a developer available to assign on an issue")
async def assign_developer(category: str) -> str:
    """Get a developer available to assign on an issue"""
    dev_list = ["Dev1", "Dev2","Dev4", "Dev5"]
    if category == "INFRASTRUCTURE":
        return "Dev3"
    return random.choice(dev_list)

@mcp.tool(description= "Find issue category")
async def find_issue_category(issue_desc:str) -> str:
    """Find the issue category"""
    if "infra" in issue_desc.lower():
        return "INFRASTRUCTURE"
    elif "new" in issue_desc.lower():
        return "New Feature"
    elif "security" in issue_desc.lower():
        return "Security Fix"
    elif "bug" in issue_desc.lower():
        return "Bug Fix"
    elif "bug" in issue_desc.lower():
        return "Bug Fix"
    elif "document" in issue_desc.lower():
        return "Document Change"
    else:
        return "UNKNOWN"
    

@mcp.tool(description="create a github issue")
async def create_github_issue(
    title: str,
    issue_desc: str,
    category: str,
    assigned_to: str):
    """create github issue
    returns the issue id"""

    print(f"Issue created {title}::{issue_desc}::{category}::{assigned_to}")
    return random.randrange(1,10000)

if __name__ == "__main__":
    mcp.run(transport="http")

