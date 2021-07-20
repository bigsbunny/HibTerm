from pathlib import Path
import sys
import requests
import click
from bs4 import BeautifulSoup as bs
import re
import html
import time


class Student(object):
    def __init__(self, id, password):
        self.stud_id = id
        self.stud_pass = password

    def student_login(self):
        post_data = {
            "uid": self.stud_id,
            "pwd": self.stud_pass,
            "txtInput": ''
        }

        with requests.session() as s:
            login_response = s.post(
                'https://hib.iiit-bh.ac.in/m-ums-2.0/start/login/auth.php?client=iiit', data=post_data, allow_redirects=True)
            self.session_cookie = login_response.request.headers['Cookie']

        if login_response.text.find("UserID_or_Password_Incorrect") > 0:
            return False
        return True

    def student_greeting(self):
        get_headers = {
            "Cookie": self.session_cookie,
            "Referer": "https://hib.iiit-bh.ac.in/m-ums-2.0/start/here/aisMenu.php?role=STU",
        }

        with requests.session() as s:
            response = s.get(
                'https://hib.iiit-bh.ac.in/m-ums-2.0/app.acadstu/myCV/docDet1.php', headers=get_headers)

        soup_obj = bs(response.text, "html.parser")
        returned = soup_obj.find_all("font")
        student_name = returned[1].contents[0]
        click.echo(click.style(
            "-"*24 + f"\nWelcome, {student_name}\n" + "-"*24 + "\n", fg="bright_blue", bold=True))
        self.notice_parser()

    def notice_parser(self):
        notice_compilation = []
        notice_dates = []
        get_headers = {
            "Cookie": self.session_cookie,
            "Referer": "https://hib.iiit-bh.ac.in/m-ums-2.0/start/here/?w=1536&h=749"
        }

        with requests.session() as s:
            notices_fetched = s.get(
                "https://hib.iiit-bh.ac.in/m-ums-2.0/app.misc/nb/docList.php", headers=get_headers)

        notice_soup = bs(notices_fetched.text, "html.parser")
        notices = notice_soup.find_all("font", attrs={"color": "red"})
        # for _ in notice_soup.find_all("td",attrs={"width": "10%", "align": "Center"}):
        #     notice_dates.append(_.contents[0].contents[0])
        # notice_audience = notice_soup.find_all("font", attrs={"color": "Blue"})
        # notice_links = notice_soup.find_all(href=re.compile(r'docDet\.php\?docid=\d'))

        for _ in range(len(notices)):
            notice_info = {
                "notice_title": notices[_].contents[0],
                "notice_url": notice_soup.find_all(href=re.compile(r'docDet\.php\?docid=\d'))[_].get('href'),
                "notice_date": notice_soup.find_all("td", attrs={"width": "10%", "align": "Center"})[_].contents[0].contents[0],
                "notice_audience": notice_soup.find_all("font", attrs={"color": "Blue"})[_].contents[0]
            }
            notice_compilation.append(notice_info)

        self.notice_compilation = notice_compilation
        self.notice_display(notice_compilation)

    def notice_display(self, notice_compilation):
        ctr = 1
        for notice_dict in notice_compilation:
            click.echo(f'{ctr}--> {notice_dict["notice_title"]}', nl=False)
            click.echo(click.style(
                f'  ({notice_dict["notice_date"]})', fg="bright_red"), nl=False)
            click.echo(click.style(
                f'\n\t{notice_dict["notice_audience"]}\n', fg="cyan"))
            ctr += 1

        self.user_interaction()

    def user_interaction(self):
        while True:
            user_response = click.prompt(
                'Enter notice number to view (or type exit to exit)')
            if (user_response == 'exit'):
                sys.exit()
            else:
                try:
                    self.view_notice(int(user_response))
                except ValueError:
                    click.echo(click.style(
                        'Invalid Response, try again.', fg="bright_red"))
                except IndexError:
                    click.echo(click.style(
                        'Invalid Notice number, try again.', fg="bright_red"))

    def view_notice(self, sl_no):
        has_attachement = ''
        get_headers = {
            "Cookie": self.session_cookie,
            "Referer": "https://hib.iiit-bh.ac.in/m-ums-2.0/app.misc/nb/docList.php"
        }

        notice_url = "https://hib.iiit-bh.ac.in/m-ums-2.0/app.misc/nb/" + \
            self.notice_compilation[sl_no-1]['notice_url']
        notice_id = notice_url[65:]

        with requests.session() as s:
            notice = s.get(notice_url, headers=get_headers)
            has_attachment = check_attachment(notice)

        notice_obj = bs(notice.text, "html.parser")

        click.clear()

        notice_div = notice_obj.find(
            "div", attrs={"class": "well well-lg col-lg-10 col-lg-offset-1 text-left"})
        test = [content for content in notice_div.contents if content != '\n']

        click.echo(click.style(
            f"Posted on: {self.notice_compilation[sl_no-1]['notice_date']}\n", fg="green"))
        for tag in test:
            if tag.name not in ['table', 'ul', 'ol']:
                formatted = re.sub(re.compile(r'<.*?>'), '', str(tag))
                # formatted = re.sub(re.compile(r'<\/?\S*\s*\S*>'),'',formatted)
                click.echo(click.style(
                    f"{html.unescape(formatted)}\n", fg="bright_cyan"))

            elif tag.name == 'table':
                for tr in tag.find_all('tr'):
                    for td in tr.find_all('td'):
                        td_print = [re.sub(re.compile(r'<.*?>'), '', str(content))
                                    for content in td.contents if content != '\n'][0]
                        click.echo(click.style(
                            td_print + "  ", fg="yellow"), nl=False)
                    click.echo()
                click.echo()

            elif tag.name in ['ul', 'ol']:
                for li in tag.find_all('li'):
                    click.echo(click.style(f"-->  {re.sub(re.compile(r'<.*?>'), '', str(li))}",fg="yellow"))
                click.echo()

        if has_attachment:
            self.download_attachment(notice_id)

        while True:
            click.echo("Press b to go back, q to exit:  ", nl=False)
            user_char = click.getchar()
            if user_char == 'b':
                self.notice_display(self.notice_compilation)
            elif user_char == 'q':
                sys.exit('\n')
            else:
                click.echo("Invalid response")

    def download_attachment(self, notice_id):
        attachment_response = ''
        get_headers = {
            "Cookie": self.session_cookie,
            "Referer": "https://hib.iiit-bh.ac.in/m-ums-2.0/app.misc/nb/docDet.php?docid=" + notice_id
        }
        get_headers2 = {
            "Cookie": self.session_cookie,
            "Referer": "https://hib.iiit-bh.ac.in/m-ums-2.0/app.misc/nb/showPDF.php?docid=" + notice_id
        }

        with requests.session() as s:
            attachment_page = s.get(
                "https://hib.iiit-bh.ac.in/m-ums-2.0/app.misc/nb/showPDF.php?docid="+notice_id, headers=get_headers)
            obj = bs(attachment_page.text, "html.parser")
            attachment_href = obj.find("iframe")['src'].split("..")[2]
            attachment_name = obj.find("iframe")['src'].split("/")[6]
            attachment_url = "https://hib.iiit-bh.ac.in/m-ums-2.0/" + attachment_href
            attachment_response = s.get(attachment_url, headers=get_headers2)

        downloads_directory = str(Path.home()/"Downloads")
        with open(f"{downloads_directory}/{attachment_name}", 'wb') as f:
            f.write(attachment_response.content)

        time.sleep(1)

        click.echo(click.style(
            f"Notice Attachment downloaded to '{downloads_directory}'\n", fg="bright_red"))


def check_attachment(notice):
    if notice.text.find('View Attachment') > 0:
        return True
    return False
