# All the utils function for the inventory app


from datetime import datetime, timedelta


def expiring_date(available_from=None, days=5):
    """Return the a future date adding `days` starting from the `available_from` date. 
       If not available_from is passed, datetime.now() is used as starting date.

       Params:
       -------
       available_from - starting date
       days - how many days should be added to the starting date.

       Return:
       expiring - the computed date

    """
    if available_from == None:
        available_from = datetime.now()
    expiring = available_from + timedelta(days=days)
    return expiring
