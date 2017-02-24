# -*- coding: utf-8 -*-
from textblob.classifiers import NaiveBayesClassifier
import sklearn
import re
import tweepy


def clean_tweet(text):
    remove_line = re.sub('\n', '', text.encode("utf-8"))
    remove_whitespaces = remove_line.strip(" ")
    remove_url = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', remove_whitespaces)
    remove_quotes = re.sub('[^a-zA-Z0-9 ]', '', remove_url.lower())
    return remove_quotes


def label_data(data, label):
    return [[d, label] for d in data]


class TweetClassifier:
    def __init__(self):
        consumer_key = "wM2F3XWOgOSvOikMu7x1imXZP"
        consumer_secret = "CLhBpZMWZIaoLyLoI1PkMf8EF1O736QcRZAWLrRIrETZMuMNWR"
        access_key = ""
        access_secret = ""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.limit_tweets = 10

    def find_by_hash_tag(self, tag):
        tweets = tweepy.Cursor(self.api.search, q='#{}'.format(tag)).items(self.limit_tweets)
        return [clean_tweet(tweet.text) for tweet in tweets if (tweet.lang == "en") and (not tweet.retweeted) and ('RT @' not in tweet.text)]

    def find_by_account(self, account):
        tweets = self.api.user_timeline(account, count=100)
        return [clean_tweet(tweet.text) for tweet in tweets if (tweet.lang == "en") and (not tweet.retweeted) and ('RT @' not in tweet.text)]

    def get_train_data(self):
        personal_tweets = self.find_by_hash_tag("Personal")
        business_tweets = self.find_by_hash_tag("business")
        return label_data(personal_tweets, "personal") + label_data(business_tweets, "business")

    def get_train_data_by_tags(self, tags):
        train_data = []
        for tag in tags:
            train_data += label_data(self.find_by_hash_tag(tag), tag)
        return train_data

    def get_test_data(self, account_id):
        return self.find_by_account(account_id)

    def classify_account_tags(self, account_id, tags):
        train_data = self.get_train_data_by_tags(tags)
        test_data = self.get_test_data(account_id)
        print "Training NB classifier...."
        cl = NaiveBayesClassifier(train_data)
        result = {}
        for tag in tags:
            result[tag] = []
        for d in test_data:
            label = cl.classify(d)
            result[label].append(d)
        return result

    def classify_account(self, account_id):
        train_data = self.get_train_data()
        test_data = self.get_test_data(account_id)
        # Training NB Classifier
        print "Training NB classifier...."
        cl = NaiveBayesClassifier(train_data)

        return [{'text': d, 'label': cl.classify(d)} for d in test_data]


# Printing measurements
# print "Calculating Accuracy and Confusion Matrix"
# test_confu_mat = sklearn.metrics.confusion_matrix(testgiven, testpred)
# test_accu_score = sklearn.metrics.accuracy_score(testgiven, testpred)
#
# print "Accuracy"
# print test_accu_score
#
# print "Confusion Matrix"
# print test_confu_mat
