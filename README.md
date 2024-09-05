## Examples

### Extract all 'Ask HN' post titles

```
$ poetry run python -m logicalsoup.main > askhn.pl
$ swipl askhn.pl
```

Example output:

```prolog
?- attr(TitleId,class,"titleline"),child(AnchorId,TitleId),attr(AnchorId,text(Title)).
TitleId = "859b3396-6bcc-11ef-9c29-6a3e8c423ff5",
AnchorId = "859b33dc-6bcc-11ef-9c29-6a3e8c423ff5",
Title = "Ask HN: Who is hiring? (September 2024)" ;
TitleId = "859b3c42-6bcc-11ef-9c29-6a3e8c423ff5",
AnchorId = "859b3c88-6bcc-11ef-9c29-6a3e8c423ff5",
Title = "Ask HN: Who wants to be hired? (September 2024)" ;
TitleId = "859b43ae-6bcc-11ef-9c29-6a3e8c423ff5",
AnchorId = "859b43ea-6bcc-11ef-9c29-6a3e8c423ff5",
Title = "Ask HN: Who wants to collaborate (thread) – 5 Sep 2024" .
```