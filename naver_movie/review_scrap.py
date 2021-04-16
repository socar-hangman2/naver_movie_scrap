import math
from tqdm import trange
from .util import get_soup

review_url_form = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={}&order=newest&page={}&onlySpoilerPointYn={}'


def calc_max_page(url):
    max_page = min(end_page, get_max_page(url))
    return max_page if max_page > 0 else False


def get_review_data(movie_id, start_page=1, end_page=-1, spoiler='Y'):
    url = review_url_form.format(movie_id, page, spoiler)
    max_page = calc_max_page(url)

    if max_page == False:
        return "Failed: please check end_page"

    comments = []
    for page in trange(start_page, max_page + 1):
        url = review_url_form.format(movie_id, page, spoiler)
        current_page_comments = get_a_page(get_soup(url))
        comments += current_page_comments
    return comments


def get_a_page(soup):
    comments = []
    for row in soup.select('div[class=score_result] li'):
        try:
            score = int(row.select('div[class=star_score] em')[0].text.strip())
            text = row.select('div[class=score_reple] p')[0].text.strip()

            if text[:4] == '관람객\n':
                text = text[4:].strip()
            if text[:25] == '스포일러가 포함된 감상평입니다. 감상평 보기\n':
                text = text[25:].strip()

            user_id = row.select('div[class=score_reple] em')[0].text.strip()
            comments.append(
                {'score': score,
                 'text': text,
                 'user': user_id
                 })
        except Exception as e:
            return e
            continue
    return comments


def get_max_page(url):
    soup = get_soup(url)
    try:
        num_comments = int(soup.select(
            'div[class="score_total"] em')[-1].text.replace(',', ''))
        return math.ceil(num_comments / 10)
    except Exception as e:
        return -1
