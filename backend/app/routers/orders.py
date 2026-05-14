"""
AR: مسارات الطلبات — إنشاء طلب، طلباتي، كل الطلبات (أدمن)، تحديث الحالة، حذف.
EN: Order routes — create, my orders, all orders (admin), status update, delete.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import admin_only, get_token_payload
from app.dependencies.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(tags=["Orders"])


@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_token_payload),
):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient stock for product '{product.name}'. "
                    f"Available: {product.stock}"
                ),
            )

    new_order = Order(user_id=current_user["user_id"])
    db.add(new_order)
    db.flush()

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock -= item.quantity
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/orders/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_token_payload),
):
    orders = db.query(Order).filter(Order.user_id == current_user["user_id"]).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    _admin: dict = Depends(admin_only),
):
    return db.query(Order).all()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_token_payload),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user["role"] != "admin" and order.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")

    return order


@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    _admin: dict = Depends(admin_only),
):
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from: {valid_statuses}")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)
    return order


@router.delete("/orders/{order_id}", status_code=200)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(admin_only),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
