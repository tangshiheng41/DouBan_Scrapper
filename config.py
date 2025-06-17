        ##Some Values
#several user_agents for headers
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

    ]

#The prompt send to deepseek
ANALYSIS_PROMPT ="""
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
"""

#STOPWORDS
CUSTOM_STOPWORDS = {
    "的", "了", "在", "是", "我", "有", "和", "就", "也", "都", "这", "要", "去", "还", "不",
    "好", "上", "下", "很", "看", "没", "给", "到", "说", "得", "着", "个", "里", "之", "为",
    "什么", "呢", "啊", "么", "吧", "呀", "这个", "一个", "不是", "就是", "不能", "没有", "可以",
    "觉得", "一部", "电影", "这部", "片子", "导演", "演员", "剧情", "角色", "感觉", "故事", "真的",
    "我们", "自己", "看到", "非常", "特别", "如此", "出来", "然后", "因为", "所以", "而且", "什么",
    "人", "事", "时", "会", "被", "对", "过", "而", "年", "月", "日", "一", "二", "三", "四",
    "五", "六", "七", "八", "九", "十", "以及", "虽然", "但是", "如果", "那么", "一定", "一样",
    "一点", "一些", "一下", "一种", "一些", "一样", "不要", "不会", "可能", "应该", "很多", "这种",
    "那种", "怎么", "这样", "那样", "大家", "这样", "那样", "这种", "那种", "还有", "他们", "她们",
    "它们", "你们", "我们", "只是", "已经", "现在", "之后", "之前", "之后", "其实", "为什么","跟","但",
    "还是","又","这么","把","与","大","最后","小","来","让","能","有些","不过","太","更","后","多",
    "任何","还要","只有","甚至","任何","相当","除了","看着","吗",
    "的", "了", "在", "是", "我", "有", "和", "就", "也", "都", "这", "要", "去", "还", "不",
    "好", "上", "下", "很", "看", "没", "给", "到", "说", "得", "着", "个", "里", "之", "为",
    "什么", "呢", "啊", "么", "吧", "呀", "跟", "但", "还是", "又", "这么", "把", "与", "大",
    "最后", "小", "来", "让", "能", "有些", "不过", "太", "更", "后", "多", "都", "又", "也","stars",
    "那个","你","却","中","真","等","感","地","走","像是","rating","对于","当","前",

    # 指示代词和数量词
    "这个", "一个", "不是", "就是", "不能", "没有", "可以", "一点", "一些", "一下", "一种",
    "一样", "不要", "不会", "可能", "应该", "很多", "这种", "那种", "怎么", "这样", "那样",
    "各种", "几分", "多次", "每个", "每次",

    # 人称代词
    "我们", "自己", "他们", "她们", "它们", "你们", "人们", "咱们",

    # 时间相关词
    "时候", "现在", "之后", "之前", "然后", "其实", "当时", "时间", "刚刚",
    "起初", "终于", "最后", "原来", "后来", "平时", "从来", "总是", "有时",

    # 地点和方位词
    "这里", "那里", "哪里", "外面", "面前", "旁边", "上面", "下面", "左边", "右边", "中间",

    # 情感表态词 (过于通用)
    "觉得", "感觉", "真的", "非常", "特别", "如此", "真的", "太", "好", "还好", "简直", "实在",
    "挺", "最好", "最为", "尤其", "有点", "算是", "算是",

    # 电影术语高频词 (需要避免通用术语)
    "电影", "片子", "剧情", "角色", "故事", "导演", "演员", "表演", "部分", "场景", "画面",
    "戏份", "镜头", "情节", "方面", "内容", "发展", "人物", "表现", "效果", "节奏",

    # 图片中高频但无意义的词 (从您的词云图中提取)
    "为了", "作为", "找到", "出现", "体验", "后面", "后面", "最后", "开始", "开始", "继续",
    "用", "来", "到", "是", "有", "在", "的", "了", "而", "但", "可", "啊", "吧", "其实",
    "就是", "属于", "各种", "算是", "新", "并", "最", "好", "带", "能", "没", "可以", "这么",
    "这么", "不过", "更", "有些", "有点", "真的", "部分", "后面", "开始",

    # 无实义动词
    "开始", "继续", "出来", "进去", "进去", "回到", "来到", "达到", "变成", "成为", "认为", "可能",

    # 英文停用词 (根据您的词云图添加)
    "s", "as", "ars", "girl", "with", "the", "and", "of", "in", "to", "a", "is", "was", "were","stars","Stars","STARS","Star",

    # 单字词 (几乎全部排除)
    "他", "她", "它", "而", "且", "虽", "然", "因", "果", "从", "向", "往", "只", "仅", "又",
}

        ##Constant
#The maximum comments get from website
MAX_COMMENTS=200
#The amount of comments want to show on the RUN
OUTPUT_C = 5