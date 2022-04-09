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

I want to retrieve movie scripts that are about crimes for money.

## How to use

To process movie scripts with boolean model.
```sh
python sources/boolean_model.py movies
```

To process movie scripts with vector space model.
```sh
python sources/vector_space_model.py movies
```

## Resources

https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt

