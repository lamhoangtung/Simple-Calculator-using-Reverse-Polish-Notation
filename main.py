import re
from math import sqrt
from anytree import Node, RenderTree, DoubleStyle
from anytree.exporter import DotExporter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def preprocessExpression(string):
    """Convert a expression string to a list of operand and operator"""
    # Remove space
    string = string.replace(" ","")
    # Add missing '*' operator
    string = re.sub(r'(\)|x)(\(|[0-9]|s|x)', r'\1*\2', string)
    string = re.sub(r'([0-9])(\(|x|s)', r'\1*\2', string)
    string = re.sub(r'(x)(x)', r'\1*\2', string)
    # Handle multiple '+' and '-' operator
    string = re.sub(r'(\-{2})+', '+', string)
    string = re.sub(r'\++', '+', string)
    string = re.sub(r'(\+\-)+', '-', string)
    string = re.sub(r'(\-\+)+','-', string)
    # Separate minus operator and minus number
    string = re.sub(r'(\)|[0-9]|x)(\-)', r'\1\2 ',string)
    string = re.sub(r'([\*\/])(\-)', r'\1 \2',string)
    # Convert to a list with operand and operator by order
    exp = re.findall(r'(-*[0-9,\.]+)|([*+^\/-]+|[A-Za-z]+)|(\(|\))', string)
    exp = [tuple(j for j in i if j)[-1] for i in exp]
    for i, x in enumerate(exp):
        try:
            exp[i] = float(x)
        except ValueError:
            pass
    haveVarible = True if 'x' in exp else False
    return exp, haveVarible


def notGreater(i, j):
    """Determine which operator will have higher priority."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'sqrt': 4}
    try:
        a = precedence[i]
        b = precedence[j]
        return True if a <= b else False
    except KeyError:
        return False


def infixToPostfix(exp):
    """Convert infix expression to postfix expression"""
    output = []
    stack = []
    for i in exp:
        if type(i) is float or i == 'x':
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


def evaluatePostfix(postfix, x):
    """Evaluate a postfix expression"""
    stack = []
    for i in postfix:
        if type(i) is float:
            stack.append(i)
        elif i == 'x':
            stack.append(x)
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
        if type(i) is float or i == 'x':
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
    print("\nExpression Tree:")
    print(RenderTree(root, style=DoubleStyle).by_attr(attrname='val'))


def plotFunction(postfix):
    """Plot a function by connect a collection of points specify by user input"""
    x1 = float(input("\nInput x start: "))
    x2 = float(input("Input x end: "))
    m = int(input("Input number of points: "))
    step = (x2-x1)/m
    x = []
    y = []
    for i in np.arange(x1, x2, step):
        x.append(i)
        y.append(evaluatePostfix(postfix, i))
    df = pd.DataFrame({'x_axis': x, 'y_axis': y})
    print(df)
    fig = plt.figure(num='Ham so')
    ax = fig.add_subplot(111)
    plt.plot('x_axis', 'y_axis', color='green', data=df, linestyle='-', marker='o')
    plt.plot(x, y, 'go-')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.scatter(0, 0)
    plt.grid(True)
    plt.savefig("function.png")
    print("Function ploted, see the result at 'function.png' file.")
    # plt.show()


def main():
    try:
        expression = input("Input your expression: ")
        expression, haveVarible = preprocessExpression(expression)
        postfix = infixToPostfix(expression)
        print(postfix)
        print("Postfix expression: ", end='')
        for each in postfix:
            print(str(each), ' ', end='')
        drawExpressionTree(postfix)
        if haveVarible:
            x = float(input("Input value of x: "))
            print('\nValue of expression:', evaluatePostfix(postfix, x))
            plotFunction(postfix)
        else:
            print('\nValue of expression:', evaluatePostfix(postfix, 0))
    except ValueError:
        print("Math Error!")
    except IndexError:
        print("Expression Not Valid")


if __name__ == '__main__':
    main()
