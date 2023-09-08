import requests, json
from flask import Flask, redirect, request, render_template, url_for
import pandas as pd
from git import Repo, Commit
import urllib.request
from datetime import datetime,date, timedelta
from urllib.request import urlopen
import dateutil.relativedelta

app = Flask(__name__)

BASE_URL = 'https://api.github.com'
ORG = 'liquiloans'

HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer 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',
    'X-GitHub-Api-Version': '2022-11-28'
}

repo_list = []
@app.route('/',methods=['GET'])        
def get_all_repo():
    response = requests.get(f'{BASE_URL}/orgs/{ORG}/repos', headers=HEADERS)
    repos_df = pd.json_normalize(response.json())
    fin = []
    fin = repos_df['name']
    if len(repo_list) == 0:
        for b in fin:
            repo_list.append(b)
    return render_template("home.html",repo_list = repo_list)
# @app.route('/all_commits',methods=['POST'])
# def get_all_commit():
#     repos = []
#     name_of_repo = request.form['repo_name']
#     start_date = request.form['startDate']
#     end_date = request.form['endDate']    
#     commitsLink = "https://api.github.com/repos/{0}/{1}/commits".format(ORG, name_of_repo)
#     req = urllib.request.Request(commitsLink, headers = HEADERS)
#     resp = urllib.request.urlopen(req)
#     f = urlopen(req)
#     string = f.read().decode('utf-8')
#     commits = json.loads(string)  
#     users = []  
#     # print(commits)
#     commit_list = []
#     for commit in commits:
#         li = []
#         date = commit['commit']['committer']['date']
#         date = date.split('T')
#         da = date[0]
#         name = commit['commit']['committer']['name']
#         msg = commit['commit']['message']
#         li.append(da)
#         li.append(name)
#         li.append(msg)
#         if da>=start_date and da <= end_date:
#             if li[1] != "GitHub":
#                 commit_list.append(li)
#                 users.append(name)
    # user_count = []
    # check_users = []
    # for i in users:
    #     if(check_users.count(i) == 0):
    #         check_users.append(i)
    #         ui = []
    #         ui.append(i)
    #         ui.append(users.count(i))
    #         user_count.append(ui)

#     return render_template("index.html", commit_list = commit_list,user_count = user_count, repo_list = repo_list,start_date = start_date,end_date = end_date )
@app.route("/lastcommitted")
def toGetLastCommit():
    items_per_page = 10
    lastCommit = []
    for repo in repo_list:
        i = 1
        toGetLastCommitUrl = "https://api.github.com/repos/{0}/{1}/commits".format(ORG, repo)
        req = urllib.request.Request(toGetLastCommitUrl, headers = HEADERS)
        resp = urllib.request.urlopen(req)
        f = urlopen(req)
        string = f.read().decode('utf-8')
        commits = json.loads(string)
        for commit in commits:
            if i == 1:
                name = commit['commit']['committer']['name']
                date = commit['commit']['committer']['date']
                message = commit['commit']['message']
                li = []
                li.append(repo)
                li.append(name)
                li.append(date)
                li.append(message)
                lastCommit.append(li)
                i = i + 1

    page = request.args.get('page', default=1, type=int)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_items = lastCommit[start_idx:end_idx]
    total_pages = (len(lastCommit)+ items_per_page - 1) // items_per_page
    return render_template('lastCommit.html', current_items=current_items, total_pages=total_pages, current_page=page)



@app.route('/name_of_branches',methods = ['POST'])
def all_branches_in_repo():
    name_of_repo = request.form['repo_name']
    url = "https://api.github.com/repos/{0}/{1}/branches".format(ORG, name_of_repo)
    req = urllib.request.Request(url, headers = HEADERS)
    resp = urllib.request.urlopen(req)
    f = urlopen(req)
    string = f.read().decode('utf-8')
    commits = json.loads(string)  
    branches = []
    for commit in commits:
        branch_name = commit['name']
        branches.append(branch_name)
        
    return render_template('home.html', repo_list = repo_list, branches = branches)

    
@app.route('/all_commits',methods=['POST'])
def get_with_branch_name():
    name_of_repo = request.form['repo_name']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    name_of_branch = request.form['branch_name']
    url = "https://api.github.com/repos/{0}/{1}/branches".format(ORG, name_of_repo)
    req = urllib.request.Request(url, headers = HEADERS)
    resp = urllib.request.urlopen(req)
    f = urlopen(req)
    string = f.read().decode('utf-8')
    commits = json.loads(string)  
    branches = []
    for commit in commits:
        if commit['name'] == name_of_branch:
            sha = commit['commit']['sha']
            branches.append(name_of_branch)
            branches.append(sha)
          
    results = []
    urlForBranchName ="https://api.github.com/repos/{0}/{1}/commits?per_page={2}&sha={3}".format(ORG,name_of_repo,1000, branches[1])
    req1 = urllib.request.Request(urlForBranchName, headers = HEADERS)
    resp1 = urllib.request.urlopen(req1)
    f1 = urlopen(req1)
    string1 = f1.read().decode('utf-8')
    all_deta = json.loads(string1)
    users = []
    for x in all_deta:
        li = []
        date = x['commit']['committer']['date']
        date = date.split('T')
        da = date[0]
        name = x['commit']['committer']['name']
        msg = x['commit']['message']
        li.append(da)
        li.append(name)
        li.append(msg)
        li.append(branches[0])

        if da>=start_date and da <= end_date:
            if li[1] != "GitHub":
                results.append(li)
                users.append(name)

    user_count = []
    check_users = []
    for l  in users:
        if(check_users.count(l) == 0):
            check_users.append(l)
            ui = []
            ui.append(l)
            ui.append(users.count(l))
            user_count.append(ui)

    return render_template("home.html", results = results, repo_list = repo_list,start_date = start_date,end_date = end_date)


# @app.route('/jira_projetcs')
# def  getAllProjects():



if __name__=='__main__':
    app.run(debug = True)
