from fastmcp import FastMCP
import random
from github import Github
from ghdata import GhData



mcp = FastMCP("myorg-mcp-server")

async def assign_developer(category: str) -> str:
    """Get a developer available to assign on an issue"""
    dev_list = ["Dev1", "Dev2","Dev4", "Dev5"]
    if category == "INFRASTRUCTURE":
        return "Dev3"
    return random.choice(dev_list)

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
    issue_desc: str) -> str:
    """create github issue
    returns the issue id"""
    category = await find_issue_category(issue_desc)
    assigned_dev =await assign_developer(category)
    ##############
    ## uncomment if you want the real GH call
    ##############
    #YOUR_TOKEN = "github_" 
    #REPO_PATH = "owner/repo"
    #gh = Github(YOUR_TOKEN)
    #repo = gh.get_repo(REPO_PATH)
    #issue = repo.create_issue(title=title, body=issue_desc,assignee=assigned_dev,labels=[category])
    #print(f"Issue has been created::{issue.number} :: title : {issue.title}")
    issue_id = random.randrange(1,10000)
    print(f"Issue created title {title}:: description: {issue_desc}:: category: {category}:Assigned to: {assigned_dev}")
    return f"Issue created title {title}:: description: {issue_desc}:: category: {category}:Assigned to: {assigned_dev}"

if __name__ == "__main__":
    mcp.run(transport="http")

