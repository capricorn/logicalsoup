import argparse

from bs4 import BeautifulSoup, Tag
from jinja2 import Template

from logicalsoup.tags import tags

def generate_prolog_ast(root_node):
    return generate_prolog_ast_rec(root_node)# + '.'

def generate_prolog_ast_rec(root_node):
    children_asts = [ f'element(\'{child.name}\', [{generate_prolog_ast_rec(child)}])' for child in root_node.children if type(child) is Tag ]
    children_asts_str = f'[{', '.join(children_asts)}]'
    return f'element(\'{root_node.name}\', {children_asts_str})'

def build_logicalsoup_predicates(prolog_ast, tags):
    with open('ast.jinja') as f:
        template = Template(f.read())
    
    return template.render(prolog_ast=prolog_ast, tags=tags)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('html_file', help='An HTML file to convert to a Prolog AST.')
    args = parser.parse_args()

    with open(args.html_file, 'r') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    prolog_ast = generate_prolog_ast(soup)
    print(build_logicalsoup_predicates(prolog_ast=prolog_ast, tags=tags))