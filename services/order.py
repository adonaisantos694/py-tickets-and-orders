from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from datetime import datetime


@transaction.atomic
def create_order(tickets, username, date=None):
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
                id=ticket_data["movie_session"]),
            order=order
        )

    return order


def get_orders(username=None):
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
