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

# name_of_repo = ''

@app.route('/',methods=['GET'])        
def get_all_repo():
    response = requests.get(f'{BASE_URL}/orgs/{ORG}/repos', headers=HEADERS)
    repos_df = pd.json_normalize(response.json())
    fin = []
    fin = repos_df['name']
    final_list = []
    for b in fin:
        final_list.append(b)
    return render_template("index.html",final_list = final_list)

# @app.route('/last_n_month', methods=['POST'])
# def last_n_month_commit():
#     n = 1
#     name_of_repo = 'liquiloans_iac'
#     # name_of_repo = request.form['repo_name']
#     start_date = date.today()
#     last_n_month_date = start_date - timedelta(days=start_date.day)
#     last_n_month_date = last_n_month_date.replace(month=start_date.month - n)
#     commitsLink = "https://api.github.com/repos/{0}/{1}/commits".format(ORG, name_of_repo)
#     req = urllib.request.Request(commitsLink, headers = HEADERS)
#     resp = urllib.request.urlopen(req)
#     f = urlopen(req)
#     string = f.read().decode('utf-8')
#     commits = json.loads(string)    
#     # print(commits)
#     final_list = []
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
#         if da>=start_date and da <= last_n_month_date:
#             final_list.append(li)
#     return render_template("last_n_month.html", final_list = final_list)


@app.route('/all_commits',methods=['POST'])
def get_all_commit():
    name_of_repo = request.form['repo_name']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    if start_date == None:
        name_of = 'liquiloans_iac'
        return redirect(url_for('last_n_month_commit',name_of_repo =name_of))
    if start_date == None:
        start_date = date.today()
        last_n_month_date = start_date - timedelta(days=start_date.day)
        end_date = last_n_month_date.replace(month=start_date.month - 1)
    
    commitsLink = "https://api.github.com/repos/{0}/{1}/commits".format(ORG, name_of_repo)
    req = urllib.request.Request(commitsLink, headers = HEADERS)
    resp = urllib.request.urlopen(req)
    f = urlopen(req)
    string = f.read().decode('utf-8')
    commits = json.loads(string)    
    # print(commits)
    final_list = []
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
            final_list.append(li)
# return final_list
    return render_template("all_commits.html", final_list = final_list)



if __name__=='__main__':
    app.run(debug = True)
