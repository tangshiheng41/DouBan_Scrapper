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

def get_random_headers():
    return {"User-Agent":random.choice(user_agents)}    #divid a get_random_headers function to avoid the 403

def get_basic_information(movie_url:str)->dict:
    try:
        headers = get_random_headers()
        response = requests.get(movie_url, headers=headers)                 #use random user-agent to reach the movie_url
        response.raise_for_status()                             #raise the status of movie_url, to check whether the HTTP response
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')   #use BeautifulSoup to get the html content of web, use html.parser to analysis

        info_dict = {}              #Create a empty dict to storage basic information

        information_items = soup.find_all("div", id="info")         #first reduce the range to the <div><id = info>
                                                                        #which is the basic information located range
        for item in information_items:      #loop the item in this range
            try:
                title_element = soup.find('span', property='v:itemreviewed')        #find the tag <span><property = 'v:itemreviewed'>
                info_dict['title'] = title_element.text.strip() if title_element else "Unknown Title"   #if there is title element exist then collect the title data, otherwise give unknown title tag

                year_element = soup.find('span', class_='year')         #find the tag <span><class = year> to gain the year of movie
                info_dict['year'] = (re.sub(r"[()]", '', year_element.text).strip() if year_element else "Unknown Year")       #when find the year tag, remove the (), and use .strip()to remove the space and \n

                rating_element = soup.find('strong', class_='ll rating_num')        #find the tag<strong><class = ll rating_num>
                info_dict['rating'] = rating_element.text.strip() if rating_element else "Not Rated"    #no tag give Not Rated infor

                directors = [a.text for a in item.find_all('a', rel='v:directedBy')]    #loop the items in tag<'a'><rel = 'v:directedBy'>
                if directors:
                    info_dict['Directors'] = ' / '.join(directors)          #condition is true then add '/' and director element

                writers = []            #creat a writers list to storage the writers
                writer_span = item.find('span', string='编剧')           #find the tag<span><string contain '编剧'
                if writer_span:                 #if we find the tag and have element
                    writer_span = writer_span.next_sibling      #use .next_sibling method to gain the next same level tag
                    while writer_span and writer_span.name != 'br':         #make sure the next sibling not <br> tag, which is a branch tag
                        if writer_span.name == 'a':             #after the condition, and is a <a> tag, the writer name is got
                            writers.append(writer_span.text.strip())        #so add it to the list
                        writer_span = writer_span.next_sibling              #move to next sibling again to get all the writers
                if writers:
                    info_dict['Writer'] = ' / '.join(writers)       #use '/' to separate different writers

                actors = [a.text for a in item.find_all('a', rel='v:starring')]         #find the tag<a><rel = 'v:starring'>
                if actors:
                    info_dict['Actor'] = ' / '.join(actors)             #use '/' to separate different actors

                genres = [a.text for a in item.find_all('span', property='v:genre')]        #find the tag with<span><property = 'v:genre'>
                if genres:
                    info_dict['Type'] = ' / '.join(genres)      #use '/' to separate different genres

                country_span = item.find('span', string='制片国家/地区:')         #find tag<span><string='制片国家/地区'>
                if country_span:
                    info_dict['Producing Country/Area'] = country_span.next_sibling.strip()         #create the key for producing country

                language_span = item.find('span', string='语言:')             #find tag<span><string = '语言：'
                if language_span:
                    info_dict['Language'] = language_span.next_sibling.strip()      #create the key, and store the next same level tag strip

                release_dates = [span.text for span in item.find_all('span', property='v:initialReleaseDate')]          #loop all the <property = 'v:initialReleaseDate'> tags under the <span>
                                                                                                                            #and transfer the "span" to text form
                if release_dates:
                    info_dict['Release Date'] = ' / '.join(release_dates)       #separate

                runtime_span = item.find('span', property='v:runtime')      #find all the <property = 'v:runtime'> under the span tag
                if runtime_span:
                    info_dict['Time Taken'] = runtime_span.text.strip()        #create the key and store text data with removed the space

                aka_span = item.find('span', string='又名:')              #find all the <span><string = '又名'>tag>
                if aka_span:
                    info_dict['Other Name'] = aka_span.next_sibling.strip()     #create a key and store the next same level tag content to dict



                summary_tag = soup.find('span', property='v:summary')   #find all the tag<property = 'v:summary'>under the <span>
                summary = summary_tag.text.strip() if summary_tag else "无简介"
                if summary:
                    info_dict['Summary'] = summary.strip()          #store the summary strip to the dict with key=Summary

            except HTTPError as he:
                print(f"HTTP error: {he}")
            except Timeout:
                print("Request timed out")
            except RequestException as req:
                print(f"Network error: {req}")
            except (AttributeError, TypeError) as at:
                print(f"Data parsing error: {at}")          #raise exception when have error and remind extract part have error

            print("\nThe basic information about movie:")           #print out the information
            for key, value in info_dict.items():                    #with key : value form
                print(key + ": " + value)
        return info_dict                                            #return the information dictionary
    except Exception as e:
        print(f"When getting comment something went wrong: {e}")    #raise exception
        return {}

