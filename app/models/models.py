from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, Integer, Table, Text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class Hashtag(Base):
    __tablename__ = 'hashtag'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(255))

    video: Mapped[List['Video']] = relationship(
        'Video', secondary='video_hastag', back_populates='hashtag')


class TblRole(Base):
    __tablename__ = 'tblRole'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    tblUser: Mapped[List['TblUser']] = relationship(
        'TblUser', back_populates='role')


class TblUser(Base):
    __tablename__ = 'tblUser'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['tblRole.id'],
                             name='tblUser_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('role_id', 'role_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    avatar: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    password: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    user_name: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    biography: Mapped[Optional[str]] = mapped_column(Text)

    role: Mapped[Optional['TblRole']] = relationship(
        'TblRole', back_populates='tblUser')
    tblFollower: Mapped[List['TblFollower']] = relationship(
        'TblFollower', foreign_keys='[TblFollower.follower_id]', back_populates='follower')
    video: Mapped[List['Video']] = relationship(
        'Video', back_populates='owner')
    view_profile: Mapped[List['ViewProfile']] = relationship(
        'ViewProfile', foreign_keys='[ViewProfile.viewer_id]', back_populates='viewer')
    comment: Mapped[List['Comment']] = relationship(
        'Comment', back_populates='user')
    react_comment: Mapped[List['ReactComment']] = relationship(
        'ReactComment', back_populates='user')


class TblFollower(Base):
    __tablename__ = 'tblFollower'
    __table_args__ = (
        ForeignKeyConstraint(['follower_id'], ['tblUser.id'],
                             name='tblFollower_ibfk_2'),
        ForeignKeyConstraint(['id'], ['tblUser.id'],
                             name='tblFollower_ibfk_1'),
        Index('follower_id', 'follower_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    follower_id: Mapped[Optional[int]] = mapped_column(Integer)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    follower: Mapped[Optional['TblUser']] = relationship(
        'TblUser', foreign_keys=[follower_id], back_populates='tblFollower')


class Video(Base):
    __tablename__ = 'video'
    __table_args__ = (
        ForeignKeyConstraint(['owner_id'], ['tblUser.id'],
                             name='video_ibfk_1'),
        Index('owner_id', 'owner_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[Optional[int]] = mapped_column(Integer)
    picture_cover: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    title: Mapped[Optional[str]] = mapped_column(Text)

    hashtag: Mapped[List['Hashtag']] = relationship(
        'Hashtag', secondary='video_hastag', back_populates='video')
    owner: Mapped[Optional['TblUser']] = relationship(
        'TblUser', back_populates='video')
    comment: Mapped[List['Comment']] = relationship(
        'Comment', back_populates='video')


class ViewProfile(Base):
    __tablename__ = 'view_profile'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tblUser.id'],
                             name='view_profile_ibfk_2'),
        ForeignKeyConstraint(['viewer_id'], ['tblUser.id'],
                             name='view_profile_ibfk_1'),
        Index('viewer_id', 'viewer_id')
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    viewer_id: Mapped[Optional[int]] = mapped_column(Integer)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    viewer: Mapped[Optional['TblUser']] = relationship(
        'TblUser', foreign_keys=[viewer_id], back_populates='view_profile')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tblUser.id'],
                             name='comment_ibfk_2'),
        ForeignKeyConstraint(['video_id'], ['video.id'],
                             name='comment_ibfk_1'),
        Index('user_id', 'user_id'),
        Index('video_id', 'video_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[Optional[int]] = mapped_column(Integer)
    parent_comment_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped[Optional['TblUser']] = relationship(
        'TblUser', back_populates='comment')
    video: Mapped[Optional['Video']] = relationship(
        'Video', back_populates='comment')
    react_comment: Mapped[List['ReactComment']] = relationship(
        'ReactComment', back_populates='comment')


t_video_hastag = Table(
    'video_hastag', Base.metadata,
    Column('video_id', Integer, primary_key=True, nullable=False),
    Column('hashtag_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['hashtag_id'], ['hashtag.id'],
                         name='video_hastag_ibfk_2'),
    ForeignKeyConstraint(['video_id'], ['video.id'],
                         name='video_hastag_ibfk_1'),
    Index('hashtag_id', 'hashtag_id')
)


class ReactComment(Base):
    __tablename__ = 'react_comment'
    __table_args__ = (
        ForeignKeyConstraint(['comment_id'], ['comment.id'],
                             name='react_comment_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tblUser.id'],
                             name='react_comment_ibfk_2'),
        Index('comment_id', 'comment_id'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    react: Mapped[Optional[int]] = mapped_column(Integer)

    comment: Mapped[Optional['Comment']] = relationship(
        'Comment', back_populates='react_comment')
    user: Mapped[Optional['TblUser']] = relationship(
        'TblUser', back_populates='react_comment')
