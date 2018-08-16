import os
import sys
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy import Table, Text, DateTime, Time, Interval
from sqlalchemy import BLOB, Numeric, Boolean, Float
#from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

user_location = Table('user_location', Base.metadata,
                      Column('user_id', ForeignKey(
                          'user.id'), primary_key=True),
                      Column('landmark_id', ForeignKey(
                          'landmark.id'), primary_key=True),
                      Column('postal_id', ForeignKey(
                          'postal.id'), primary_key=True),
                      Column('city_id', ForeignKey('city.id')),
                      Column('region_id', ForeignKey('region.id')),
                      Column('country_id', ForeignKey('country.id')))

channel_locations = Table('channel_locations', Base.metadata,
                          Column('channel_id', ForeignKey(
                              'channel.id'), primary_key=True),
                          Column('landmark_id', ForeignKey(
                              'landmark.id'), primary_key=True),
                          Column('postal_id', ForeignKey(
                              'postal.id'), primary_key=True),
                          Column('city_id', ForeignKey('city.id')),
                          Column('region_id', ForeignKey('region.id')),
                          Column('country_id', ForeignKey('country.id')))

article_locations = Table('article_locations', Base.metadata,
                          Column('article_id', ForeignKey(
                              'article.id'), primary_key=True),
                          Column('landmark_id', ForeignKey(
                              'landmark.id'), primary_key=True),
                          Column('postal_id', ForeignKey(
                              'postal.id'), primary_key=True),
                          Column('city_id', ForeignKey('city.id')),
                          Column('region_id', ForeignKey('region.id')),
                          Column('country_id', ForeignKey('country.id')))


subscriptions = Table('subscriptions', Base.metadata,
                      Column('subscriber', ForeignKey(
                          'user.id'), primary_key=True),
                      Column('subscribed_channel', ForeignKey('channel.id'), primary_key=True))

article_topics = Table('article_topics', Base.metadata,
                       Column('topic_id', ForeignKey(
                           'topic.id'), primary_key=True),
                       Column('article_id', ForeignKey('article.id'), primary_key=True))

article_categories = Table('article_categories', Base.metadata,
                           Column('category_id', ForeignKey(
                               'category.id'), primary_key=True),
                           Column('article_id', ForeignKey('article.id'), primary_key=True))

article_media = Table('article_media', Base.metadata,
                      Column('media_id', ForeignKey(
                          'media.id'), primary_key=True),
                      Column('article_id', ForeignKey('article.id'), primary_key=True))

channel_categories = Table('channel_categories', Base.metadata,
                           Column('category_id', ForeignKey(
                               'category.id'), primary_key=True),
                           Column('channel_id', ForeignKey('channel.id'), primary_key=True))


channel_preferences = Table('channel_preferences', Base.metadata,
                            Column('preferences_id', ForeignKey(
                                'preferences.id'), primary_key=True),
                            Column('channel_id', ForeignKey('channel.id'), primary_key=True))

user_preferences = Table('user_preferences', Base.metadata,
                         Column('preferences_id', ForeignKey(
                             'preferences.id'), primary_key=True),
                         Column('user_id', ForeignKey('user.id'), primary_key=True))

# To keep track of which articles have been watched, and by who, I have the following junction/ association table:
article_views = Table('article_views', Base.metadata,
                      Column('user', ForeignKey('user.id'), primary_key=True),
                      Column('article', ForeignKey('article.id'), primary_key=True))


class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  user_name = Column(String(250), nullable=False)
  first_name = Column(String(250))
  middle_names = Column(String(250))
  last_name = Column(String(250))
  join_date = Column(Date(), nullable=False)
  is_verified = Column(Boolean, unique=False, default=False)
  email = Column(String(120), unique=True)
  phone = Column(String(16), unique=True)
  # for profile picture, use pythonhosted.org/Flask-Uploads

  comment = relationship('Comment', back_populates='user')

  # This relationship with channel is for keeping track of subscriptions
  channel = relationship('Channel',
                         secondary=subscriptions,
                         back_populates='user')
  # And this relationship is for the bi-directional part of the one (Owner(user)) to many (Channel) relationship
  # which links each channel to an owner (User). This has nothing to do with subscriptions (viewers of the channel), but rather who
  # owns the channel
  channels = relationship('Channel')

  article = relationship(
      'Article', secondary=article_views, back_populates="user")

  landmark = relationship('Landmark', secondary=user_location,
                          back_populates="user")
  postal = relationship('Postal', secondary=user_location,
                        back_populates="user")
  city = relationship('City', secondary=user_location,
                      back_populates="user")
  region = relationship('Region', secondary=user_location,
                        back_populates="user")
  country = relationship('Country', secondary=user_location,
                         back_populates="user")

  preferences = relationship('Preferences', secondary=user_preferences,
                             back_populates="user")


