from uuid import uuid1
import argparse

from bs4 import BeautifulSoup
import bs4

def walk_tree(node, f, node_id):
    if type(node) is bs4.element.NavigableString:
        return

    # TODO: Support
    if type(node) is bs4.Comment:
        return

    # TODO: Support? (Parsing JS in Prolog is a different matter...)
    if type(node) is bs4.Script:
        return

    f(node, node_id)
    for child in node.children:
        child_id = uuid1()
        print(f'child("{child_id}", "{node_id}").')
        walk_tree(child, f, child_id)

def attr_relations(node, node_id) -> uuid1:
    attrs = []
    for key, val in node.attrs.items():
        if type(val) is list:
            for i in val:
                attrs.append(f'attr("{node_id}", {node.name}, {key}, "{i}").')
                attrs.append(f'attr("{node_id}", {key}, "{val}").')
                if node.text:
                    attrs.append(f'attr("{node_id}", {node.name}, {key}, "{i}", text("{node.text}")).')
                    attrs.append(f'attr("{node_id}", text("{node.text}")).')
        else:
            attrs.append(f'attr("{node_id}", {node.name}, {key}, "{val}").')
            attrs.append(f'attr("{node_id}", {key}, "{val}").')
            if node.text:
                attrs.append(f'attr("{node_id}", {node.name}, {key}, "{val}", text("{node.text}")).')
                attrs.append(f'attr("{node_id}", text("{node.text}")).')
        
    
    return attrs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('html_file', help='An HTML filepath to transform into Prolog facts.')
    args = parser.parse_args()

    with open(args.html_file) as f:
        html = f.read()
    
    parser = BeautifulSoup(html, 'html.parser')
    node = parser.html

    # TODO: Move to template?
    print(':- use_module(library(solution_sequences)).')
    print('titles(Title) :- attr(RecordListId,ul,class,"record-list"), attr(MediaBodyId,div,class,"media-body"), descendant(MediaBodyId,RecordListId), attr(TitleId,a,class,"title"), descendant(TitleId,MediaBodyId), attr(TitleId,text(Title)).')

    s = []
    walk_tree(node, lambda n, id: s.extend(attr_relations(n, id)), uuid1())

    '''
    Procedure for finding an id that's a descendant of a given node.
    '''
    descendant_rule = \
        '''
        descendant(DescendantId, AncestorId) :-
            child(DescendantId, AncestorId) ;
            (child(BetweenId, AncestorId), descendant(DescendantId, BetweenId)).
        '''
    print(descendant_rule)

    for fact in s:
        print(fact)