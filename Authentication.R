library(twitteR)
library(rtweet)
library(ROAuth)
library(sentimentr)
library(tm)
library(plyr)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)
library(syuzhet)
library(ggplot2)

download.file(url="http://curl.haxx.se/ca/cacert.pem", destfile="cacert.pem")  #downloads the certificate

consumerKey <- "Consumer key"
consumerSecret <- "Consumer Secret Key "
accessToken <- "Access Tokens"
accessTokenSecret <- "Access Token Secret key"


requestURL<- "https://api.twitter.com/oauth/request_token"
accessURL<- "https://api.twitter.com/oauth/access_token"
authURL<- "https://api.twitter.com/oauth/authorize"

setup_twitter_oauth(consumerKey,consumerSecret,accessToken,accessTokenSecret)

#cred <- OAuthFactory$new(consumerKey=consumerKey, 
#                         consumerSecret=consumerSecret,
#                         requestURL='https://api.twitter.com/oauth/request_token',
#                         accessURL='https://api.twitter.com/oauth/access_token',
#                         authURL='https://api.twitter.com/oauth/authorize')

#cred$handshake(cainfo="cacert.pem") ##4867698

input_data <- read.csv("vals.txt", header = FALSE, fileEncoding = "UTF-8-BOM", stringsAsFactors=FALSE)

#input_data <- readtext::readtext("names.csv")
handle=input_data[1]
number=input_data[2]

#search TWitter
searched_tweets<- searchTwitteR(searchString=handle, resultType="recent",n=number, lang="en")
#can use since and until parameters also
# can use geocode to filter tweets
#searched_tweets

#Converting into Dataframe 
tweets.df = do.call("rbind",lapply(searched_tweets,as.data.frame))
tweet_export=tweets.df$text
write.table(tweet_export,file="tweets.txt", append= FALSE, sep="\n")

#tm::findFreqTerms(tweet_export,lowfreq = 0, highfreq = Inf)

#tweet_list<-dplyr::glimpse(tweets.df$text)

#sentimentr::sentiment(tweet_export)$sentiment
sentiment_values=sentiment_by(tweet_export,by=NULL,averaging.function = sentimentr::average_downweighted_zero)$ave_sentiment

pos_neg_terms<-tweet_export%>%extract_sentiment_terms()
write_as_csv(pos_neg_terms,file_name = "tweet_sentiment.csv",na="NA")

#jpeg('hist.jpg',hist(sentiment_values, freq=TRUE)
pdf("sentiment_histogram.pdf")
hist(sentiment_values, freq=NULL)
dev.off()
#Converting into Dataframe 
tweets.df = do.call("rbind",lapply(searched_tweets,as.data.frame))
tweet_export=tweets.df$text
write.table(tweet_export,file="tweets.txt", append= FALSE, sep="\n")
tweet_export

tweet_export<-gsub("<.*>", "", tweet_export) 
tweet_export<-gsub("&amp;", "", tweet_export) 
tweet_export<-gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", tweet_export)
tweet_export<-gsub("@\\w+", "", tweet_export) 
tweet_export<-gsub("[[:punct:]]", "", tweet_export)
tweet_export<-gsub("&amp;", "", tweet_export)
tweet_export<-gsub("[[:digit:]]", "", tweet_export)
tweet_export<-gsub("http\\w+", "", tweet_export) 
tweet_export<-iconv(from = "latin1", to = "ASCII", sub="",tweet_export) 
tweet_export<-gsub("[ \t]{2,}", " ", tweet_export) 
tweet_export<-gsub("^\\s+|\\s+$", "", tweet_export)


docs <- Corpus(VectorSource(tweet_export))
docs = tm_map(docs, removeWords, stopwords("english"))
dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
write.table(head(d, 10),file="frequency.csv",append=FALSE)
head(d,20)
set.seed(1234)
pdf("Wordcloud.pdf")
pdf.options(title="Word Cloud for Search")
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))
frequent_terms=tm::findFreqTerms(dtm,lowfreq = 0, highfreq = Inf)
dev.off()
pdf("sentiment_barplot.pdf")
barplot(d[1:10,]$freq, las = 2, names.arg = d[1:10,]$word,
        col ="lightblue", main ="Most frequent words",
        ylab = "Word frequencies")
dev.off()

#tweet_list<-dplyr::glimpse(tweets.df$text)

#sentimentr::sentiment(tweet_export)$sentiment
sentiment_values=sentiment_by(tweet_export,by=NULL,averaging.function = sentimentr::average_downweighted_zero)$ave_sentiment

pos_neg_terms<-tweet_export%>%extract_sentiment_terms()
pos_values=pos_neg_terms$positive
write_as_csv(pos_neg_terms,file_name = "tweet_sentiment.csv",na="NA")

#jpeg('hist.jpg',hist(sentiment_values, freq=TRUE)
pdf("sentiment_histogram.pdf")
hist(sentiment_values, freq=NULL)
dev.off()


#Sentiment Analysis
result <- get_nrc_sentiment(as.character(tweet_export))
result1<-data.frame(t(result))
new_result <- data.frame(rowSums(result1))
names(new_result)[1] <- "count"
new_result <- cbind("sentiment" = rownames(new_result), new_result)
rownames(new_result) <- NULL
pdf("SentimentAnalysis.pdf")
qplot(sentiment, data=new_result[1:10,], weight=count, geom="bar",fill=sentiment)+ggtitle("Sentiment of Tweets")
dev.off()