def get_douban_comments(movie_url:str)->list:                                  #get comments part and store the infor to list
    try:
        headers = get_random_headers()
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        comment_list = []                                                   #create a comment_list to store data
        comment_items = soup.find_all("div", class_="comment-item")   #first find the tag<div><class='comment-item'>part

        for item in comment_items:                                          #loop the every comment
            try:
                #username part
                user=item.find('span',class_='comment-info' )
                username = user.find('a').string

                #rating part
                rating_tag = item.find('span',class_='rating')
                rating_stars = "no rating"                                  #initial the rating

                if rating_tag:
                    classes = rating_tag.get('class',[])
                    for c in classes:
                        if c.startswith('allstar'):
                            star_num = int(c.replace('allstar',''))//10     #the star is 10-50,divide 10 equal the star
                            rating_stars = f"{star_num} stars"
                            break

                #comment content part
                content = item.find('span',class_='short').text.strip()             #cause extract short comments, so tag<class = 'short'>

                #comment time
                comment_time = item.find('span',class_='comment-time').text.strip()


                comment_list.append({                                       #append th dict to list
                    'username':username,
                    'rating':rating_stars,
                    'comment-content':content,
                    'comment-time':comment_time,
                })
            except Exception as e:
                print(f"Extract Comment Have Error: {e}")                   #raise th exception, in Extract comment part
                continue
        print(f"\nThis page get comments {len(comment_list)}")              #remind how much comments got
        return comment_list                                                 #return the comment_list, after that will save and print
    # raise the exception, in get_douban comment part
    except HTTPError as he:
        print(f"HTTP error: {he}")
    except Timeout:
        print("Request timed out")
    except RequestException as req:
        print(f"Network error: {req}")
    except (AttributeError, TypeError) as AT:
        print(f"Data parsing error: {AT}")
        #return list
        return []

def get_comment_url(movie_url:str)->list:
    headers = get_random_headers()
    all_comment = []                                            #create a all_comment list
    for start in range(0,MAX_COMMENTS,20):                      #start form 0 to 100, every time add 20
        comment_url = movie_url+f"/comments?start={start}"      #sub the num
        print(f"getting comment url: {comment_url}......")      #print the comment url to obviously see the error

        page_comments = get_douban_comments(comment_url)#use the def get_douban_comments to get one page comments
        if page_comments:
            all_comment.extend(page_comments)                   #store the comments to one total list then print together later
            time.sleep(random.uniform(1,3))                #sleep the random seconds to avoid visit to frequent
        else:
            print(f"Page: {start} has no comments")             #if no comments print it out
    print(f"\n{'='*200}")
    print(f"Successfully extracted {len(all_comment)} comments")
    for idx, comment in enumerate(all_comment[0:OUTPUT_C]):
        print("=" * 200)                                                #print all the comments out
        print(f"\nComment #{idx + 1}:")         #order
        print(f"\n**User:{comment['username']}")
        print(f"\n**Rating:{comment['rating']}")
        print(f"\n**Comment Content:{comment['comment-content']}")
        print(f"\n**Comment Time:{comment['comment-time']}")
    return all_comment                        #return the list

def save_basic_info_to_csv(info_dict:dict,filename):
    try:
        with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:       #open a csvfile with write mode
            writer = csv.writer(csvfile)

            writer.writerow(['key'+'   |   '+'value'])                  #head
            for key, value in info_dict.items():
                writer.writerow([key,value])

        print(f"Successfully save basic info to csv:{filename}")
    except Exception as e:
        print(f"Failed to save basic info to csv:{e}")

def save_comments_to_csv(comments:list,filename):
    try:
        csvfile: TextIO
        with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:       #create a csvfile:TextIO
            fieldnames = ['username','rating','comment-content','comment-time']     #define the fieldnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()                #write the fieldnames

            for comment in comments:

                writer.writerow({
                    'username':comment['username'],                     #write the comments
                    'rating':comment['rating'],
                    'comment-content':comment['comment-content'],
                    'comment-time':comment['comment-time'],
                })
        print(f"Successfully save comments to csv:{filename}")          #store the comments in csv form
    except Exception as e:
        print(f"Failed to save comments to csv:{e}")                #raise exception for failed to save

def read_csv_to_string(filename):
    try:
        with open(filename, 'r',encoding='utf-8-sig') as f :            #open with read mode, then return as string
            return f.read()
    except Exception as e:
        print(f"Error Reading {filename}:{e}")                          #raise exception for error
        return ""

