from config import (                #import variables from config.py
    ANALYSIS_PROMPT,
    MAX_COMMENTS,
    user_agents,
    OUTPUT_C,
    CUSTOM_STOPWORDS
)
from typing import TextIO           #type of file
import requests                     #send HTTP requests,
from bs4 import BeautifulSoup       #extract the messages from web,find_all,find,
import re                           #substitute re.sub,
import time                         #time.sleep use this method to makes the requests not to frequent,
import random                       #use random to provide random user-agent and sleep random time to avoid Anti-scraping,
import csv                          #storage the data with csv form,
from openai import OpenAI           #use deepseek API to analysis data,
from requests.exceptions import HTTPError,RequestException ,Timeout #import more exception type to accurate detect the exception
import matplotlib.pyplot as plt     #show the wordcloud in the pycharm
import jieba                        #divid the words tool
from wordcloud import WordCloud     #show wordcloud diagram
import os                           #import environment to project the API_KEY

class RequestHandler:
    """deal the HTTP request"""
    def __init__(self):
        self.headers = self._get_random_headers()       #make the headers varies, and random choose one

    @staticmethod
    def _get_random_headers():
        return {"User-Agent": random.choice(user_agents)}  # divide a get_random_headers function to avoid the 403

    def get_html_content(self,url):
        """send http request to url"""
        try:
            self.headers = self._get_random_headers()
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()         #raise status
            return response.text
        except HTTPError as he:                                     #deal the different exception
            print(f"Http Error!!!: {he}")
        except Timeout as te:
            print(f"Requests Timeout!!!: {te}")
        except RequestException as req:
            print(f"Request Exception!!!: {req}")
        except Exception as e:
            print(f"Error Fetching{url}: {e}")
        return None

    @staticmethod
    def parse_html(html_content:str,parser='html.parser'):
        return BeautifulSoup(html_content,parser)                       #use beautiful soup get html content

