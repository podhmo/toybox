from: https://github.com/sloria/webargs/tree/dev/examples


```bash
$ python app.py

$ pip install httpie
$ http GET :5001/
$ http GET :5001/ name==Ada
$ http POST :5001/add x=40 y=2
$ http POST :5001/dateadd value=1973-04-10 addend=63
$ http POST :5001/dateadd value=2014-10-23 addend=525600 unit=minutes
```
