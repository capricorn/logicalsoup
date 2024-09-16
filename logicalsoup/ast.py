from bs4 import BeautifulSoup, Tag
import argparse

def generate_prolog_ast(root_node):
    return generate_prolog_ast_rec(root_node)# + '.'

def generate_prolog_ast_rec(root_node):
    children_asts = [ f'element("{child.name}", [{generate_prolog_ast_rec(child)}])' for child in root_node.children if type(child) is Tag ]
    children_asts_str = f'[{', '.join(children_asts)}]'
    return f'element("{root_node.name}", {children_asts_str})'

def build_logicalsoup_predicates():
    match_predicate = \
        '''
        match([Child|Siblings], Expr) :-
            match(Child, Expr)
            ; match(Siblings, Expr).
        match(Node, Expr) :-
            Node = Expr
            ; (Node = element(_, Children), match(Children, Expr)).
        match(Expr) :-
            match({prolog_ast}, Expr).

        % Test: wrap every (individual) node in 'hello(Node)'
        hello(Expr).
        hello([], SiblingExpr) :-
            SiblingExpr = [].
        hello([Child|Siblings], ResultExpr) :-
            hello(Siblings, SiblingExpr),
            append([hello(Child)], SiblingExpr, ResultExpr).

        % An example: visiting a tree and wrapping each element in 'hello' 
        helloVisit([], ResultExpr) :-
            ResultExpr = [].
        % This performs the traversal
        helloVisit([Child|Siblings], ResultExpr) :-
            helloVisit(Child, ChildExpr),
            helloVisit(Siblings, SiblingExpr),
            append([ChildExpr], [SiblingExpr], ResultExpr).
        % This performs the map
        helloVisit(Expr, ResultExpr) :- 
            Expr = element(Tag, Children),
            helloVisit(Children, ChildExpr),
            % ResultExpr = hello(element(Tag, ChildExpr)).
            ResultExpr = element(Tag, ChildExpr).

        % Next change: use match to see if an element should be substituted
        % Then, provide AST as arg
        % Either: have a match (and a rewrite) or visit the next element
        % Consider: Rewrite how match works?

        % Test this on a few cases
        % NB. Expr may be some deeply nested thing; 
        % helloMatch(Expr, MatchExpr) :-
        %    (Expr = MatchExpr)
        %    ; (Expr = element(Tag, Children), )

        helloVisit([], MatchExpr, RewriteExpr, ResultExpr) :-
            ResultExpr = [].

        % This performs the traversal
        helloVisit([Child|Siblings], MatchExpr, RewriteExpr, ResultExpr) :-
            helloVisit(Child, MatchExpr, RewriteExpr, ChildExpr),
            helloVisit(Siblings, MatchExpr, RewriteExpr, SiblingExpr),
            append([ChildExpr], [SiblingExpr], ResultExpr).

        % Consider: Treat MatchExpr and RewriteExpr as predicates, call them?

        helloVisit(Expr, MatchExpr, RewriteExpr, ResultExpr) :-
            % (match(Expr, MatchExpr), helloVisit(RewriteExpr, ResultExpr))
            % TODO: Is it a problem of this sort of match?
            % (Expr = MatchExpr, customRewrite(Expr, NewExpr), helloVisit(NewExpr, MatchExpr, RewriteExpr, ResultExpr))
            (customRewrite(Expr, NewExpr), helloVisit(NewExpr, MatchExpr, RewriteExpr, ResultExpr), !)
            ; (Expr = element(Tag, Children), helloVisit(Children, MatchExpr, RewriteExpr, ChildrenExpr), ResultExpr = element(Tag, ChildrenExpr)).
        
        
        visit(Rewriter, [], ResultExpr) :-
            ResultExpr = [].
        visit(Rewriter, [Child|Siblings], ResultExpr) :-
            visit(Rewriter, Child, ChildExpr),
            visit(Rewriter, Siblings, SiblingExpr),
            append([ChildExpr], [SiblingExpr], ResultExpr).
        visit(Rewriter, Expr, ResultExpr) :-
            (rewrite(Rewriter, Expr, NewExpr), visit(Rewriter, NewExpr, ResultExpr), !)
            ; (Expr = element(Tag, Children), visit(Rewriter, Children, ChildrenExpr), ResultExpr = element(Tag, ChildrenExpr)).
    
        % Provide a dynamic predicate such as:
        customRewrite(Expr, NewExpr) :-
            Expr = element(div, Children),
            NewExpr = element(p, Children).
        
        % Example of applying a rule via call -- make a 'helloVisit' declaration that is wrapped with this
        rewrite(Rule, Expr, NewExpr) :-
            call(Rule, Expr, NewExpr).

        '''
    
    return '\n'.join([match_predicate]) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('html_file', help='An HTML file to convert to a Prolog AST.')
    args = parser.parse_args()

    with open(args.html_file, 'r') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    prolog_ast = generate_prolog_ast(soup)
    print(build_logicalsoup_predicates().format(prolog_ast=prolog_ast))