import json
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Date
from sqlalchemy.orm import sessionmaker
from databasesetup import User, Method, Grade, Ascent, Base
import datetime


def main():
    """Executes all scraping helper methods"""

    lower = int(input("Lower start?"))
    upper = int(input("Upper limit?"))

    ready = input("Ready to start? (y/n)")

    if ready == 'y':
        for i in range(lower, upper + 1):
            user_added = False
            urls = url_maker(i)
            for url in urls:
                climb_dict = scrape_page(url)
                if climb_dict:
                    if not user_added:
                        scrape_user(climb_dict)
                        user_added = True
                    scrape_ascent(climb_dict)
            if user_added:
                print("Ascents and info from user " + str(i) + " added")
            else:
                print("User " + str(i) + " may not exist")


def scrape_page(url):
    """Scrape an 8a.nu page, return a python dictionary containing info"""

    try:
        html_page = requests.get(url, timeout=60)

        if html_page.status_code != 200:
            return False

        soup = BeautifulSoup(html_page.text, "lxml")
        json_info = soup.select("[data-js-react-on-rails-store]")
        climb_dict = json.loads(json_info[0].getText())

        return climb_dict

    except requests.ConnectionError as e:
        print("Connection Error:")
        print(e)
    except requests.Timeout as e:
        print("Timeout Error:")
        print(e)
    except requests.RequestException as e:
        print("General Error:")
        print(e)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")


def url_maker(num):
    """Return a list of well-formatted URLs"""

    url_part_one = "https://beta.8a.nu/scorecard/"
    url_part_two = "/routes/all"
    url_part_three = "/boulders/all"

    urls = [url_part_one + str(num) + url_part_two,
            url_part_one + str(num) + url_part_three]

    return urls


def scrape_grades(climb_dict):
    """Scrape grade information, save to database"""

    session = database_connection()

    for key in climb_dict["gui"]["betaGrades"].keys():
        try:
            grade_info = climb_dict["gui"]["betaGrades"][key]

            id = grade_info['id']
            score = grade_info['score']
            fra_routes = grade_info['fra_routes']
            fra_routes_input = grade_info['fra_routes_input']
            fra_routes_selector = grade_info['fra_routes_selector']
            fra_boulders = grade_info['fra_boulders']
            fra_boulders_input = grade_info['fra_boulders_input']
            fra_boulders_selector = grade_info['fra_boulders_selector']
            usa_routes = grade_info['usa_routes']
            usa_routes_input = grade_info['usa_routes_input']
            usa_routes_selector = grade_info['usa_routes_selector']
            usa_boulders = grade_info['usa_boulders']
            usa_boulders_input = grade_info['usa_boulders_input']
            usa_boulders_selector = grade_info['usa_boulders_selector']

            grade = Grade(id=id, score=score, fra_routes=fra_routes,
                          fra_routes_input=fra_routes_input,
                          fra_routes_selector=fra_routes_selector,
                          fra_boulders=fra_boulders,
                          fra_boulders_input=fra_boulders_input,
                          fra_boulders_selector=fra_boulders_selector,
                          usa_routes=usa_routes,
                          usa_routes_input=usa_routes_input,
                          usa_routes_selector=usa_routes_selector,
                          usa_boulders=usa_boulders,
                          usa_boulders_input=usa_boulders_input,
                          usa_boulders_selector=usa_boulders_selector)

            session.add(grade)
            session.commit()
        except Exception as e:
            print(e)

    session.close()


