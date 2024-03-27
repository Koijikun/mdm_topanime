from datetime import datetime

def calculate_timespan(airing_date):
    # Slit by "-" to get start & end
    date_parts = airing_date.strip().split(' - ')
    
    # Check if both start and end dates are present
    if len(date_parts) == 2:
        start_date_str, end_date_str = date_parts

        # Convert the start and end dates to datetime objects
        start_date = datetime.strptime(start_date_str.strip(), '%b %Y')
        end_date = datetime.strptime(end_date_str.strip(), '%b %Y')

        # Calculate the timespan in days
        timespan = (end_date - start_date).days

        return timespan
    else:
        # Handle cases where either start or end date is missing
        return None
    