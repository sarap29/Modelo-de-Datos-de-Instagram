import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

    # Relación: Un usuario puede tener muchos seguidores (followers)
    followers_id = Column(Integer, ForeignKey('followers.user_id'))
    followers = relationship('Followers')

    # Relación: Un usuario puede seguir a muchos usuarios (followers)
    following_id = Column(Integer, ForeignKey('followers.follower_id'))
    following = relationship('Followers')  

    # Relación: Un usuario puede tener muchos posts
    user_id_posts = Column(Integer, ForeignKey('users.id'))
    posts = relationship('Post') 

    # Relación: Un usuario puede tener muchos likes
    user_id_likes = Column(Integer, ForeignKey('users.id'))
    likes = relationship('Likes')  

    # Relación: Un usuario puede tener muchos medios: publicación, reels..
    user_id_media = Column(Integer, ForeignKey('users.id'))
    media = relationship('Media')  

    # Relación: Un usuario puede tener muchos comentarios
    user_id_comments = Column(Integer, ForeignKey('users.id'))
    comments = relationship('Comments')  

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    accepted = Column(Boolean)

    # Relación: Muchos seguidores pertenecen a un usuario
    follower_id = Column(Integer, ForeignKey('users.id'))
    follower = relationship('Users', foreign_keys=[follower_id])
    # Relación: Muchos seguidores están asociados a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', foreign_keys=[user_id])
    

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    photo = Column(String(50))
    description = Column(String(250))

    # Relación: Muchos posts pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)
    
    # Relación: Un post puede tener muchos comentarios
    post_id_comments = Column(Integer, ForeignKey('posts.id'))
    comments = relationship('Comments')  
    

class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)

    # Relación: Muchos likes pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)  

    # Relación: Muchos likes están asociados a un post
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Post)   
    

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)

    # Relación: Muchos medios pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)  
    

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(250))

    # Relación: Muchos comentarios pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)  

    # Relación: Muchos comentarios están asociados a un post
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Post)   


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