def scrape_user(climb_dict):
    """Scrape user information"""

    session = database_connection()
    try:
        user_info = climb_dict["importData"][0]["response"]["user"]

        id = user_info['id']
        first_name = user_info['firstName']
        last_name = user_info['lastName']
        city = user_info['city']
        country = user_info['country']
        sex = user_info['sex']
        height = user_info['height']
        weight = user_info['weight']
        started = user_info['started']
        competitions = user_info['competitions']
        occupation = user_info['occupation']
        sponsor1 = user_info['sponsor1']
        sponsor2 = user_info['sponsor2']
        sponsor3 = user_info['sponsor3']
        best_area = user_info['bestArea']
        worst_area = user_info['worstArea']
        guide_area = user_info['guideArea']
        interests = user_info['interests']

        # some deactivated users's bday years are listed as 0000, some have no
        # bday listed

        if user_info['birth']:
            bday_list = list(map(int, user_info['birth'].split('-')))
            if bday_list[0] == 0000:
                birth = None
            else:
                birth = datetime.date(bday_list[0], bday_list[1], bday_list[2])
        else:
            birth = None
        
        presentation = user_info['presentation']
        deactivated = user_info['deactivated']
        anonymous = user_info['anonymous']

        user = User(id=id, first_name=first_name, last_name=last_name,
                    city=city,
                    country=country, sex=sex, height=height, weight=weight,
                    started=started, competitions=competitions,
                    occupation=occupation, sponsor1=sponsor1,
                    sponsor2=sponsor2,
                    sponsor3=sponsor3, best_area=best_area,
                    worst_area=worst_area,
                    guide_area=guide_area, interests=interests, birth=birth,
                    presentation=presentation, deactivated=deactivated,
                    anonymous=anonymous)

        session.add(user)
        session.commit()
    except Exception as e:
        print("User error")
        print(e)
    session.close()


def scrape_ascent(climb_dict):
    """Scrape ascent information"""

    session = database_connection()
    try:
        ascents = climb_dict["importData"][0]["response"]["ascents"]["ascents"]
        try:
            for _ascent in ascents:
                id = _ascent['id']
                user_id = _ascent['userId']
                grade_id = _ascent['grade']
                notes = _ascent['notes']
                raw_notes = _ascent['rawNotes']
                method_id = _ascent['methodId']
                climb_type = _ascent['type']
                total_score = _ascent['totalScore']
                date = _ascent['date']
                year = _ascent['year']
                last_year = _ascent['lastyear']
                rec_date = _ascent['recDate']
                project_ascent_date = _ascent['projectAscentDate']
                name = _ascent['name']
                crag_id = _ascent['cragId']
                crag = _ascent['crag']
                sector_id = _ascent['sectorId']
                sector = _ascent['sector']
                country = _ascent['country']
                comment = _ascent['comment']
                rating = _ascent['rating']
                description = _ascent['description']
                yellow_id = _ascent['yellowId']
                climb_try = _ascent['try']
                repeat = _ascent['repeat']
                exclude_from_ranking = _ascent['excludeFromRanking']
                user_recommended = _ascent['userRecommended']
                chipped = _ascent['chipped']

                ascent = Ascent(id=id, user_id=user_id, grade_id=grade_id, notes=notes,
                                raw_notes=raw_notes, method_id=method_id,
                                climb_type=climb_type, total_score=total_score,
                                date=date, year=year, last_year=last_year,
                                rec_date=rec_date,
                                project_ascent_date=project_ascent_date, name=name,
                                crag_id=crag_id, crag=crag, sector_id=sector_id,
                                sector=sector, country=country, comment=comment,
                                rating=rating, description=description,
                                yellow_id=yellow_id, climb_try=climb_try,
                                repeat=repeat,
                                exclude_from_ranking=exclude_from_ranking,
                                user_recommended=user_recommended, chipped=chipped)

                session.add(ascent)
                session.commit()
        except Exception as e:
            print("Ascent error")
            print(e)
    except Exception as e:
        print("No ascents at all!")
        print(e)
    session.close()


def scrape_method(climb_dict):
    """Scrape ascent method"""

    session = database_connection()

    for key in climb_dict["gui"]["methods"]:
        method_info = climb_dict["gui"]["methods"][key]

        id = method_info['id']
        score = method_info['score']
        shorthand = method_info['shorthand']
        name = method_info['name']

        method = Method(id=id, score=score, shorthand=shorthand, name=name)

        session.add(method)
        session.commit()
        session.close()


def database_connection():
    """Return a database connection"""

    engine = create_engine('sqlite:///8adata.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


if __name__ == '__main__':
    main()
