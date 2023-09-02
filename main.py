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
    'Authorization': 'Bearer',
    'X-GitHub-Api-Version': '2022-11-28'
}

# name_of_repo = ''

repo_list = []
@app.route('/',methods=['GET'])        
def get_all_repo():
    response = requests.get(f'{BASE_URL}/orgs/{ORG}/repos', headers=HEADERS)
    repos_df = pd.json_normalize(response.json())
    fin = []
    # print(repos_df.columns)
    fin = repos_df['name']

    result = dict()
    for b in fin:
        repo_list.append(b)
    return render_template("index.html",repo_list = repo_list)

@app.route('/all_commits',methods=['POST'])
def get_all_commit():
    name_of_repo = request.form['repo_name']
    start_date = request.form['startDate']
    end_date = request.form['endDate']    
    commitsLink = "https://api.github.com/repos/{0}/{1}/commits".format(ORG, name_of_repo)
    req = urllib.request.Request(commitsLink, headers = HEADERS)
    resp = urllib.request.urlopen(req)
    f = urlopen(req)
    string = f.read().decode('utf-8')
    commits = json.loads(string)    
    # print(commits)
    commit_list = []
    for commit in commits:
        li = []
        date = commit['commit']['committer']['date']
        date = date.split('T')
        da = date[0]
        name = commit['commit']['committer']['name']
        msg = commit['commit']['message']
        li.append(da)
        li.append(name)
        li.append(msg)
    # ymd to m d y
    # date_i = datetime.strptime(da, '%Y-%m-%d')
    # date_of_commit = date_i.strftime("%m-%d-%Y")
        if da>=start_date and da <= end_date:
            commit_list.append(li)
# return final_list
    return render_template("index.html", commit_list = commit_list, repo_list= repo_list)



if __name__=='__main__':
    app.run(debug = True)
