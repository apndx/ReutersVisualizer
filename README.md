# [ReutersVisualizer](https://reuters-visualizer.herokuapp.com/)
This project is for the Helsinki University Interactive data visualization course.

The visualizations are based on the [Reuters Corpora](https://trec.nist.gov/data/reuters/reuters.html) document topics in the CD 2. The articles are from year 1997. I was inspired to explore the data more thoroughly with visualizations while I was using the corpus in developing [a document classifier](https://github.com/apndx/ReutersDocLabeler).

### Cleaning, exploring and sketching

I did data cleaning, exploration data analysis in [Jupyter noteboooks](https://github.com/apndx/ReutersVisualizer/tree/main/notebooks). In some of the notebooks I also tried out different visualization techniques and ideas. Some parts of the notebooks are quite verbose and not that edited. In them I try in a sketchy manner to find out what might work and what does not. The parts that I decided to keep, are used in the [Dash application](https://github.com/apndx/ReutersVisualizer/blob/main/app.py).

The online version of the application can be found in [Heroku](https://reuters-visualizer.herokuapp.com/).

### Application

To locally run the application, download the repository and install the [dependencies](https://github.com/apndx/ReutersVisualizer/blob/main/requirements.txt). After that you can start the application in the main folder:

```
python app.py
```

### Learning diaries

The project is described in a more detailed manner in the four learning diaries that cover the four week period of the project. 

* [Week 1](https://github.com/apndx/ReutersVisualizer/tree/main/documentation/learning-diary-1.pdf)
* [Week 2](https://github.com/apndx/ReutersVisualizer/tree/main/documentation/learning-diary-2.pdf)
* [Week 3](https://github.com/apndx/ReutersVisualizer/tree/main/documentation/learning-diary-3.pdf)
* [Week 4](https://github.com/apndx/ReutersVisualizer/tree/main/documentation/learning-diary-4.pdf)
