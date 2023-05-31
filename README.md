# Automatic Quesion Answering of City Council Questions

The city council can ask the municipal executive questions to clarify certain subjects. Answering those questions is a time-consuming and complex process. This project aims to aid the task by experimenting with different NLP modeling approaches and comparing the results regarding accuracy and execution times.

Therefore, the project aims to answer the following research question: 
To what extent can state-of-the art NLP models for (i) information retrieval and (ii) text generation aid the process of answering Amsterdam city council questions?

The planned implementation consists of two main steps: 
(1) retrieving:  rank the answer-relevant documents from the websites 
(2) generating: create an answer based on the most relevant documents

![](media/examples/question_types.png)

---


## Project Folder Structure

This project has the following folder structure:

1) [`notebooks`](./notebooks): Folder containing the different stages of the pipeline:
- [`EDA`](./notebooks/EDA): Notebooks containing graphs and descriptive statistics of the data
- [`Ranking`](./notebooks/Ranking): Folder containing a notebook per each retrieval method
    -> BM25.ipynb: Ranks documents from the collection through the ElasticSearch API
    -> TF-IDF.ipynb:  Ranks documents from the collection based on TF-IDF and Cosine Similarity
    -> Random_retrieval: Randomly ranks documents from the collection - *to be fixed*
    -> ... Neural search methods - *to be included*
- [`Reading`](./notebooks/Reading): Folder containing a notebook per each text generation method
        - mT5.ipynb: Summarizes the top retrieved documents from the best retrieval method
        - ... 
    iv) [`URL_Collection`](./notebooks/URL_Collection): Folder containing a notebook per each web scraping source
        - Collect_amsterdam.ipynb: Collects all pages and subpages under the category 'Onderwepen' in amsterdam.nl
        - Collect_rijksoverheijd: Collects pdfs from rijksoverheid.nl/documenten *to be included*
        - Collect_references.ipynb: Collects all URLs that have been referenced to in the answers from the QA dataset
4) [`src`](./src): Folder for all source files specific to this project
5) [`data`](./data) Includes sample data - *to be included*
6) [`tests`](./tests) Test example - *to be included*
7) [`media`](./media): Folder containing media files (icons, video)





---


## Installation

Explain how to set up everything. 
Let people know if there are weird dependencies - if so feel free to add links to guides and tutorials.

A person should be able to clone this repo, follow your instructions blindly, and still end up with something *fully working*!

1) Clone this repository:
    ```bash
    git clone https://github.com/Amsterdam-Internships/InternshipAmsterdamGeneral
    ```

1) If you are using submodules don't forget to include `--recurse-submodules` to the step above or mention that people can still do it afterwards:
   ```bash
   git submodule update --init --recursive
   ```

1) Install all dependencies:
    ```bash
    pip install -r requirements.txt
    ```
---


## Usage

Explain example usage, possible arguments, etc. E.g.:

To train... 


```
$ python train.py --some-importang-argument
```

If there are too many command line arguments, you can add a nice table with explanation (thanks, [Diana Epureano](https://www.linkedin.com/in/diana-epureanu-235104153/)!)

|Argument | Type or Action | Description | Default |
|---|:---:|:---:|:---:|
|`--batch_size`| int| `Batch size.`|  32|
|`--device`| str| `Training device, cpu or cuda:0.`| `cpu`|
|`--early-stopping`|  `store_true`| `Early stopping for training of sparse transformer.`| True|
|`--epochs`| int| `Number of epochs.`| 21|
|`--input_size`|  int| `Input size for model, i.e. the concatenation length of te, se and target.`| 99|
|`--loss`|  str|  `Type of loss to be used during training. Options: RMSE, MAE.`|`RMSE`|
|`--lr`|  float| `Learning rate.`| 1e-3|
|`--train_ratio`|  float| `Percentage of the training set.`| 0.7|
|...|...|...|...|


Alternatively, as a way of documenting the intended usage, you could add a `scripts` folder with a number of scripts for setting up the environment, performing training in different modes or different tasks, evaluation, etc (thanks, [Tom Lotze](https://www.linkedin.com/in/tom-lotze/)!)

---


## How it works



---
## Acknowledgements

*to be included*

