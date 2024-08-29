from django.core.management.base import BaseCommand
from shop.models import Order  # Replace with your actual model
import csv


class Command(BaseCommand):
    help = 'Generates a CSV report of all orders'

    def handle(self, *args, **options):
        # Specify the path for the CSV file
        file_path = 'orders_report.csv'

        # Open the file for writing
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header
            writer.writerow(['Order ID', 'Customer', 'Total', 'Date'])

            # Write order data
            for order in Order.objects.all():
                writer.writerow([order.id, order.buyer.first_name, order.total_price, order.ordered_at])

        self.stdout.write(self.style.SUCCESS(f'Report generated successfully and saved to {file_path}'))
