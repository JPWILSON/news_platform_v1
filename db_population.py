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

# Add some users
user1 = User(user_name='J-P', first_name='Jean-Paul', last_name='Wilson',
             email='jeanpaulwilson@email.co', join_date=date(2018, 7, 24))

user2 = User(user_name='Mich', first_name='Michelle', last_name='Wilson',
             email='mish@email.co', join_date=date(2018, 7, 27))

user3 = User(user_name='Henk', first_name='Henk', last_name='Wilson',
             email='henki@email.co', join_date=date(2019, 7, 27))

session.add(user1)
session.add(user2)
session.add(user3)


# Add 2 channels
channel1 = Channel(channel_name='The JP Report', owner_id=user1.id, start_date=date(2018, 7, 27),
                   description='This is a channel for any news, on any thing')
channel2 = Channel(channel_name='The Michelley Report', owner_id=user2.id, start_date=date(2018, 7, 18),
                   description='This is the news Channel of Michelley welly')
session.add(channel1)
session.add(channel2)
session.commit()
#channel1 = Channel(channel_name = 'The JP Report', owner=user1, start_date=date(2018, 7, 27), description='This is a channel for any news, on any thing')
#channel1 = Channel(channel_name = 'The JP Report', owner=user1, start_date=date(2018, 7, 27), description='This is a channel for any news, on any thing')
# Then add 5 articles
article1 = Article(title='JP becomes richest main man', channel_id=channel1.id, description='Update on the rich list',
                   article_text='This is all the article text, man', date=date(2018, 6, 8))

article2 = Article(title='JP gets a job', channel_id=channel1.id, description='Finally, he\'s bringing in some cash!',
                   article_text='Wow, so JP is this guy, who has been thinking about coding for a loooong time, and he is quite good in some ways, but..',
                   date=date(2018, 6, 8))

article3 = Article(title='Mich out of night shift!', channel_id=channel2.id, description='Update on having to work at night!',
                   article_text='This is such a huge relief, we can now finally start looking forward with our life!', date=date(2018, 6, 22))

article4 = Article(title='Michelley makes Schone gifting', channel_id=channel2.id, description='Focus on new gifting startup',
                   article_text='This is all the article text, man', date=date(2018, 2, 8))
article5 = Article(title='Starting a new country', channel_id=channel1.id, description='People are worried, and they should be',
                   article_text='This is all the article text, man', date=date(2015, 6, 8))

session.add(article1)
session.add(article2)
session.add(article3)
session.add(article4)
session.add(article5)
session.commit()
