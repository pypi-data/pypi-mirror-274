import pandas as pd
import numpy as np
import nltk
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
import holoviews as hv
from holoviews import opts, dim

def ChordReviews(df, text_column, size=300, stopwords_to_add=[], stemming=False, lemmatization=True, words_to_replace={}):
    """
    Process reviews data, apply text preprocessing, and generate a chord plot visualization showing word co-occurrence patterns and sentiment analysis.

    Args:
    df (pandas.DataFrame): DataFrame containing review data.
    text_column (str): Name of the column containing the text data.
    size (int, optional): Size of the output chord plot (default is 300).
    stopwords_to_add (list, optional): Additional stopwords to be included in the stop words set (default is []).
    stemming (bool, optional): Whether to apply stemming to words (default is False).
    lemmatization (bool, optional): Whether to apply lemmatization to words (default is True).
    words_to_replace (dict, optional): A dictionary where keys are words to be replaced and values are the replacements (default is {}).

    Returns:
    hv.Chord: Chord plot visualization.
    """
    try:
        # Text preprocessing function
        def text_preprocess(raw_text, remove_HTML=True, chars_to_remove=r'\?|\.|\!|\;|\.|\"|\,|\(|\)|\&|\:|\-|\\|\/|\[|\]|\{|\}|\=|\+|\*|\%|\$|\@|\#|\_|\`|\~|\>|\<|\^|\|', 
                            remove_numbers=True, remove_line_breaks=False, 
                            special_chars_to_remove=r'[^\x00-\xfd]', convert_to_lower=True, 
                            remove_consecutive_spaces=True, remove_urls=True, stemming=stemming):
            if type(raw_text) != str:
                raw_text = str(raw_text)
            proc_text = raw_text

            if proc_text == '':
                return proc_text
        
            # Define function to remove URLs from text    
            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            if remove_urls:
                # Convert the input to string
                if not isinstance(raw_text, str):
                    raw_text = str(raw_text)
                # Remove URLs from text
                proc_text = url_pattern.sub('', raw_text)

            # Remove HTML
            if remove_HTML:
                proc_text = BeautifulSoup(proc_text, 'html.parser').get_text()
        
            if stemming:
                stemmer = SnowballStemmer("english")
                proc_text = ' '.join([stemmer.stem(word) for word in word_tokenize(proc_text) if word.isalnum()])
                
            if lemmatization:
                lemmatizer = WordNetLemmatizer()
                # Tokenize the text into words, filter out non-alphanumeric words, and lemmatize each word
                proc_text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(proc_text) if word.isalnum()])

            # Remove punctuation and other special characters
            if len(chars_to_remove) > 0:
                proc_text = re.sub(chars_to_remove, ' ', proc_text)

            # Remove numbers
            if remove_numbers:
                proc_text = re.sub(r'\d+', ' ', proc_text)

            # Remove line breaks
            if remove_line_breaks:
                proc_text = proc_text.replace('\n', ' ').replace('\r', '')

            # Remove special characters
            if len(special_chars_to_remove) > 0:
                proc_text = re.sub(special_chars_to_remove, ' ', proc_text)

            # Normalize to lower case
            if convert_to_lower:
                proc_text = proc_text.lower()

            # Replace multiple consecutive spaces with just one space
            if remove_consecutive_spaces:
                proc_text = re.sub(' +', ' ', proc_text)

            # Replace words
            for word, replacement in words_to_replace.items():
                proc_text = proc_text.replace(word, replacement)

            return proc_text

        # Tokenize words function
        def tokenize_words(words):
            if type(words) != str or word_tokenize(words) == '':
                return np.nan
            else:
                return word_tokenize(words)

        # Function to remove stop words
        def remove_stop_words(text, stop_words):
            if type(text) == list:
                return [w for w in text if w not in stop_words]
            else:
                return np.nan

        # Text preprocessing
        df['PreProcessedText'] = df[text_column].apply(text_preprocess)

        # Tokenize sentences
        sentences = pd.DataFrame(data=[sent_tokenize(text) for text in df['PreProcessedText']], columns=['BaseText'])
        df['RevID'] = df.index
        sentences['RevID'] = sentences.index

        # Convert NA rows into empty strings
        sentences['BaseText'] = sentences['BaseText'].fillna('')

        # Add a column with the review ID
        sentencesPerReview = [len(elem) for elem in sentences['BaseText']]
        sentences['RevID'] = np.repeat(df['RevID'].values, np.repeat(1, len(sentencesPerReview)))

        # Get words
        sentences['Words'] = sentences['BaseText'].apply(tokenize_words)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        stop_words.add("n't")
        stop_words.update(stopwords_to_add)
        sentences['WordsCleaned'] = sentences['Words'].apply(remove_stop_words, stop_words=stop_words)

        # Compute term frequency distribution
        fdist = FreqDist()
        for review in sentences['WordsCleaned']:
            for term in review:
                fdist[term] += 1

        # Transform results to a sorted dataframe
        df_fdist = pd.DataFrame.from_dict(fdist, orient='index', columns=['Frequency'])
        df_fdist.index.name = 'Term'
        df_fdist = df_fdist.sort_values(by='Frequency', ascending=False)

        # Scale the frequency of each word to a 0-100 scale
        df_fdist['Frequency_Scaled'] = df_fdist['Frequency'].apply(lambda number: int(((number - 1) / (len(df_fdist) - 1)) * 100))

        # Preprocess text for word co-occurrence
        sentences['ProcessedText'] = sentences['WordsCleaned'].apply(lambda words: ' '.join(words))

        # Filter words that are not nouns, adjectives, or adverbs
        def filter_grammatical_words(text):
            words = text
            pos_tags = pos_tag(words)

            filtered_words = []
            for word, tag in pos_tags:
                if tag.startswith('N') or tag.startswith('J') or tag.startswith('R'):
                    filtered_words.append(word)

            return ' '.join(filtered_words)

        sentences['FilteredText'] = sentences['WordsCleaned'].apply(filter_grammatical_words)

        # Function to count pairs of words at a certain distance
        def count_word_pairs(df, column_name, n, threshold=1):
            word_pairs_counter = Counter()

            for text in df[column_name]:
                words = text.split()
                for i in range(len(words) - n):
                    if words[i] != words[i + n]:
                        pair = tuple(sorted((words[i], words[i + n])))
                        word_pairs_counter[pair] += 1

            filtered_word_pairs_counter = Counter({pair: count for pair, count in word_pairs_counter.items() if count >= threshold})
            sorted_word_pairs_counter = filtered_word_pairs_counter.most_common()

            return sorted_word_pairs_counter

        # Get word pairs at a distance of 2 that are shown at least 100 times in reviews
        word_pairs_at_distance = count_word_pairs(sentences, 'FilteredText', 2, 100)

        # Convert to DataFrame
        df_word_pairs = pd.DataFrame([{'source': pair[0], 'target': pair[1], 'weight': count} for pair, count in word_pairs_at_distance])

        # Sentiment analysis using VADER
        sid = SentimentIntensityAnalyzer()
        
        def calculate_sentiment_strength(adj, noun):
            text = f"The {noun} is {adj}."
            scores = sid.polarity_scores(text)
            return scores['compound']

        # Add Sentiment Strength column to DataFrame
        df_word_pairs['Sentiment Strength'] = df_word_pairs.apply(lambda row: calculate_sentiment_strength(row['source'], row['target']), axis=1)

        # Binning data according to sentiment strength
        df_word_pairs["Polarity"] = np.where(df_word_pairs["Sentiment Strength"] < -0.33, "Negative", 
                                            np.where(df_word_pairs["Sentiment Strength"] <= 0.33, "Neutral", "Positive"))

        # Select top 50 word pairs
        df_word_pairs = df_word_pairs.head(50)

        # Generate gray scale dictionary
        def generate_gray_scale():
            gray_scale_dict = {}
            for i in range(101):
                gray_value = int(((100 - i) / 100) * 255)  # Invert i to make higher numbers darker
                hex_color = "#{:02x}{:02x}{:02x}".format(gray_value, gray_value, gray_value)
                gray_scale_dict[i] = hex_color
            gray_scale_dict['nan'] = '#000000'  # Black color for NaN values
            return gray_scale_dict

        # Generate the gray scale dictionary
        gray_scale_dictionary = generate_gray_scale()

        df_fdist['Color'] = df_fdist['Frequency_Scaled'].map(gray_scale_dictionary)

        color_map = df_fdist['Color'].dropna().copy()
        color_map = color_map.to_dict()

        hv.extension('matplotlib')
        hv.output(fig='svg', size=size)

        def rotate_label(plot, element):    
            labels = plot.handles["labels"]
            for annotation in labels:        
                angle = annotation.get_rotation()
                if 90 < angle < 270:
                    annotation.set_rotation(180 + angle)
                    annotation.set_horizontalalignment("right")

        chord_plot = hv.Chord(df_word_pairs).opts(
            opts.Chord(edge_cmap={'Negative': '#fe7f81', 'Neutral': '#93e0e6', 'Positive': '#c2ffc1'}, edge_color='Polarity', 
                    labels='index', node_cmap=color_map, node_color='index', hooks=[rotate_label], node_size=0))

        return chord_plot
    except Exception as e:
        print(f"An error occurred: {e}")
        return None