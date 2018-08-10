import re
from math import sqrt
from anytree import Node, RenderTree, DoubleStyle
from anytree.exporter import DotExporter


def notGreater(i, j):
    """Determine which operator will have higher priority."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'sqrt': 4}
    try:
        a = precedence[i]
        b = precedence[j]
        return True if a <= b else False
    except KeyError:
        return False


def preprocessExpression(string):
    """Convert a expression string to a list of operand and operator"""
    string = string.replace(' ', '')
    string = string.replace(')-', ') - ')
    string = string.replace('*-', ' * -')
    string = string.replace('/-', ' / -')
    string = string.replace('+-', ' + -')
    string = string.replace('--', ' + ')
    i = 1
    if len(string) != 1:
        while True:
            while string[i] == '-' and string[i - 1].isdigit() and string[i + 1].isdigit():
                string = string[:i] + ' ' + string[i] + ' ' + string[i + 1:]
            i += 1
            if i == len(string):
                break
    exp = re.findall(r'(-*[0-9,\.]+)|([*+^\/-]+|[A-Za-z]+)|(\(|\))', string)
    exp = [tuple(j for j in i if j)[-1] for i in exp]
    for i, x in enumerate(exp):
        try:
            exp[i] = float(x)
        except ValueError:
            pass
    return exp


def infixToPostfix(exp):
    """Convert infix expression to postfix expression"""
    output = []
    stack = []
    for i in exp:
        if type(i) is float:
            output.append(i)
        elif i == '(':
            stack.append('(')
        elif i == ')':
            while stack and stack[-1] != '(':
                a = stack.pop()
                output.append(a)
            if stack and stack[-1] != '(':
                return -1
            else:
                stack.pop()
        else:
            while stack and notGreater(i, stack[-1]):
                output.append(stack.pop())
            stack.append(i)
    while stack:
        output.append(stack.pop())

    return output


def evaluatePostfix(postfix):
    """Evaluate a postfix expression"""
    stack = []
    for i in postfix:
        if type(i) is float:
            stack.append(i)
        else:
            if i == 'sqrt':
                val = stack.pop()
                stack.append(sqrt(val))
            elif i == '-' and len(stack) == 1:
                val = stack.pop()
                stack.append(-val)
            else:
                val1 = stack.pop()
                val2 = stack.pop()
                if i == '+':
                    stack.append(val2 + val1)
                elif i == '-':
                    stack.append(val2 - val1)
                elif i == '*':
                    stack.append(val2 * val1)
                elif i == '/':
                    stack.append(val2 / val1)
                elif i == '^':
                    stack.append(val2**val1)

    return stack.pop()


def nodeattrfunc(node):
    """Export to DOT by value of node"""
    return 'label="' + str(node.val) + '"'


def edgetypefunc(node, child):
    """Return undirected egde for undirected tree export"""
    return '--'


def drawExpressionTree(postfix):
    """Draw expression tree in console and output to file"""
    stack = []
    index = 0
    for i in postfix:
        if type(i) is float:
            stack.append(Node(index, parent=None, val=i))
            index += 1
        else:
            if i == 'sqrt':
                child = stack.pop()
                parent = Node(index, parent=None, val=i)
                index += 1
                child.parent = parent
                stack.append(parent)
            elif i == '-' and len(stack) == 1:
                child = stack.pop()
                parent = Node(index, parent=None, val=i)
                index += 1
                child.parent = parent
                stack.append(parent)
            else:
                right = stack.pop()
                left = stack.pop()
                parent = Node(index, parent=None, val=i)
                index += 1
                left.parent = parent
                right.parent = parent
                stack.append(parent)
    root = stack.pop()
    DotExporter(root, graph="graph", nodeattrfunc=nodeattrfunc,
                edgetypefunc=edgetypefunc).to_dotfile("tree.dot")
    # Graphviz: http://www.webgraphviz.com/
    print(RenderTree(root, style=DoubleStyle).by_attr(attrname='val'))


try:
    expression = input("Input your expression: ")
    postfix = infixToPostfix(preprocessExpression(expression))
    print("Postfix expression: ", end='')
    for each in postfix:
        print(str(each), ' ', end='')
    drawExpressionTree(postfix)
    print('\nValue:', evaluatePostfix(postfix))
except ValueError:
    print("Math Error!")
except IndexError:
    print("Expression Not Valid")
