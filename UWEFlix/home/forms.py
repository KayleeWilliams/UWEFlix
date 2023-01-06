from django import forms
from .models import Ticket, Booking


class BookingForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    customer_email = forms.EmailField()

    # Create a field for each available ticket type
    def __init__(self, *args, **kwargs):
        available_tickets = kwargs.pop('available_tickets')
        super().__init__(*args, **kwargs)
        for ticket in available_tickets:
          self.fields[f'ticket_{ticket.id}'] = forms.IntegerField(
              label=ticket.name,
              initial=0,
              min_value=0,
              widget=forms.NumberInput(attrs={'data-price': ticket.price}) # Add price as an attribute for the js
          )
