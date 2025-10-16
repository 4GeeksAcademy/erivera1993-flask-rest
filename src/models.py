from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationships
    posts: Mapped[list[Post]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list[Comments]] = relationship(
        "Comments", back_populates="user", cascade="all, delete-orphan"
    )
    followers: Mapped[list[Follower]] = relationship(
        "Follower",
        foreign_keys="Follower.following_id",
        back_populates="following_user",
        cascade="all, delete-orphan",
    )
    following: Mapped[list[Follower]] = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower_user",
        cascade="all, delete-orphan",
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    repost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))  # FK → User

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="posts")
    comments: Mapped[list[Comments]] = relationship(
        "Comments", back_populates="post", cascade="all, delete-orphan"
    )
    pictures: Mapped[list[Picture]] = relationship(
        "Picture", back_populates="post", cascade="all, delete-orphan"
    )


class Picture(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    caption: Mapped[str] = mapped_column(String(250))
    date_posted: Mapped[str] = mapped_column(String(50))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))  # FK → Post

    # Relationships
    post: Mapped[Post] = relationship("Post", back_populates="pictures")


class Comments(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))  # FK → User
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))  # FK → Post

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="comments")
    post: Mapped[Post] = relationship("Post", back_populates="comments")


class Follower(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Self-referential relationships to User
    follower_user: Mapped[User] = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    following_user: Mapped[User] = relationship(
        "User", foreign_keys=[following_id], back_populates="followers"
    )
