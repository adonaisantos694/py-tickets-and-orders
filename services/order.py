from typing import List, Dict, Optional
from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.fromisoformat(date)
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            ),
            order=order,
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
