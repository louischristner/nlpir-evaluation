# Evaluation

## Introduction

### Previous work

Proximity between crime movies and thriller movies.
Can we use word distribution statistics on movie scripts to understand their proximity and differences?

### Instructions

In the previous HW, we have collected movie scripts, and understood there are some difference on term frequency.

In this HW, we need to use the same dataset and implement two models for IR.
- Boolean model
- Vector space model

More importantly, we need to evaluate the models for understanding how good the models are working.
- Precision & Recall
- MAP (CG model)

### Goal of the project

The goal of the project is to implement the boolean and vector space models, and evaluate them using Precision & Recall and Mean Average Precision.

The dataset used for the project is composed of 100 scripts of thriller and crime movies.

For the evaluation of the models, I tried to come up with a query related to the common topics of movies among these genres. Thus, the objective for this project is to retrieve the most pertinent movies about crimes committed for money.

## How to use

To process movie scripts with boolean model.
```sh
python sources/boolean_model.py movies
```

To process movie scripts with ranked boolean model.
```sh
python sources/ranked_boolean_model.py movies
```

To process movie scripts with vector space model.
```sh
python sources/vector_space_model.py movies
```

## Resources

https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt

