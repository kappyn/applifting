import uuid as uuid_pkg
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.products.examples import (
    ex_product_create,
    ex_product_patch,
    ex_product_read,
)


class IDModel(BaseModel):
    id: int = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )


class ProductBase(SQLModel):
    name: str = Field(max_length=255)
    description: str


class Product(IDModel, ProductBase, table=True):
    __tablename__ = "products"
    offers: List["Offer"] = Relationship(
        sa_relationship=relationship(
            "Offer", cascade="all, delete", back_populates="product"
        )
    )


class ProductRead(IDModel, ProductBase):
    class Config:
        schema_extra = {"example": ex_product_read}


class ProductCreate(ProductBase):
    class Config:
        schema_extra = {"example": ex_product_create}


class ProductPatch(ProductBase):
    class Config:
        schema_extra = {"example": ex_product_patch}


class OfferBase(SQLModel):
    price: int
    items_in_stock: int


class Offer(IDModel, OfferBase, table=True):
    __tablename__ = "offers"
    product_id: int = Field(foreign_key="products.id")
    product: Product = Relationship(
        sa_relationship=relationship("Product", back_populates="offers")
    )


class StatusMessage(BaseModel):
    message: str
