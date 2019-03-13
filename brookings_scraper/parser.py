from .utils import get_soup
from .utils import now
from dateutil.parser import parse
def parse_page(url):
    """
    Argument
    --------
    url : str
        Web page url

    Returns
    -------
    json_object : dict
        JSON format web page contents
        It consists with
            title : article title
            time : article written time
            content : text with line separator \\n
            url : web page url
            scrap_time : scrapped time
    """
    try:
        if '/blog/' in url:
            return parse_blog(url)
        if '/research/' in url:
            return parse_report(url)
        if '/testimonies/' in url:
            return parse_testimony(url)
        if '/bpea-articles/' in url:
            return parse_bpea(url)
    except Exception as e:
        print(e)
        print('Parsing error from {}'.format(url))
        return None

def parse_blog(url):
    def parse_author(soup):
        author = soup.find('h2', class_='name')
        if not author:
            return 'no name'
        return author.find('span', itemprop='name').text

    def parse_title(soup):
        title = soup.find('h1', class_='report-title')
        if not title:
            return ''
        return title.text

    def parse_date(soup):
        date = soup.find('time', itemprop= 'datePublished')['content']
        if not date:
            return None
        return parse(date[:-15])

    def parse_content(soup):
        content = soup.find('div', class_= 'post-body post-body-enhanced')
        if not content:
            return ''
        return content.text

    soup = get_soup(url)
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup),
        'scraping_date': now()
    }

def parse_testimony(url):
    def parse_title(soup):
        title = soup.find('h1', class_='report-title')
        if not title:
            return ''
        return title.text

    def parse_author(soup):
        author = soup.find('span', class_ = 'meta').find('span', itemprop='author')
        if not author:
            return ''
        return author.text

    def parse_date(soup):
        date = soup.find('time', itemprop= 'datePublished')['content']
        if not date:
            return None
        return parse(date[:-15])

    def parse_content(soup):
        p = soup.find('div', class_ = 'post-body post-body-enhanced')
        if not p:
            return ''
        return p.text

    soup = get_soup(url)
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'content': parse_content(soup),
        'author': parse_author(soup),
        'scraping_date': now()
    }


def parse_report(url):
    def parse_title(soup):
        h1 = soup.select('h1[class=report-title]')
        if not h1:
            return ''
        return h1[0].text.strip()

    def parse_author(soup):
        author = soup.find('span', class_ = 'meta').find('span', itemprop='author')
        if not author:
            return ''
        return author.text

    def parse_date(soup):
        date = soup.find('time', itemprop= 'datePublished')['content']
        if not date:
            return None
        return parse(date[:-15])

    def parse_publication_link(soup):
        for a in soup.select('a'):
            if 'https://www.brookings.edu/wp-content/uploads/' in a.attrs.get('href', ''):
                return a.attrs['href']
        return ''

    def parse_content(soup):
        content = soup.find('div', class_= 'post-body post-body-enhanced')
        if not content:
            return ''
        return content.text

    soup = get_soup(url)
    content_url = parse_publication_link(soup)
    return {
        'url': url,
        'author': parse_author(soup),
        'title': parse_title(soup),
        'date': parse_date(soup),
        'content_url': content_url,
        'content': parse_content(soup),
        'scraping_date': now()
    }

def parse_bpea(url):
    def parse_title(soup):
        h1 = soup.select('h1[class=report-title]')
        if not h1:
            return ''
        return h1[0].text.strip()

    def parse_author(soup):
        author = soup.find('span', class_ = 'meta').find('span', itemprop='author')
        if not author:
            return ''
        return author.text

    def parse_date(soup):
        date = soup.find('time', itemprop= 'datePublished')['content']
        if not date:
            return None
        return parse(date[:-15])

    def parse_publication_link(soup):
        for a in soup.select('a'):
            if 'https://www.brookings.edu/wp-content/uploads/' in a.attrs.get('href', ''):
                return a.attrs['href']
        return ''
    def parse_content(soup):
        content = soup.find('div', class_= 'post-body post-body-enhanced')
        if not content:
            return ''
        return content.text

    soup = get_soup(url)
    content_url = parse_publication_link(soup)
    return {
        'url': url,
        'author': parse_author(soup),
        'title': parse_title(soup),
        'date': parse_date(soup),
        'content_url': content_url,
        'content': parse_content(soup),
        'scraping_date': now()
    }
