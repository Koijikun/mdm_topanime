from datetime import datetime

def calculate_timespan(airing_date):
    date_parts = airing_date.strip().split(' - ')
    
    if len(date_parts) == 2:
        start_date_str, end_date_str = date_parts

        start_date = datetime.strptime(start_date_str.strip(), '%b %Y')
        end_date = datetime.strptime(end_date_str.strip(), '%b %Y')

        timespan = (end_date - start_date).days

        return timespan
    else:
        return None
    
