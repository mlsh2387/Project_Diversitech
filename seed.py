"""Utility file to seed diversity database."""

from sqlalchemy import func
from model import Company
from model import Category
from model import Review
from model import Logo
import random
import os
import requests

from model import connect_to_db, db

from application import app
import pandas as pd
import numpy as np



def load_companies():
    """Load companies into Companies table."""
    data = pd.read_csv("Diversitech-Table.csv")

    print "Companies"

    Company.query.delete()

    for index, row in data.iterrows():
        name = row[0]
        if type(name) == str:
            name_lower = name.lower()
        # number_of_employees = row[28]
        report_date = row[2]
        female_overall = row[3]
        male_overall = row[4]

        company = Company(name=name_lower,
                          # number_of_employees=number_of_employees,
                          report_date=report_date,
                          female_overall=female_overall,
                          male_overall=male_overall)

        db.session.add(company)

    db.session.commit()


def load_company_logos():

    companies = Company.query.all()

    for company in companies:
        company_name = company.name
        company_id = company.company_id

        if company_name == "u.s. population" or company_name == "average from our sample":
            continue

        else:

            url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=55828&t.k=fhcJ0ZT1E89&action=employers&q=" + str(company_name)

            resp = requests.get(url, headers={'User-Agent': 'curl/7.30.0'})
            results = resp.json()

            if company_name == "hp":
                square_logo = "http://fixstream.com/wp-content/uploads/2015/08/hp-logo-square.jpg"

            elif company_name == "instagram":
                square_logo = "http://cdn.wccftech.com/wp-content/uploads/2015/08/Instagram-logo.png"

            elif company_name == "codespark":
                square_logo = "http://i.imgur.com/yFr2Xn4.png"

            else:
                square_logo = results["response"]["employers"][0]["squareLogo"]

            logo = Logo(company_id=company_id,
                        logo=square_logo)

            db.session.add(logo)

    db.session.commit()



def load_categories():
    """Load categories into categories table."""
    data = pd.read_csv("Diversitech-Table.csv")
    print "Categories"

    categories = data.columns.values

    for index, row in data.iterrows():
        for i in range(len(row[5:21])):

            if row[i + 5] == "-":
                continue

            else:

                category = categories[i + 5]
                percentage = row[i + 5]
                name = row[0]
                name_lower = name.lower()
                company = Company.query.filter(Company.name == name_lower).first()
                id_of_company = company.company_id
                detail = Category(category=category,
                                  percentage=percentage,
                                  company_id=id_of_company)

                db.session.add(detail)

    db.session.commit()



