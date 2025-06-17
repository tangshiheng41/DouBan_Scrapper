import requests                     #send HTTP requests,
from bs4 import BeautifulSoup       #extract the messages from web,find_all,find,
import re                           #substitute re.sub,
import time                         #time.sleep use this method to makes the requests not to frequent,
import random                       #use random to provide random user-agent and sleep random time to avoid Anti-scraping,
import csv                          #storage the data with csv form,
from openai import OpenAI           #use deepseek API to analysis data,

def get_basic_information(movie_url,headers):
    try:
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
                info_dict['year'] = re.sub(r'[()]', '', year_element.text).strip() if year_element else "Unkown Year"       #when find the year tag, remove the (), and use .strip()to remove the space and \n

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


            except Exception as e:
                print(f"Extract information have Error: {e}")           #raise exception when have error and remind extract part have error

            print("\nThe basic information about movie:")           #print out the information
            for key, value in info_dict.items():                    #with key : value form
                print(key + ": " + value)
        return info_dict                                            #return the information dictionary
    except Exception as e:
        print(f"When getting comment something went wrong: {e}")    #raise exception
        return {}

def get_douban_comments(movie_url,headers):                                  #get comments part and store the infor to list
    try:
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
    except Exception as e:
        print(f"When getting  DouBan comment something went wrong: {e}")            #raise the exception, in get_douban comment part
        return []

def get_comment_url(movie_url,headers):
    all_comment = []                                            #create a all_comment list
    for start in range(0,100,20):                               #start form 0 to 100, every time add 20
        comment_url = movie_url+f"/comments?start={start}"      #sub the num
        print(f"getting comment url: {comment_url}......")      #print the comment url to obviously see the error

        page_comments = get_douban_comments(comment_url,headers)#use the def get_douban_comments to get one page comments
        if page_comments:
            all_comment.extend(page_comments)                   #store the comments to one total list then print together later
            time.sleep(random.uniform(1,3))                #sleep the random seconds to avoid visit to frequent
        else:
            print(f"Page: {start} has no comments")             #if no comments print it out
    print(f"\n{'='*200}")
    print(f"Successfully extracted {len(all_comment)} comments")
    for idx, comment in enumerate(all_comment):
        print("=" * 200)                                                #print all the comments out
        print(f"\nComment #{idx + 1}:")         #order
        print(f"\n**User:{comment['username']}")
        print(f"\n**Rating:{comment['rating']}")
        print(f"\n**Comment Content:{comment['comment-content']}")
        print(f"\n**Comment Time:{comment['comment-time']}")
    return all_comment                                                  #return the list

def save_basic_info_to_csv(info_dict,filename):
    try:
        with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:       #open a csvfile with write mode
            writer = csv.writer(csvfile)

            writer.writerow(['key'+'   |   '+'value'])                  #head
            for key, value in info_dict.items():
                writer.writerow([key,value])

        print(f"Successfully save basic info to csv:{filename}")
    except Exception as e:
        print(f"Failed to save basic info to csv:{e}")

def save_comments_to_csv(comments,filename):
    try:
        with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:       #create the csvfile
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

    client = OpenAI(
        api_key="sk-e318a20fd4ae4f68b9d90bfc3c362930",                      #API and deepseek url
        base_url="https://api.deepseek.com")


    messages=[                          #prompt
        {"role": "system", "content": "你是一个专业的电影数据分析助手，擅长从观众评论中提取情感倾向并生成结构化报告。"},
        {"role": "user", "content": f"""
        ### 任务要求：
请基于以下电影信息和观众评论，完成以下分析：

### 电影基本信息：
{basic_info_str}

### 观众评论（共 100 条）：
{comments_str}

---

### 分析步骤：
1. **情感得分计算**：
   - 对每条评论进行情感分类（正面/中性/负面），评分规则：
     - 正面情感：+1 分（明确赞扬、推荐）
     - 中性情感：0 分（客观描述、无强烈倾向）
     - 负面情感：-1 分（批评、失望）
   - 计算全体评论的平均得分（范围 [-1, 1]），保留 2 位小数。
   - 统计正面/中性/负面评论的占比（百分比）。

2. **高频意见提取**：
   - **积极方面**：列出 3-5 个最常见表扬点（如演技、剧情、特效等），附带代表性评论例句。
   - **消极方面**：列出 3-5 个最常见批评点（如节奏拖沓、逻辑漏洞等），附带代表性评论例句。

3. **结构化报告**：
   请按以下格式输出结果：

   ---
   ### 电影情感分析报告：《movie_title》
   **1. 情感分布可视化图表**  
   - 平均情感得分：score（interpretation）  
   - 正面评论：pos_pct%  
   - 中性评论：neutral_pct%  
   - 负面评论：neg_pct%  

   **2. 观众反馈总结**  
   - 👍 **主要优点**：  
     1. 优点1（例句："评论片段"）  
     2. 优点2（例句："评论片段"）  
     3. 优点3（例句："评论片段"）  
   - 👎 **主要缺点**：  
     1. 缺点1（例句："评论片段"）  
     2. 缺点2（例句："评论片段"）  
     3. 缺点3（例句："评论片段"）  

   **3. 改进建议**  
   - 针对 缺点1，建议：具体改进方向  
   - 针对 缺点2，建议：具体改进方向 
   ---

### 附加要求：
- 情感分类需基于评论内容而非评分星级。
- 若评论同时包含正负面内容，按主导情感归类。
- 优先选择高赞或详细评论作为例句。
"""}
]

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


def main():

    user_agents= [

        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',

        'Opera/8.0 (Windows NT 5.1; U; en)',

        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',

        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',

        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',

        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',

        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',

        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',

        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',

        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',

        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',

        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',

        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',

        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',

        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',

        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',

        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',

        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",

        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",

        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",

        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",

        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",

        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",

        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",

        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",

        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",

        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",

        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",

        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"

    ]               #several user_agents for headers
    _HEADERS = {"User-Agent": (random.choice(user_agents))}         #random choose user_agent

    #ask user to give a url
    _URL = input("Please print the URL of a Douban Movie (for example:https://movie.douban.com/subject/30433456/):")
    if not _URL.endswith("/"):                          #ask for movie url, and if no / at the end, add it auto, avoid the error
        _URL += "/"

    try:
        movie_id = _URL.split("/")[-2]                  #get movie id for write csv title
        if not movie_id.isdigit():
            movie_id = "movie"
    except:
        movie_id = "movie"


    basic_information=get_basic_information(_URL,_HEADERS)      #gain basic information

    if basic_information:
        save_basic_info_to_csv(basic_information,f"{movie_id}_basic_info.csv")              #save the basic information as ...
    else:
        print("Didn't get the basic information, skip saving...")       #skip the error to keep other part work


    all_comments = get_comment_url(_URL,_HEADERS)
    if all_comments:
        save_comments_to_csv(all_comments,f"{movie_id}_comments.csv")       #save the comments as ...
    else:
        print("Didn't get the comments, skip saving...")            #skip the error to keep other parts work

    basic_info_filename = f"{movie_id}_basic_info.csv"          #give the filename
    comments_filename = f"{movie_id}_comments.csv"

    print("\nAnalysing Data...")
    analysis_result = send_2csv_to_deepseek(basic_info_filename, comments_filename)             #give deepseek to analysis data

    if analysis_result:
        with open(f"{movie_id}_analysis.txt", "w", encoding="utf-8") as f:
            f.write(analysis_result)
        print(f"\n\nAnalysed Date is saved to: {movie_id}_analysis.txt")            #save the analysed data


if __name__ == "__main__":              #run programme
    main()
