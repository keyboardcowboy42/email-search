#!/usr/bin/env python3
# encoding: UTF-8


import requests
import re
import random


def convert_tags(text):
    for e in '''<KW> </KW> </a> <br> </br> <b> </b> </div> <em> </em> <p> </span>
                <strong> </strong> <title> <wbr> </wbr> \n'''.split():
        text = text.replace(e, '')
    for e in '%2f %3a %3A %3C %3D & / : ; < = > \\'.split():
        text = text.replace(e, ' ')
    return text 

def emails(text,domain):
    text = convert_tags(text)
    reg_emails = re.compile(
        '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +
        '@' +
        '[a-zA-Z0-9.-]*' +
        domain)
    return reg_emails.findall(text)

f = open('user_agents','r')
user_agents_list = [k.rstrip('\n') for k in f]

def get_emails(domain):
    no = 5
    url = 'https://www.google.com/search?num=100&start={counter}&hl=en&q="%40{domain}"'
    userAgent = random.choice(user_agents_list)
    print (userAgent)
    all_emails = []
    for i in range(no-1):
        final = url.format(counter = str(i*10),domain = domain)
        r=requests.get(final, headers={'User-Agent': userAgent})
        all_emails.extend(emails(r.text,domain))
    
    

    all_emails = [x.lower() for x in all_emails if not '22' in x]
    if len(all_emails) == 0:
        all_emails.append("Sorry no emails found")
    all_emails = set(all_emails)
    
    return all_emails