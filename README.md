# logicalsoup

An experiment in scraping HTML with Prolog. This script takes an HTML file,
parses it with beautifulsoup and prints the corresponding Prolog facts.
See the below examples and [facts.jinja](facts.jinja) for an idea of use.

## Examples

### Extract all 'Ask HN' post titles

```
$ poetry run python -m logicalsoup.main tests/data/ask-hn.html > out/askhn.pl
$ swipl out/askhn.pl
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

### Extract 'Ask HN' posts from u/whoishiring

```
$ poetry run python -m logicalsoup.main tests/data/ask-hn.html > out/askhn.pl
$ swipl out/askhn.pl
```

Example output:

```prolog
?- attr(FirstId,class,"athing"),attr(FirstId,tr),sibling(SiblingId,FirstId),descendant(ChildId,SiblingId),attr(ChildId,a,class,"hnuser"),attr(ChildId,text("whoishiring")),descendant(TitleId,FirstId),attr(TitleId,class,"title"),attr(TitleId,text(Title)),descendant(LinkId,TitleId),attr(LinkId,a,href,PostLink).
FirstId = "c977221c-6c91-11ef-a357-6a3e8c423ff5",
SiblingId = "c977262c-6c91-11ef-a357-6a3e8c423ff5",
ChildId = "c97727c6-6c91-11ef-a357-6a3e8c423ff5",
TitleId = "c977253c-6c91-11ef-a357-6a3e8c423ff5",
Title = "Ask HN: Who is hiring?\n                                        (September 2024)",
LinkId = "c97725d2-6c91-11ef-a357-6a3e8c423ff5",
PostLink = "item?id=41425910" ;
FirstId = "c977221c-6c91-11ef-a357-6a3e8c423ff5",
SiblingId = "c977262c-6c91-11ef-a357-6a3e8c423ff5",
ChildId = "c97727c6-6c91-11ef-a357-6a3e8c423ff5",
TitleId = "c977253c-6c91-11ef-a357-6a3e8c423ff5",
Title = "Ask HN: Who is hiring?\n                                        (September 2024)",
LinkId = "c97725d2-6c91-11ef-a357-6a3e8c423ff5",
PostLink = "item?id=41425910" ;
FirstId = "c9772b4a-6c91-11ef-a357-6a3e8c423ff5",
SiblingId = "c9772f5a-6c91-11ef-a357-6a3e8c423ff5",
ChildId = "c97730f4-6c91-11ef-a357-6a3e8c423ff5",
TitleId = "c9772e60-6c91-11ef-a357-6a3e8c423ff5",
Title = "Ask HN: Who wants to be\n                                        hired? (September 2024)",
LinkId = "c9772eec-6c91-11ef-a357-6a3e8c423ff5",
PostLink = "item?id=41425908" ;
FirstId = "c9772b4a-6c91-11ef-a357-6a3e8c423ff5",
SiblingId = "c9772f5a-6c91-11ef-a357-6a3e8c423ff5",
ChildId = "c97730f4-6c91-11ef-a357-6a3e8c423ff5",
TitleId = "c9772e60-6c91-11ef-a357-6a3e8c423ff5",
Title = "Ask HN: Who wants to be\n                                        hired? (September 2024)",
LinkId = "c9772eec-6c91-11ef-a357-6a3e8c423ff5",
PostLink = "item?id=41425908" ;
false.
```