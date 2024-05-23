import typer
import requests
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='.env.public')
app = typer.Typer()

@app.command()
def call_api(git_url: str,git_branch:str,app_name:str):
    """
    Call the API with the provided git_url.
    """
    print("git url",git_url)
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    body = {
        "git_req": {
            "git_url": git_url,
            "git_branch":git_branch,
            "app_name":app_name
        }
    }
    #url = os.getenv("API_URL")
    url="https://code-explorer-pre-prod.dal2a.ciocloud.nonprod.intranet.ibm.com/api/github"
    print("url",url)
    response = requests.post(url, json=body, headers=headers)
    print ("response",response)
    if response.status_code == 201:
        typer.echo("API call successful!")
        typer.echo("Response:")
        typer.echo(response.json())
    else:
        typer.echo(f"API call failed with status code: {response.status_code}")
        typer.echo("Response:")
        typer.echo(response.text)

if __name__ == "__main__":
    app()
