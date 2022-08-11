# CNN_NewsSpider_ByKeywords
![CNN](./CNN_icon.jpg)
CNN(Cable News Network) founded in June 1980 by Ted Turner of Turner Broadcasting Corporation (TBS), it provides all-weather news programs to cable networks and satellite TV users through satellite, and is headquartered in Atlanta, Georgia, USA. CNN Website: [CNN](https://us.cnn.com/)
## Crawl English News Demo(CNN as an example)
### Installation
First, you need to install the corresponding anaconda environment to utilize the relevant dependent libraries by running:  
`
conda env create -f newsspider.yml
`

### Set Types, sections, sort and other info
Second, you can refer to the sections below to restrict the specific categories of content to be crawled through custom URL filtering constraints.  
Sections = us, politics,world,opinion, health/business/entertainment/sport/travel/style, if all CNN just no section  
`
URL = 'https://edition.cnn.com/search?size=10&q=' + keywords + '&sections=us,politics,world,opinion,health' + '&types=article' + '&sort=relevance'
`

### Set keyword and savedir
You can set the keyword and savedir in [CNN_NewsSpider_Keywords.py](CNN_NewsSpider_Keywords.py).  
`
keyword =  
`  
`
savedir = 
`
### Crawl
After setting the necessary information, you can execute the following command to grab:  
`python CNN_NewsSpider_Keywords.py`

### Post-processing
After the crawling is over, you can refer to [Extract_TextContent.py](Extract_TextContent.py) to extract and customize post-processing like duplicate to get the desired content.  
`python Extract_TextContent.py`  

Duplicate content can be removed by the check function and recursive sequence by run:   
`python Fill_Sequence.py`

## Crawl Chinese News Demo(Peaple-Daily as an example)
The code of this part is heavily borrowed from [people-daily-crawler-date](https://github.com/caspiankexin/people-daily-crawler-date)  
[人民日报-人民网 (people.com.cn)](http://paper.people.com.cn/rmrb/html/2021-06/08/nbs.D110000renmrb_01.htm). 

## References  
Many code references [people-daily-crawler-date](https://github.com/caspiankexin/people-daily-crawler-date) , thanks to the relevant authors for their open source. 