class MovieScrapper:
    """get the movie basic information and comments"""
    def __init__(self): #initialize
        self.request_handler = RequestHandler()

    def get_basic_information(self,movie_url: str) -> dict:
        try:
            html_content = self.request_handler.get_html_content(movie_url)  # use random user-agent to reach the movie_url
            if not html_content:
                return {}

            soup =self.request_handler.parse_html(html_content)  # use BeautifulSoup to get the html content of web, use html.parser to analysis(already combin with parse_html method)
            info_dict = {}  # Create empty dict to storage basic information

            information_items = soup.find_all("div", id="info")  # first reduce the range to the <div><id = info>
            # which is the basic information located range
            for item in information_items:  # loop the item in this range
                try:
                    title_element = soup.find('span',
                                              property='v:itemreviewed')  # find the tag <span><property = 'v:itemreviewed'>
                    info_dict[
                        'title'] = title_element.text.strip() if title_element else "Unknown Title"  # if there is title element exist then collect the title data, otherwise give unknown title tag

                    year_element = soup.find('span',
                                             class_='year')  # find the tag <span><class = year> to gain the year of movie
                    info_dict['year'] = (re.sub(r"[()]", '',
                                                year_element.text).strip() if year_element else "Unknown Year")  # when find the year tag, remove the (), and use .strip()to remove the space and \n

                    rating_element = soup.find('strong',
                                               class_='ll rating_num')  # find the tag<strong><class = ll rating_num>
                    info_dict[
                        'rating'] = rating_element.text.strip() if rating_element else "Not Rated"  # no tag give Not Rated infor

                    directors = [a.text for a in item.find_all('a',
                                                               rel='v:directedBy')]  # loop the items in tag<'a'><rel = 'v:directedBy'>
                    if directors:
                        info_dict['Directors'] = ' / '.join(
                            directors)  # condition is true then add '/' and director element

                    writers = []  # creat a writers list to storage the writers
                    writer_span = item.find('span', string='编剧')  # find the tag<span><string contain '编剧'
                    if writer_span:  # if we find the tag and have element
                        writer_span = writer_span.next_sibling  # use .next_sibling method to gain the next same level tag
                        while writer_span and writer_span.name != 'br':  # make sure the next sibling not <br> tag, which is a branch tag
                            if writer_span.name == 'a':  # after the condition, and is a <a> tag, the writer name is got
                                writers.append(writer_span.text.strip())  # so add it to the list
                            writer_span = writer_span.next_sibling  # move to next sibling again to get all the writers
                    if writers:
                        info_dict['Writer'] = ' / '.join(writers)  # use '/' to separate different writers

                    actors = [a.text for a in
                              item.find_all('a', rel='v:starring')]  # find the tag<a><rel = 'v:starring'>
                    if actors:
                        info_dict['Actor'] = ' / '.join(actors)  # use '/' to separate different actors

                    genres = [a.text for a in item.find_all('span',
                                                            property='v:genre')]  # find the tag with<span><property = 'v:genre'>
                    if genres:
                        info_dict['Type'] = ' / '.join(genres)  # use '/' to separate different genres

                    country_span = item.find('span', string='制片国家/地区:')  # find tag<span><string='制片国家/地区'>
                    if country_span:
                        info_dict[
                            'Producing Country/Area'] = country_span.next_sibling.strip()  # create the key for producing country

                    language_span = item.find('span', string='语言:')  # find tag<span><string = '语言：'
                    if language_span:
                        info_dict[
                            'Language'] = language_span.next_sibling.strip()  # create the key, and store the next same level tag strip

                    release_dates = [span.text for span in item.find_all('span',
                                                                         property='v:initialReleaseDate')]  # loop all the <property = 'v:initialReleaseDate'> tags under the <span>
                    # and transfer the "span" to text form
                    if release_dates:
                        info_dict['Release Date'] = ' / '.join(release_dates)  # separate

                    runtime_span = item.find('span',
                                             property='v:runtime')  # find all the <property = 'v:runtime'> under the span tag
                    if runtime_span:
                        info_dict[
                            'Time Taken'] = runtime_span.text.strip()  # create the key and store text data with removed the space

                    aka_span = item.find('span', string='又名:')  # find all the <span><string = '又名'>tag>
                    if aka_span:
                        info_dict[
                            'Other Name'] = aka_span.next_sibling.strip()  # create a key and store the next same level tag content to dict

                    summary_tag = soup.find('span',
                                            property='v:summary')  # find all the tag<property = 'v:summary'>under the <span>
                    summary = summary_tag.text.strip() if summary_tag else "无简介"
                    if summary:
                        info_dict['Summary'] = summary.strip()  # store the summary strip to the dict with key=Summary

                except (AttributeError, TypeError) as at:
                    print(f"Data parsing error: {at}")  # raise exception when have error and remind extract part have error

                print("\nThe basic information about movie:")  # print out the information
                for key, value in info_dict.items():  # with key : value form
                    print(key + ": " + value)
            return info_dict  # return the information dictionary
        except (AttributeError, TypeError) as at:
            print(f"Data parsing error: {at}")  # raise exception when have error and remind extract part have error

    def get_comments(self,movie_url:str)->list:
        """get the comments for one page"""
        html_content = self.request_handler.get_html_content(movie_url)
        if not html_content:
            return []                   #no html content return empty list

        soup = self.request_handler.parse_html(html_content)
        comment_list = []  # create a comment_list to store data
        comment_items = soup.find_all("div",class_="comment-item")  # first find the tag<div><class='comment-item'>part

        for item in comment_items:  # loop the every comment
            try:
                # username part
                user = item.find('span', class_='comment-info')
                username = user.find('a').string

                # rating part
                rating_tag = item.find('span', class_='rating')
                rating_stars = "no rating"  # initial the rating

                if rating_tag:
                    classes = rating_tag.get('class', [])
                    for c in classes:
                        if c.startswith('allstar'):
                            star_num = int(
                                c.replace('allstar', '')) // 10  # the star is 10-50,divide 10 equal the star
                            rating_stars = f"{star_num} stars"
                            break

                # comment content part
                content = item.find('span',class_='short').text.strip()  # cause extract short comments, so tag<class = 'short'>

                # comment time
                comment_time = item.find('span', class_='comment-time').text.strip()

                comment_list.append({  # append th dict to list
                        'username': username,
                        'rating': rating_stars,
                        'comment-content': content,
                        'comment-time': comment_time,
                    })
            except Exception as e:
                print(f"Extract Comment Have Error: {e}")  # raise th exception, in Extract comment part
                continue
        print(f"\nThis page get comments {len(comment_list)}")  # remind how much comments got
        return comment_list  # return the comment_list, after that will save and print

