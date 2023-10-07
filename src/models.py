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

    # Relaciones
    followers = relationship('Followers', foreign_keys='Followers.user_id')  
    # Relación uno a muchos (un usuario puede tener muchos seguidores)
    following = relationship('Followers', foreign_keys='Followers.follower_id')  
    # Relación uno a muchos (un usuario puede seguir a muchos usuarios-followers)
    posts = relationship('Post')  
    # Relación uno a muchos (un usuario puede tener muchos posts)
    likes = relationship('Likes')  
    # Relación uno a muchos (un usuario puede dar muchos likes)
    media = relationship('Media')  
    # Relación uno a muchos (un usuario puede tener muchos medios asociados)
    comments = relationship('Comments')  
    # Relación uno a muchos (un usuario puede tener muchos comentarios)

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey(Users.id))
    user_id = Column(Integer, ForeignKey(Users.id))
    accepted = Column(Boolean)

    # Relaciones con otras tablas
    follower = relationship(Users, foreign_keys='Followers.follower_id')  
    # Relación muchos a uno (muchos seguidores pertenecen a un usuario)
    user = relationship(Users, foreign_keys='Followers.user_id')  
    # Relación muchos a uno (muchos seguidores están asociados a un usuario)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    photo = Column(String(50))
    description = Column(String(250))

    # Relaciones con otras tablas
    user = relationship(Users)  
    # Relación muchos a uno (muchos posts pertenecen a un usuario)
    comments = relationship('Comments')  
    # Relación uno a muchos (un post puede tener muchos comentarios)

class Likes(Base):
    # Definición de la tabla 'likes'
    __tablename__ = 'likes'
    # Columnas de la tabla
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    post_id = Column(Integer, ForeignKey(Post.id))

    # Relaciones con otras tablas
    user = relationship(Users, foreign_keys='Likes.user_id')  
    # Relación muchos a uno (muchos likes pertenecen a un usuario)
    post = relationship(Post)  
    # Relación muchos a uno (muchos likes están asociados a un post)

class Media(Base):
    # Definición de la tabla 'media'
    __tablename__ = 'media'
    # Columnas de la tabla
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(Users.id))

    # Relaciones con otras tablas
    user = relationship(Users)  
    # Relación muchos a uno (muchos medios pertenecen a un usuario)

class Comments(Base):
    # Definición de la tabla 'comments'
    __tablename__ = 'comments'
    # Columnas de la tabla
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    post_id = Column(Integer, ForeignKey(Post.id))
    text = Column(String(250))

    # Relaciones con otras tablas
    user = relationship(Users)  
    # Relación muchos a uno (muchos comentarios pertenecen a un usuario)
    post = relationship(Post)  
    # Relación muchos a uno (muchos comentarios están asociados a un post)

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
