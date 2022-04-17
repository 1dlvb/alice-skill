# Alice skill python server. Short example.
#### Prepare cert files
```cert/fullchain.pem```   
```cert/privkey.pem```   
```cert/cert.json```
#### Check, does your server accepting https requests
https://~~yoursite.net~~:8081/check   
Should return: ok
#### Run the server
```python3 server.py```   
to run server forever:   
```nohup python3 /home/format37_gmail_com/projects/alice/server.py &```
#### Open skill setup page
https://dialogs.yandex.ru/developer/skills
#### Paste your server https link to Backend Webhook URL field
https://~~yoursite.net~~:8081/alice
#### Switch to testing page and test it!
![Alt-текст](https://github.com/format37/alice/blob/master/images/alice.png "Success!")