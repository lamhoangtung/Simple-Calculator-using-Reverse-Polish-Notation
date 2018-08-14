# Simple-Calculator-using-Reverse-Polish-Notation
Simple Calculator using Reverse Polish Notation in Python

## How to run

When **[main.py](main.py)** is running, you will be able to input your expression, the program will evaluate your expression and also plot an Expression Tree to the console and to a **.dot** file:

![alt text](https://sv1.uphinhnhanh.com/images/2018/08/10/ScreenShot2018-08-10at10.11.52.png)

It's also can handle **one variable function**, when evaluate the expression, the program will ask you to **input the value of the variable**:

![alt text](https://i.imgur.com/YwTppXu.png)

You can use **dot** tool from the [graphviz](http://www.graphviz.org/) package to render the expression tree into a ***.png*** image:
```
dot tree.dot -T png -o tree.png
```
<p align="center">
  <img src="https://s2.upanh.pro/2018/08/09/tree.png">
</p>

You can also copy all content inside the [**tree.dot**](tree.dot) file and use [Webgprahviz](http://www.webgraphviz.com/) to plot the tree right inside your browser:

<p align="center">
  <img src="https://media.giphy.com/media/2fsdaNR299EuyYtVJ7/giphy.gif">
</p>

If the expression is an one variable function, this program can plot it to a [**.png file**](function.png). The program will ask you the range of the graph and how many point (how acurrate) you want the graph to be. **Keep in mind, you shoudn't plot with too little points since it may lead to wrong graph:**

<p align="center">
  <img src="https://i.imgur.com/ByTU4tv.png">
</p>

#### Dependencies
The code was developed with the following configuration:
* python 3.6.4
* anytree 2.4.3
* graphviz 0.8.4
* numpy 1.14.2
* pandas 0.22.0
* matplotlib 2.2.2

Other configuration will reasonably work

## Documentation
You can see the details documentation about how I make this calculator in the [notebook file](Simple Calculator using Reverse Polish Notation.ipynb).

## Contributing

Please feels free to contribute to this project, there are a lot of room for improvement, my suggesion are:
* Evaluate expression using expression tree and DFS
* Making UI (currently running on console)
* Add support for more variable (currently support only one variable)
* Add more operator (currently support + - * / ^ and sqrt)

## Authors

* **Hoang Tung Lam** - *Initial work* - [lamhoangtung](https://github.com/lamhoangtung)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
