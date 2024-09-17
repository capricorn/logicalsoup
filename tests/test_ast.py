from bs4 import BeautifulSoup
from logicalsoup import ast

def test_attrs_generation():
    with open('tests/data/ask-hn.html') as f:
        html = f.read()
        parser = BeautifulSoup(html, 'html.parser')
    element = parser.find(attrs={'id': 'pagespace'})
    prolog_attrs = ast.generate_attributes(element)

    assert prolog_attrs == '[attr("id", "pagespace"), attr("title", "Ask"), attr("style", "height:10px")]'