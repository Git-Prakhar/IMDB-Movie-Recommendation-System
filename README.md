# Thought Process for the Recommendation Model: 

## 1. Combine text data from important columns into a single column.
- The text data from the columns `overview`, `keywords`, `cast`, `crew`, and `genres` are combined into a single column `tags` to form a corpus of text data for each movie.
## 2. Text Cleanup.
- The text data is cleaned up by lowering the text, stemming the words, and removing the stopwords.
    - **Stemming** is the process of reducing the words to their root form. For example, the words `running`, `ran`, `runs` will all be reduced to `run`.
    - **Stopwords** are the words that are very common and do not add much value to the text data. For example, `is`, `the`, `and`, etc. are stopwords.
- The text data is cleaned up to remove any unwanted characters, symbols, and numbers.
## 3. Creating Vectors from the text data.
- The text data is converted into vectors using the Bag Of Words model **(CountVectorizer from sklearn.feature_extraction.text)**.
    - The Bag Of Words model is used to convert the text data into numerical data that can be used by the machine learning model for calculating the similarity/distance between the text data for different movies.
    - The Bag Of Words model creates a matrix where each row represents a single document (movie in this case) and each column represents a single word from the text data.
    - The value in each cell is the frequency of the word in the single document.
- The first 5000 most frequent words from the entire corpus (all the text for all the rows combined) are used as the columns for the matrix.
- It looks something like this:
        <table>
        <tr>
            <td>word1</td>
            <td>word2</td>
            <td>word3</td>
            <td>...</td>
            <td>word5000</td>
        </tr>
        <tr>
            <td>0</td>
            <td>1</td>
            <td>0</td>
            <td>...</td>
            <td>0</td>
        </tr>
        <tr>
            <td>1</td>
            <td>0</td>
            <td>0</td>
            <td>...</td>
            <td>0</td>
        </tr>
        <tr>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>...</td>
            <td>0</td>
        </tr>
    </table>
## 4. Calculating the Cosine Similarity.
- The cosine similarity is calculated between the vectors of the text data for different movies.
    - The cosine similarity is a metric used to determine how similar the text data of two movies is using the angle between their vectors.
    - The cosine similarity value ranges from -1 to 1, where 1 means the text data is very similar, 0 means no similarity, and -1 means dissimilarity.
- The cosine similarity matrix is created where each row and column represent a movie, and the cell value represents the cosine similarity between the movies.
- The diagonal of the matrix will have a value of 1 as it represents the similarity of the movie with itself.
- It looks something like this:
    <table>
        <tr>
            <td>Movie1</td>
            <td>Movie2</td>
            <td>Movie3</td>
            <td>...</td>
            <td>MovieN</td>
        </tr>
        <tr>
            <td>1</td>
            <td>0.8</td>
            <td>0.2</td>
            <td>...</td>
            <td>0.5</td>
        </tr>
        <tr>
            <td>0.8</td>
            <td>1</td>
            <td>0.6</td>
            <td>...</td>
            <td>0.3</td>
        </tr>
        <tr>
            <td>0.2</td>
            <td>0.6</td>
            <td>1</td>
            <td>...</td>
            <td>0.7</td>
        </tr>
        <tr>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
        </tr>
    </table>
## 5. Creating the Recommendation Function.
- The recommendation function takes the movie title as input and then finds its index in the dataframe.
- It then fetches the row of the cosine similarity matrix for that movie.
- It sorts the values in the row in descending order to get the indices of the most similar movies.
- It returns the titles of the top 5 most similar movies.