class Channel(Base):
  __tablename__ = 'channel'

  id = Column(Integer, primary_key=True)
  channel_name = Column(String(250), nullable=False, unique=True)
  # This relationship is between the journalist and their channel, the other is for subscribers to the channel)
  owner_id = Column(Integer, ForeignKey('user.id'))
  owner = relationship('User', back_populates='channels')
  start_date = Column(Date(), nullable=False)
  description = Column(String(1000))
  # this relationship between user and channel is for the many-to-many relation for subscribers to a channel
  # Dont think I need this: subscriber_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', secondary=subscriptions,
                      back_populates="channel")

  # Still need to figure out a way to rate channels (and users)
  rating = Column(Float())

  article = relationship('Article', back_populates='channel')

  category = relationship('Category', secondary=channel_categories,
                          back_populates="channel")

  # relationships between the location tables and the location assoc table (channel_locations)
  landmark = relationship('Landmark', secondary=channel_locations,
                          back_populates="channel")
  postal = relationship('Postal', secondary=channel_locations,
                        back_populates="channel")
  city = relationship('City', secondary=channel_locations,
                      back_populates="channel")
  region = relationship('Region', secondary=channel_locations,
                        back_populates="channel")
  country = relationship('Country', secondary=channel_locations,
                         back_populates="channel")

  preferences = relationship('Preferences', secondary=channel_preferences,
                             back_populates="channel")

  # for profile picture AND background image, use pythonhosted.org/Flask-Uploads or below:

# For Images: https://stackoverflow.com/questions/34154660/correct-way-to-declare-an-image-field-sqlalchemy
# class UserPicture(Base, Image):
#     """User picture model."""
#     __tablename__ = 'user_picture'

#     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     user = relationship(User)


class Article(Base):
  __tablename__ = 'article'

  id = Column(Integer, primary_key=True)
  channel_id = Column(Integer, ForeignKey('channel.id'))
  channel = relationship('Channel', back_populates='article')
  title = Column(String(250), nullable=False)
  description = Column(String(1000))
  date = Column(Date(), nullable=False)
  article_text = Column(String(10000))
  rating = Column(Float())
  view_count = Column(Integer)
  urgency_id = Column(Integer, ForeignKey('urgency.id'))
  urgency = relationship('Urgency', back_populates='article')
  detail_id = Column(Integer, ForeignKey('detail.id'))
  detail = relationship('Detail', back_populates='article')

  comment = relationship('Comment', back_populates='article')

  landmark = relationship('Landmark', secondary=article_locations,
                          back_populates="article")
  postal = relationship('Postal', secondary=article_locations,
                        back_populates="article")
  city = relationship('City', secondary=article_locations,
                      back_populates="article")
  region = relationship('Region', secondary=article_locations,
                        back_populates="article")
  country = relationship('Country', secondary=article_locations,
                         back_populates="article")
  topic = relationship('Topic', secondary=article_topics,
                       back_populates="article")
  category = relationship('Category', secondary=article_categories,
                          back_populates="article")
  media = relationship('Media', secondary=article_media,
                       back_populates="article")
  user = relationship('User', secondary=article_views,
                      back_populates="article")


# Now the location tables need to be built:
class Landmark(Base):
  __tablename__ = 'landmark'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))
  # Each location category will have 3 relationships with the 3 association tables (user, channel, article):
  #user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', secondary=user_location,
                      back_populates="landmark")

  #article_id = Column(Integer, ForeignKey('article.id'))
  article = relationship('Article', secondary=article_locations,
                         back_populates="landmark")

  #channel_id = Column(Integer, ForeignKey('channel.id'))
  channel = relationship('Channel', secondary=channel_locations,
                         back_populates="landmark")


