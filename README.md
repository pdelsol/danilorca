# danilorca

## developing
### deps

```
pip install poetry
poetry install
```
## create static site

```
pelican content
pelican --listen
```

## updating content

### download new radio episodes

```
python download.py
aws s3 sync downloads/* s3://s.danilorca.com/
```



## deploy
```
git push
```