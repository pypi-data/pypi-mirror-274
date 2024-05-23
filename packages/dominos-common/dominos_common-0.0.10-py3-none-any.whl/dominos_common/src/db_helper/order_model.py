
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, Column, Integer, Float, ForeignKeyConstraint
from typing import List
from enum import Enum as PyEnum
from database_models.item import Item



from database import Base


class OrderStatusEnum(PyEnum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    IN_PROGRESS = 'in_progress'
    READY = 'ready'
    DELIVERY = 'delivery'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Enum(OrderStatusEnum))


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_status = mapped_column(ForeignKey('order_status.id'))
    items: Mapped[List['OrderItem']] = relationship()
    branch_id = mapped_column(ForeignKey('restaurants.id'), nullable=False)
    address_id = mapped_column(ForeignKey('addresses.id'), nullable=False)
    customer_id = mapped_column(ForeignKey('users.id'), nullable=False)
    total_price = Column(Float())


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id = mapped_column(ForeignKey('items.id'), nullable=False)
    item_details: Mapped[Item] = relationship()
    order_id = mapped_column(ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer(), nullable=False)