def send_2csv_to_deepseek(basic_info_file,comments_file):
    basic_info_str = read_csv_to_string(basic_info_file)                    #transfer basic information and comments to string
    comments_str = read_csv_to_string(comments_file)
    api_key = os.getenv("DEEPSEEK_API_KEY")
    client = OpenAI(
        api_key=api_key,                                  #API and deepseek url
        base_url="https://api.deepseek.com")

    formatted_prompt = ANALYSIS_PROMPT.format(
        basic_info_str=basic_info_str,
        comments_str=comments_str
    )

    messages=[{"role": "system", "content": "你是一个专业的电影数据分析助手，擅长从观众评论中提取情感倾向并生成结构化报告。"},
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
        print(f"\nAPI Exception: {e}")                      #raise exception when API have error
        return None

def filter_stopwords(words, stopwords):

    return [word for word in words if word not in stopwords]

def generate_wordcloud(content_file, font_path='simhei.ttf'):
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"get the file: {content_file}, number of charactor: {len(content)}")
    except Exception as e:
        print(f"fail to get the file: {e}")
        return

    stopwords = CUSTOM_STOPWORDS
    print(f"already import stopwords: {len(stopwords)}")

    words = jieba.cut(content)
    filtered_words = filter_stopwords(words, stopwords)

    word_counts = {}
    for word in filtered_words:
        if len(word) > 1:
            word_counts[word] = word_counts.get(word, 0) + 1

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    print("\nFrequent words(After filter):")
    for word, count in sorted_words[:20]:
        print(f"{word}: {count}times")

   #combine the text with space between them
    txt = ' '.join(filtered_words)

    #create a wordcloud
    wc = WordCloud(
        font_path=font_path,  # font path
        width=1000,
        height=700,
        background_color='white',
        max_words=300,  # show word limit
        min_font_size=20,  # set the minimum font size
        max_font_size=140,  # set the maximum font size
        random_state=42,  # promise the random state
        collocations=False  # avoid repetitive words
    )

    # form wordcloud
    print("\ncreating wordcloud ...")
    wc.generate(txt)

    # save wordcloud
    output_file = "../3/wordcloud.png"
    wc.to_file(output_file)
    print(f"wordcloud diagraph forms: {output_file}")
    return wc

def start_analysis(movie_id,basic_info_filename,comments_filename,wordcloud_object):
    if wordcloud_object:
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud_object, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    print("For now you get the : "
          "\n1.basic information of this movie"
          "\n2.the comments of this movie"
          "\n3.the wordcloud of this movie"
          "\nif the maximum comments set too big, you can stop analysis.")
    prep = input("\nStart analysis? (y/n): ")
    if  prep == "y":
        print("\nAnalysing Data...")
        analysis_result = send_2csv_to_deepseek(basic_info_filename,comments_filename)  # give deepseek to analysis data

        if analysis_result:
            with open(f"{movie_id}_analysis.txt", "w", encoding="utf-8") as f:
                f.write(analysis_result)
            print(f"\n\nAnalysed Date is saved to: {movie_id}_analysis.txt")  # save the analysed data
    elif prep == "n":
        print("\nAnalysis stopped. See you later!")

def main():

    #ask user to give a url
    _URL = input("Please print the URL of a Douban Movie (for example:https://movie.douban.com/subject/30433456/):")
    if _URL.endswith('?from=showing'):
        _URL = _URL.replace('?from=showing','')

    if not _URL.endswith('/'):                          #ask for movie url, and if no / at the end, add it auto, avoid the error
        _URL += "/"


    try:
        movie_id = _URL.split("/")[-2]                  #get movie id for write csv title
        if not movie_id.isdigit():
            movie_id = "movie"
    except:
        movie_id = "movie"


    basic_information=get_basic_information(_URL)      #gain basic information

    if basic_information:
        save_basic_info_to_csv(basic_information,f"{movie_id}_basic_info.csv")              #save the basic information as ...
    else:
        print("Didn't get the basic information, skip saving...")       #skip the error to keep other part work


    all_comments = get_comment_url(_URL)
    if all_comments:
        save_comments_to_csv(all_comments,f"{movie_id}_comments.csv")       #save the comments as ...
    else:
        print("Didn't get the comments, skip saving...")            #skip the error to keep other parts work

    content_file = f"{movie_id}_comments.csv"  #comments file path
    font_path = "simhei.ttf"  #front file path

    # if no csv files
    try:
        with open(content_file, 'r', encoding='utf-8') as test_file:
            pass
    except:
        print(f"Hints: please create a csv that contain comments '{content_file}'")

    # create a word clouds
    wordcloud_object=generate_wordcloud(content_file, font_path)

    basic_info_filename = f"{movie_id}_basic_info.csv"          #give the filename
    comments_filename = f"{movie_id}_comments.csv"

    start_analysis(movie_id,basic_info_filename,comments_filename,wordcloud_object)


if __name__ == "__main__":              #run programme
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramme interrupted by user.")
    except Exception as e:
        print(f"Occur exception: {e}")