class Postal(Base):
  __tablename__ = 'postal'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  #user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', secondary=user_location,
                      back_populates="postal")

  #article_id = Column(Integer, ForeignKey('article.id'))
  article = relationship('Article', secondary=article_locations,
                         back_populates="postal")

  #channel_id = Column(Integer, ForeignKey('channel.id'))
  channel = relationship('Channel', secondary=channel_locations,
                         back_populates="postal")


class City(Base):
  __tablename__ = 'city'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  #user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', secondary=user_location,
                      back_populates="city")

  #article_id = Column(Integer, ForeignKey('article.id'))
  article = relationship('Article', secondary=article_locations,
                         back_populates="city")

  #channel_id = Column(Integer, ForeignKey('channel.id'))
  channel = relationship('Channel', secondary=channel_locations,
                         back_populates="city")


class Region(Base):
  __tablename__ = 'region'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  #user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', secondary=user_location,
                      back_populates="region")

  #article_id = Column(Integer, ForeignKey('article.id'))
  article = relationship('Article', secondary=article_locations,
                         back_populates="region")

  #channel_id = Column(Integer, ForeignKey('channel.id'))
  channel = relationship('Channel', secondary=channel_locations,
                         back_populates="region")


class Country(Base):
  __tablename__ = 'country'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  #user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', secondary=user_location,
                      back_populates="country")

  #article_id = Column(Integer, ForeignKey('article.id'))
  article = relationship('Article', secondary=article_locations,
                         back_populates="country")

  #channel_id = Column(Integer, ForeignKey('channel.id'))
  channel = relationship('Channel', secondary=channel_locations,
                         back_populates="country")


# Need to create the different news categories!
# 1-many - urgency and detail (Each article can only have one urgency level and one detail level)
# but an article can have many topics, categories and media types!
class Urgency(Base):
  __tablename__ = 'urgency'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  article = relationship('Article', back_populates='urgency')


class Detail(Base):
  __tablename__ = 'detail'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  article = relationship('Article', back_populates='detail')

# The following three classes describe tables where there is an association table required between these 3
# and the Article class that they are related to


class Topic(Base):
  __tablename__ = 'topic'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  article = relationship('Article', secondary=article_topics,
                         back_populates="topic")


class Category(Base):
  __tablename__ = 'category'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  article = relationship('Article', secondary=article_categories,
                         back_populates="category")

  channel = relationship('Channel', secondary=channel_categories,
                         back_populates="category")


class Media(Base):
  __tablename__ = 'media'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  article = relationship('Article', secondary=article_media,
                         back_populates="media")


class Preferences(Base):
  __tablename__ = 'preferences'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(500))

  user = relationship('User', secondary=user_preferences,
                      back_populates="preferences")

  channel = relationship('Channel', secondary=channel_preferences,
                         back_populates="preferences")


class Comment(Base):
  __tablename__ = 'comment'

  id = Column(Integer, primary_key=True)
  comment_content = Column(String(5000), nullable=False)
  comment_time = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
  #time_created = Column(DateTime(timezone=True), server_default=func.now())
  comment_rating = Column(Float())

  commenter_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('User', back_populates='comment')

  article_id = Column(Integer, ForeignKey('article.id'))
  article = relationship('Article', back_populates='comment')
  # This is wrong, I think. the line above is correct....  article = relationship('Article', back_populates='article')
  # Self referencing (for the situation where one replies to a comment)
  comment_reply_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
  # This is the implementation of a self-referential relationship...
  comment_replying_to = relationship(
      "Comment", remote_side=[id])  # , back_populates="target_comment"


engine = create_engine('sqlite:///newsplatform_sqlite.db')
#engine = create_engine('postgresql+psycopg2://newsplatform_one:jp_np@localhost/newsplatform')


Base.metadata.create_all(engine)


# Notes on this code:
# for images: https://stackoverflow.com/questions/34154660/correct-way-to-declare-an-image-field-sqlalchemy
# For DateTime, see this thread: https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
