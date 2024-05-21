from gitsint import *

from git import Repo
import os
import json

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings
from detect_secrets.settings import transient_settings

# Get the directory of the current script file
current_dir = os.path.dirname(__file__)

# Navigate from the current directory to the root of your project
root_dir = os.path.abspath(os.path.join(current_dir, "../../.."))



async def fetch_repository(user, client, out, args):
    repos = {}
    
    #https://api.github.com/users/octocat/repos
    # TODO if repo > 100
    username = user["login"]
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    headers = {}
    page = 1
    if args.token:
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': "Bearer {}".format(args.token[0]),
            'X-GitHub-Api-Version' : '2022-11-28',
        }
        if args.private:
            url = f"https://api.github.com/user/repos?per_page=100"

    repos = await client.get(url, headers=headers)
    print(url)
    return repos.json()

async def repository(user, client, out, args):
    
    name = "repository"
    domain = "repository"
    method="api"
    frequent_rate_limit=True
    username = user["login"]
    authors = []
    emails = []
    
 
    try:

        repos = await fetch_repository(user, client, out, args)

        # Define the folder path at the root of your project
        RESULTS_FOLDER = os.path.join(root_dir, f"results/{username}")
        # Ensure that the folder exists, create it if it doesn't
        os.makedirs(RESULTS_FOLDER, exist_ok=True)
        
        _repos = []
        _authors = []
        _emails = []
        #print(repos)
        
        processed_repos = []
        

            # Only include forked repositories
            
        if args.fork == False:
            # Only include forked repositories
            repos = [repo for repo in repos if not repo['fork']]
            
        if args.size:
            repos = [repo for repo in repos if repo['size'] < args.size and repo['size'] > 0]
        else:
            repos = [repo for repo in repos if repo['size'] < 500000 and repo['size'] > 0]
        # # Don't clone repositories with a size > 50000 bytes
        # repos = [repo for repo in repos if repo['size'] < 500000]

        # # Filter out private repositories if the user doesn't have a token
        # repos = [repo for repo in repos if (not args.private and not repo['private'] and not args.token) or (args.private and repo['private'])]
        
        print(len(repos))
        
        # If no repositories found
        if len(repos) < 1:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                "rateLimit": False,
                "exists": False,
                "others": {"Message": "No repositories found for this user.","errorMessage" : "No repositories found for this user."},
                "data": None,
                })
            return
        
        for repo in repos:
            
            _repo = {
                "name" : repo['name'],
                "description" : repo['description'],
                "scope" : "Private" if repo['private'] else "Public",
                "authors" : [],
                "emails" : [],
            }
            try:
                repo_path = os.path.join(RESULTS_FOLDER, repo['name'])
                if os.path.exists(repo_path):
                    # Repo is already cloned, check for updates
                    repo = Repo(repo_path)
                    #repo.remotes.origin.pull()
                else:
                    # Clone the repo with clone url
                        try:
                            if args.private:
                                Repo.clone_from("https://{0}@github.com/{1}/{2}.git".format(args.token[0], username, repo['name']), repo_path)    
                            else:                        
                                Repo.clone_from(repo['clone_url'], repo_path)
                        except Exception as e:
                            out.append({
                                "name": name,
                                "domain": domain,
                                "method": method,
                                "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "others": {"Message": "Clone failed.", "errorMessage": str(e)},
                                "data": None,
                            })
                repo = Repo(repo_path)

                authors = []
                emails = []
                messages = []
                
                for commit in repo.iter_commits(all=True):
                    message = str(commit.message).strip()
                    author = commit.author.name
                    email = commit.author.email
                    committer = commit.committer.name  # Get the committer's name
                    committer_email = commit.committer.email  # Get the committer's email


                    if committer not in authors:
                        authors.append(committer)
                        _repo["authors"].append(committer)
                        
                    if committer_email not in emails:
                        emails.append(committer_email)
                        _repo["emails"].append(committer_email)

                    if author not in authors:
                        authors.append(author)
                        _repo["authors"].append(author)
                        
                    if author not in _authors:
                        _authors.append(author)
                    
                    if email not in emails:
                        emails.append(email)
                        _repo["emails"].append(email)
                        
                    if email not in _emails:
                        _emails.append(email)

                    if message not in messages:
                        messages.append(message)
                        
                _repo["authors"] = json.dumps(authors)
                _repo["emails"] = json.dumps(emails)
                _repo["messages"] = json.dumps(messages)

                _repos.append(_repo)
                
            except Exception as e:
                print(e,_repo,len(_repos))
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "others": {"Message ": "Rate limit exceeded.","errorMessage" : "Rate limit exceeded."},
                    "data": json.dumps(_repos),
                    })
    
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "others": None,
                    "data": json.dumps(_repos),
                    })
        # If no authors or emails found in global search
        
        if (len(_authors) < 1) and (len(_emails) < 1):
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "others": {"Message": "No authors or emails found for this user.","errorMessage" : "No authors or emails found for this user."},
                        "data": None,
                        })
        else:
            print("ok")
            
            out.append({"name": "repository","domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                "rateLimit": False,
                "exists": True,
                "others": None,
                "data": [{"emails_found": json.dumps(_emails)}, {"authors_found": json.dumps(_authors)}]
                })

    except Exception as e:
        print(e)
        print("nok")
        
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "data": None,
                    "others":  {"Message": "No authors or emails found for this user.","errorMessage" : "No authors or emails found for this user."}})