class CommentCollector:
    """collect comments from different pages"""
    def __init__(self,scraper:MovieScrapper):
        self.scraper = scraper                      #initialize the movie scrapper

    def collect_comments(self,movie_url:str):
        all_comments = []
        useful_pages = 0
        for start in range(0, MAX_COMMENTS, 20):  # start form 0 to 100, every time add 20
            comment_url = movie_url + f"/comments?start={start}"  # sub the num
            print(f"getting comment url: {comment_url}......")  # print the comment url to obviously see the error

            page_comments = self.scraper.get_comments(comment_url)  # use the def get_douban_comments to get one-page comments
            if page_comments:
                all_comments.extend(page_comments)  # store the comments to one total list then print together later
                useful_pages += 1
                time.sleep(random.uniform(1, 3))  # sleep the random seconds to avoid visit to frequent
            else:
                print(f"Page: {start} has no comments")  # if no comments print it out
        print(f"\n{'=' * 200}")
        print(f"Successfully extracted {len(all_comments)} comments")
        return all_comments, useful_pages   #return the list and the working pages

    @staticmethod
    def display_sample_comments(comments:list, count = OUTPUT_C):

        for idx, comment in enumerate(comments[0:count]):
            print("=" * 200)                                # print all the comments out
            print(f"\nComment #{idx + 1}:")                 # order
            print(f"\n**User:{comment['username']}")
            print(f"\n**Rating:{comment['rating']}")
            print(f"\n**Comment Content:{comment['comment-content']}")
            print(f"\n**Comment Time:{comment['comment-time']}")

class DataStorage:

    @staticmethod
    def save_basic_info(info_dict,filename:str):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:  # open a csvfile with write mode
                writer = csv.writer(csvfile)

                writer.writerow(['key' + '   |   ' + 'value'])  # head
                for key, value in info_dict.items():
                    writer.writerow([key, value])

            print(f"Successfully save basic info to csv:{filename}")
        except Exception as e:
            print(f"Failed to save basic info to csv:{e}")

    @staticmethod
    def save_comments(comments,filename):
        try:
            csvfile: TextIO
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:  # create a csvfile:TextIO
                fieldnames = ['username', 'rating', 'comment-content', 'comment-time']  # define the fieldnames
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()  # write the fieldnames

                for comment in comments:
                    writer.writerow({
                        'username': comment['username'],  # write the comments
                        'rating': comment['rating'],
                        'comment-content': comment['comment-content'],
                        'comment-time': comment['comment-time'],
                    })
            print(f"Successfully save comments to csv:{filename}")  # store the comments in csv form

        except Exception as e:
            print(f"Failed to save comments to csv:{e}")  # raise exception for failed to save

    @staticmethod
    def read_file_to_string(filename:str)->str:
        try:
            with open(filename, 'r', encoding='utf-8') as f:  # open with read mode, then return as string
                return f.read()
        except Exception as e:
            print(f"Error Reading {filename}:{e}")  # raise exception for error
            return ""

class DataAnalyzer:

    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")                #get the environment api

    def analyze_movie_data(self,basic_info_file:str,comments_file:str):
        if not self.api_key:
            print("Didn't find the DeepSeek API key...")
            print("^_^  May be you should set a DeepSeek API key on your environment.")
            return None

        basic_info_str = DataStorage.read_file_to_string(basic_info_file)
        comments_str = DataStorage.read_file_to_string(comments_file)               #read the file of basic information and comments

        formatted_prompt = ANALYSIS_PROMPT.format(basic_info_str=basic_info_str,comments_str=comments_str)

        client = OpenAI(
            api_key=self.api_key,  # API and deepseek url
            base_url="https://api.deepseek.com")

        messages = [{"role": "system",
                     "content": "你是一个专业的电影数据分析助手，擅长从观众评论中提取情感倾向并生成结构化报告。"},
                    {"role": "user", "content": formatted_prompt}]

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True  # use stream output
            )

            print("\n=== Analyse Results ===\n")
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)  # print alive
                    full_response += content
            return full_response

        except Exception as e:
            print(f"\nFailed For Analysing: {e}")  # raise exception when analyze
            return None

