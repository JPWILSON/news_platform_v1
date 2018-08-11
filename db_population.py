from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import user_location, channel_locations, article_locations, subscriptions, article_topics, article_categories, article_media, channel_categories, channel_preferences, user_preferences, article_views
from database_setup import Base, User, Channel, Article, Landmark, Postal, City, Region, Country, Urgency, Detail, Topic, Category, Media, Preferences, Comment
from datetime import datetime, date
engine = create_engine('sqlite:///newsplatform_sqlite.db')


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# temporarily using sqlite, but I will need to swap this over to psql soon,
# which will have data input formatting differences, for example:
# below is going to be for psql
# user1 = User(user_name='J-P', first_name='Jean-Paul',
#              last_name='Wilson', email='jeanpaulwilson@email.co', join_date='2018-7-24')
user1 = User(user_name='J-P', first_name='Jean-Paul', last_name='Wilson',
             email='jeanpaulwilson@email.co', join_date=date(2018, 7, 24))

user2 = User(user_name='Mich', first_name='Michelle', last_name='Wilson',
             email='mish@email.co', join_date=date(2018, 7, 27))

user3 = User(user_name='Henk', first_name='Henk', last_name='Wilson',
             email='henki@email.co', join_date=date(2019, 7, 27))


session.add(user1)
session.add(user2)
session.add(user3)
session.commit()
