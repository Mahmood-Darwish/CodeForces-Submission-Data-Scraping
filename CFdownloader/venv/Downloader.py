import requests
import json
import os
import time
from bs4 import BeautifulSoup as bs
from pathlib import Path

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789()')
user = input("Enter CF handle: ")
url = "https://codeforces.com/api/user.status?handle=" + user;
filepath = input("Enter path for file: ")
problems = requests.get(url)
problems = problems.json();
Path(filepath).mkdir(parents=True, exist_ok=True)
f = open(filepath + '\\temporary_file_to_be_del', "w")
f.close()
for submission in problems['result']:
    if submission['verdict'] != 'OK':
        continue
    page = requests.get("http://codeforces.com/contest/%s/submission/%d" %(submission['contestId'], submission['id']))
    if(page.status_code != 200):
        print("Failed! %s" %submission['problem']['name'])
        continue
    if(len(submission['problem']['name']) == 0):
        continue
    submission['problem']['name'] = ''.join(filter(whitelist.__contains__, submission['problem']['name']))
    if(len(submission['problem']['name']) == 0):
        continue
    while(len(submission['problem']['name']) > 0 and submission['problem']['name'][-1] == ' '):
        submission['problem']['name'] = submission['problem']['name'][:-1]
    Path(filepath + "\\%s" %submission['problem']['name']).mkdir(parents=True, exist_ok=True)
    if (submission['programmingLanguage'] == "Java 8"):
        f = open(filepath + "\\%s" %submission['problem']['name'] + "\\%s.txt" %submission['problem']['name'], "w")
    else:
        f = open(filepath + "\\%s" %submission['problem']['name'] + "\\%s.cpp" %submission['problem']['name'], "w")
    soup = bs(page.text, 'html.parser')
    ret = soup.find(id='program-source-text')
    result = ''
    if ret is None:
        result = ''
    else:
        result = ret.text.rstrip()
    f.write(result)
    f.close()
    f = open(filepath + "\\%s" %submission['problem']['name'] + "\\Link.txt", "w")
    f.write("http://codeforces.com/contest/%s/submission/%d" %(submission['contestId'], submission['id']))
    f.close()
    print("%s! Done!\n" %submission['problem']['name'])

print("Finished!")