class WordCloudGenerator:
    """create the world cloud"""
    def __init__(self):
        self.stopwords = CUSTOM_STOPWORDS       #initialize the stopwords

    def generate_wordcloud(self,content_file, font_path='simhei.ttf'):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:            #open the comment file
                content = f.read()
                print(f"get the file: {content_file}, number of charactor: {len(content)}")
        except Exception as e:                  #raise exception
            print(f"fail to get the file: {e}")
            return

        words = self._process_content(content)          #deal the content text and form the count of words
        word_counts = self._count_words(words)

        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        print("\nFrequent words(After filter):")
        for word, count in sorted_words[:20]:
            print(f"{word}: {count}times")

        txt = ' '.join(words)
        wc = self._create_wordcloud(txt,font_path)

        output_file = "wordcloud.png"
        wc.to_file(output_file)
        print(f"wordcloud diagraph forms: {output_file}")
        return wc

    def _process_content(self,content:str):             #deal content
        words = jieba.cut(content)
        return [word for word in words if self._is_valid_word(word)]        #filter the valid words

    def _is_valid_word(self,word):
        if len(word) <= 1:                  #filter the word length longer than 1
            return False
        if any(char.isdigit() for char in word):        #remove the numbers,like years and rating
            return False
        if word in self.stopwords:                  #remove stopwords like useless words
            return False
        return True

    @staticmethod
    def _count_words(words):                              #statistic the frequent words
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        return word_counts

    @staticmethod
    def _create_wordcloud(text:str, font_path='simhei.ttf'):
        return WordCloud(
            font_path=font_path,  # font path
            width=1000,
            height=700,
            background_color='white',
            max_words=300,  # show word limit
            min_font_size=20,  # set the minimum font size
            max_font_size=140,  # set the maximum font size
            random_state=42,  # promise the random state
            collocations=False  # avoid repetitive words
        ).generate(text)

    @staticmethod
    def display_wordcloud(wordcloud: WordCloud):                #use plt method shows the wordcloud
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        plt.show()

class MovieAnalysisApp:
    """main app, combin all the functions"""
    def __init__(self):
        self.scraper = MovieScrapper()                                  #initialize all the functions
        self.comment_collector = CommentCollector(self.scraper)
        self.data_storage = DataStorage()
        self.analyzer = DataAnalyzer()
        self.wordcloud_gen = WordCloudGenerator()
        self.movie_id =""

    def run(self):                      #run the app
        try:
            self._get_movie_url()
            self._process_movie_data()
            self._generate_analysis()
        except KeyboardInterrupt:
            print("\nProgramme interrupted by user (T_T)/")
        except Exception as e:
            print(f"\nFailed For Movie Analysis: {e}")

    def _get_movie_url(self):
        """get the movie url by user input"""
        self._url = input("Please print the URL of a Douban Movie (for example:https://movie.douban.com/subject/30433456/):")

        if self._url.endswith('?from=showing'):         #deal the error make by user click the film from showing part on web
            self._url = self._url.replace('?from=showing', '')

        if not self._url.endswith('/'):  # ask for movie url, and if no / at the end, add it auto, avoid the error
            self._url += "/"

        try:
            self.movie_id = self._url.split("/")[-2]  # get movie id for write csv title
            if not self.movie_id.isdigit():
                self.movie_id = "movie"
        except:
            self.movie_id = "movie"

    def _process_movie_data(self):
        """get the basic information and comments about the movie"""
        basic_info = self.scraper.get_basic_information(self._url)
        if basic_info:
            self.data_storage.save_basic_info(basic_info,f"{self.movie_id}_basic_info.csv")         #save the basic info to csv
        else:
            print("Didn't get the basic information, skip saving...")

        all_comments,valid_pages = self.comment_collector.collect_comments(self._url)
        if all_comments:
            self.comment_collector.display_sample_comments(all_comments)
            self.data_storage.save_comments(all_comments,f"{self.movie_id}_comments.csv")           #save comments
        else:
            print("Didn't get the comments, skip saving...")

    def _generate_analysis(self):
        comments_file = f"{self.movie_id}_comments.csv"
        wordcloud = self.wordcloud_gen.generate_wordcloud(comments_file)

        if wordcloud:
            self.wordcloud_gen.display_wordcloud(wordcloud)

        print("For now you get the : "                                      #if user don't want use deepseek api can choose no
              "\n1.basic information of this movie"
              "\n2.the comments of this movie"
              "\n3.the wordcloud of this movie"
              "\nif the maximum comments set too big, you can stop analysis.")
        prep = input("\nStart analysis? (y/n): ").lower()
        if prep == "y":
            print("\nAnalysing Data...")
            self._perform_analysis() # give deepseek to analysis data

    def _perform_analysis(self):
        basic_file = f"{self.movie_id}_basic_info.csv"
        comments_file = f"{self.movie_id}_comments.csv"             #set the name of file open

        analysis_result = self.analyzer.analyze_movie_data(basic_file, comments_file)   #use deep seek analyze
        if analysis_result:
            analysis_file = f"{self.movie_id}_analysis.csv"
            with open(analysis_file, mode='w', newline='',encoding='utf-8') as f:                #save the analyzed result
                f.write(analysis_result)
            print(f"\nAnalysis Result Store In to: {analysis_file}")

if __name__ == "__main__":
    app = MovieAnalysisApp()
    app.run()
