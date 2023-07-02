# Automatic Quesion Answering of City Council Questions

The city council can ask the municipal executive questions to clarify certain subjects. Answering those questions is a time-consuming and complex process. This project aims to aid the task by experimenting with different NLP modeling approaches and comparing the results regarding accuracy and execution times.

Therefore, the project aims to answer the following research question: 
To what extent can state-of-the art NLP models for (i) information retrieval and (ii) text generation aid the process of answering Amsterdam city council questions?

The planned implementation consists of two main steps: 
(1) retrieving:  rank the answer-relevant documents from the websites 
(2) generating: create an answer based on the most relevant documents

![](media/examples/question_types.png)

---

## Published Long Form Question Answering (LFQA) Dataset in Dutch 
You can find the published LFFQA dataset with questions, posed by the Amsterdam city council and answers by the Amsterdam municipal executive in the dates ranging from 2013 till 2022 at: [`questions`](./data/question_answer)

## Project Folder Structure

This project has the following folder structure:

1. [`notebooks`](./notebooks): Folder containing the different stages of the pipeline:
    1. [`0_exploratory_data_analysis`](./notebooks/0_exploratory_data_analysis): Notebooks containing graphs and descriptive statistics of the data
        - [`questions_answers_EDA`](./notebooks/EDA/questions_answers_EDA): Explores the data in terms of the questions and the answers, their length, common words, common topics
        - [`URLs_EDA`](./notebooks/EDA/URLs_EDA): Explores the most commonly referneced URLs in the municipal answers
    3. [`1_supporting_documents_collection`](./notebooks/1_supporting_documents_collection): Folder of notebooks containing supporting documents. You can collect the supporting documents from amsterdam.nl either all at once through [`1_1_collect_ams_at_once`](./notebooks/1_supporting_documents_collection/1_1_collect_ams_at_once.ipynb) or individually through [`1_2_1_collect_ams_subpages_individually.ipynb`](./notebooks/1_supporting_documents_collection/11_2_1_collect_ams_subpages_individually.ipynb)
        - [`1_1_collect_ams_at_once`](./notebooks/1_supporting_documents_collection/1_1_collect_ams_at_once.ipynb): Collects all subpages and all nested subpages under amsterdam.nl under the section 'onderwepen'
        - [`1_2_1_collect_ams_subpages_individually`](./notebooks/1_supporting_documents_collection/1_2_1_collect_ams_subpages_individually.ipynb) Collects all subpages and all nested subpages under amsterdam.nl under the section 'onderwepen' individually (section by section)
          - [`1_2_2_combine_collected_ams_subpages`](./notebooks/1_supporting_documents_collection/1_2_2_combine_collected_ams_subpages.ipynb): If the webpages have been collected and scraped individually, this notebook combines them all in a single .csv file 'combined.csv'
        - [`3_collect_update_URLs_from_references`](./notebooks/1_supporting_documents_collection/3_collect_update_URLs_from_references.ipynb): This notebook needs to be ran -> it collects all URLs that are referenced in the answers but more importantly it updates the URLs, since some URLs have an outdated version in the answers. It saves the questions with updated URLs 'questions_updated_url.csv'. It also saves a file with questions containing only amsterdam.nl URLs which we use for ranking evaluation and a test set for text generation. The files have been added to the repository, so this step could be skipped.
   


2. [`src`](./src): Folder for all source files specific to this project
3. [`data`](./data): Includes sample data - *to be included*
4. [`tests`](./tests): Test example - *to be included*
5. [`media`](./media): Folder containing media files (icons, video)







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


---


## How it works

*Currently(30.05)*: There are three main steps: 1) Collection of the supporting documents, which is performed through the notebooks under [`URL_Collection`](./notebooks/URL_Collection). 2) Ranking of the supporting documents through the notebooks in [`Ranking`](./notebooks/Ranking). Each notebook performs a different way of ranking. Then the best one is chosen. 3) Text summarization of the top ranked documents performed through the notebooks in [`Reading`](./notebooks/Reading). 



---
## Acknowledgements

*to be included*