# def load_reviews():
#     """Load dummy data into reviews table."""
#
#     reviews_list = ["""Bandwidth low hanging fruit mass market iPad bootstrapping facebook ramen equity termsheet long tail first mover advantage marketing.
#     Virality MVP business-to-consumer seed money. Creative backing release metrics user experience market. Angel investor ownership traction long tail
#     pivot iteration validation business model canvas. Mass market facebook incubator.""", """Client customer gamification long tail marketing. Ecosystem
#     innovator business-to-consumer seed money paradigm shift series A financing technology launch party funding customer marketing stock client return on investment.
#     Client partner network series A financing low hanging fruit. First mover advantage ownership iteration stock equity gamification holy grail pitch incubator
#     monetization lean startup angel investor. Launch party bootstrapping marketing hackathon growth hacking iPhone.""", """Low hanging fruit lean startup influencer
#     buzz burn rate termsheet. Crowdfunding social media business-to-business startup. First mover advantage stock direct mailing prototype. Facebook customer gen-z
#     validation monetization incubator. Crowdsource A/B testing partner network low hanging fruit assets crowdfunding marketing sales branding non-disclosure
#     agreement.""", """Crowdfunding gamification stealth product management venture success entrepreneur. Rockstar innovator direct mailing assets startup success investor.
#     Creative iPhone buzz bandwidth deployment ownership infographic ecosystem equity non-disclosure agreement validation customer learning curve. Partnership
#     learning curve beta traction iteration advisor churn rate low hanging fruit market return on investment crowdsource backing niche market. Direct mailing
#     buzz venture.""", """Business plan monetization long tail backing startup holy grail early adopters incubator hypotheses influencer ownership launch party
#     handshake.""", """Influencer entrepreneur channels iPhone growth hacking hypotheses twitter marketing business model canvas mass market pivot traction vesting
#     period. Validation business-to-business twitter handshake branding advisor influencer startup. Virality business model canvas technology vesting period
#     accelerator backing branding ecosystem monetization creative termsheet buzz user experience. Hackathon virality business-to-consumer series A financing
#     creative metrics channels success investor.""", """""", """Branding low hanging fruit hackathon. User experience business model canvas responsive web
#     design branding stealth facebook research & development business plan infographic founders disruptive.""", """Responsive web design iPad buzz graphical
#     user interface validation branding seed money rockstar traction. Advisor niche market hackathon startup sales gen-z burn rate infographic technology graphical
#     user interface facebook funding buyer. Disruptive low hanging fruit prototype launch party business model canvas lean startup sales creative termsheet seed
#     money investor customer.""", """Conversion handshake android advisor business-to-consumer funding crowdsource ramen startup stealth innovator stock network
#     effects.""", """eed round channels non-disclosure agreement customer hypotheses. Leverage learning curve graphical user interface analytics hypotheses twitter
#     funding seed round termsheet low hanging fruit. Long tail hypotheses influencer stock agile development. Business model canvas long tail beta gamification
#     facebook. Supply chain growth hacking startup iPad. Venture low hanging fruit market channels crowdsource creative incubator alpha. Alpha equity niche
#     market incubator freemium seed round paradigm shift founders facebook stealth scrum project business-to-business graphical user interface. Ownership pitch
#     A/B testing user experience venture assets launch party startup. Partner network infrastructure responsive web design release.""", """""", """First mover
#     advantage vesting period iPhone validation infrastructure paradigm shift advisor launch party ownership customer.""", """Churn rate iteration backing.
#     User experience pitch business plan angel investor advisor incubator alpha infographic seed round assets iPad supply chain investor non-disclosure agreement.
#     Termsheet burn rate accelerator business-to-business network effects social media backing traction entrepreneur non-disclosure agreement return on investment
#     business plan partnership.""", """Influencer innovator infographic branding non-disclosure agreement pivot bandwidth scrum project. Business plan venture
#     social media non-disclosure agreement advisor backing ramen early adopters.""", """Android non-disclosure agreement business model canvas crowdfunding
#     freemium gamification hackathon virality funding launch party. Influencer release twitter long tail lean startup paradigm shift iPhone infrastructure.
#     Launch party equity low hanging fruit holy grail. Learning curve startup branding technology hackathon social proof release business model canvas.""", """"""]
#
#
#     titles_list = ["""Great Company!""", """Diversity has become a priority""", """I love the culture here!""", """Management does not seem to care about
#     diversity!""", """Working here is the best decision I ever made!"""]
#
#     for i in range(2, 32):
#         for x in range(5):
#
#             company_id = i
#
#             rating = random.randint(1, 5)
#
#             gender = random.choice(['Male', 'Female'])
#
#             ethnicity = random.choice(['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other'])
#
#             employee_status = random.choice(['Current Employee', 'Former Employee'])
#
#             review_title = random.choice(titles_list)
#
#             pros = random.choice(reviews_list)
#
#             cons = random.choice(reviews_list)
#
#             recommended = random.choice(['Yes', 'No'])
#
#             review = Review(company_id=company_id,
#                                           rating=rating,
#                                           gender=gender,
#                                           ethnicity=ethnicity,
#                                           employee_status=employee_status,
#                                           review_title=review_title,
#                                           pros=pros,
#                                           cons=cons,
#                                           recommended=recommended
#                                           )
#
#             db.session.add(review)
#
#     db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    connect_to_db(app, os.environ.get("DATABASE_URL"))
    db.create_all(app=app)
    print "Connected to DB."

    # Import different types of data
    load_companies()
    load_categories()
    load_company_logos()
    # load_reviews()
