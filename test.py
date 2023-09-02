# import requests, json
# from flask import Flask, redirect, request, render_template, url_for
# import pandas as pd
# from git import Repo, Commit
# import urllib.request
# from datetime import datetime,date, timedelta
# from urllib.request import urlopen
# import dateutil.relativedelta

# app = Flask(__name__)

# BASE_URL = 'https://api.github.com'
# ORG = 'liquiloans'

# # HEADERS = {
# #     'Accept': 'application/vnd.github+json',
# #     'Authorization': 'Bearer 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',
# #     'X-GitHub-Api-Version': '2022-11-28'
# # }

# def get_all_repo():
#     response = requests.get(f'{BASE_URL}/orgs/{ORG}/repos')
#     repos_df = pd.json_normalize(response.json())
#     print(repos_df[''])
#     # fin = []
#     # fin = repos_df['name']

#     # final_list = []
#     # for b in fin:
#     #     final_list.append(b)
#     # print(final_list)

# get_all_repo()

# # if __name__=='__main__':
# #     response = requests.get(f'{BASE_URL}/orgs/{ORG}/repos', headers=HEADERS)
# #     repos_df = pd.json_normalize(response.json())
# #     fin = []
# #     print(repos_df.columns)
# #     app.run(debug = True)
