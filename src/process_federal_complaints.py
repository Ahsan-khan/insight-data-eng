#!/usr/bin/env python3

# coding: utf-8
import csv
import sys

from operator import itemgetter

file_field_names = [
    'date_received', 'product', 'sub_product', 'issue', 'sub_issue',
    'consumer_complaint_narrative', 'company_public_resource', 'company',
    'state', 'zip_code', 'tags', 'consumer_consent_provided', 'submitted_via',
    'date_sent_to_company', 'company_response_to_customer', 'timely_response',
    'consumer_disputed', 'complaint_id'
]


def read_and_parse(file_path):
    """Given the input file with the complaints 
    open it and organize it's contents in dict with
    product as the key and the rest of the info as the values
    for the key"""
    with open(file_path, 'r', encoding="utf8") as fh:
        reader = csv.DictReader(fh, fieldnames=file_field_names)
        header = next(reader, None)

        tracker = {}
        for com in reader:
            date = com.get('date_received')
            year = date[:4].lower(
            )  # Get this using a function to parse the date
            product = com.get('product').lower()
            company = com.get('company').lower()
            info = {}
            info['year'] = year
            info['company'] = company

            if product not in tracker:
                tracker[product] = []
            tracker[product].append(info)
        return tracker


def aggregate_data(product_tracker):
    """
    Given a parsed and organized complaints file data as a dictionary
    loop through it and get 
        1. The total complaints for a given product for a given year
        2. The total unique companies receiving a complaint for a given year
    return this information as a dictionary 
    """
    tracker = {}

    for product, company_complaints in product_tracker.items():
        if product not in tracker:
            # If this product is not yet tracked start tracking it by initializing an empty dict
            tracker[product] = {}

        for single_complaint in company_complaints:  # start looping through all complaints for a given product
            year = single_complaint.get('year')
            company = single_complaint.get('company')
            if year not in tracker[product]:
                # If we have not yet tracked this year's complaints start tracking by initializing an empty dict
                tracker[product][year] = {}
                tracker[product][year][
                    'total'] = 1  # for this current loop set total complaints for this product for this year to 1 (initialized)
                tracker[product][year][
                    'companies_receiving_complaint'] = 0  # initiliaze how many times different companies have had complaints
                if company not in tracker[product][year]:
                    # If this company in this loop is not yet tracked , start tracking it
                    tracker[product][year][company] = company
                    tracker[product][year][
                        'companies_receiving_complaint'] += 1  # Continue  counting unique companies receiving a given complaint for this year
            else:
                # If we are already tracking this year then increase the total complaints for the current product for this year
                tracker[product][year]['total'] += 1
                if company not in tracker[product][year]:
                    # If this company in this loop is not yet tracked , start tracking it
                    tracker[product][year][company] = company
                    tracker[product][year][
                        'companies_receiving_complaint'] += 1  # Countinue counting unique companies receiving a given complaint for this year
    return tracker


def get_highest_percentage(product_tracker):
    """Given a parsed and organized complaints file data as a dictionary
    loop through it and get 
        1. The total number of complaint events for a given company for a given year for a product
        2. On the second loop get the maximum percentage and set max as that percentage
        """
    tracker = {}
    for product, company_complaints in product_tracker.items():
        if product not in tracker:
            # If we have not seen this product before then start tracking it with an initialized empty dict
            tracker[product] = {}
        for single_complaint in company_complaints:  # For all complaints for this product loop
            year = single_complaint.get('year')
            company = single_complaint.get('company')
            if year not in tracker[product]:
                # If we have not yet come across this year for this product initialize it with an empty dict
                tracker[product][year] = {}
                tracker[product][year][
                    company] = 1  # Since this loop also counts then set this product for this year's total to 1
            else:
                # Since we have already seen this year for this product then
                if company not in tracker[product][
                        year]:  # Check if this company has been tracked for the product and year we're in
                    tracker[product][year][
                        company] = 1  # If not then initialize counter to 1
                else:
                    # This company has already been tracked for the product and year we're in so
                    tracker[product][year][
                        company] += 1  # increment the counter for it
    # Now calculate the percentages after getting the totals for each product for each year
    percentages = {}
    for product, aggr in tracker.items():
        percentages[product] = {
        }  # Set an empty dict to hold percentage info for this product
        for year, companies in aggr.items():  # For all years and the companies
            percentages[product][year] = {
            }  # Set the tracker for the current product and year to an empty dict
            percentages[product][year][
                'max'] = 0  # Set the default percentage to 0 for the current product and year since this is the first time

            total_for_year = sum(
                companies.values())  # Get all complaints for that year

            for company, total in companies.items(
            ):  # For all company and their totals for a given year
                percentage = (
                    total / total_for_year
                ) * 100  # get the percentage of their total against totals for the whole year
                percentage = round(percentage)  # round up the percentage
                if percentage > percentages[product][year]['max']:
                    # If the current percentage for the current company for the year is greater than hte maximum already set then set it as the new maximum
                    percentages[product][year]['max'] = percentage
                percentages[product][year][
                    company] = percentage  # If it is not greater than the current max assign it to the percentage just calculated
    return percentages


def combine_aggregated_data(file_path, output):
    # Get and organize data from the file
    tracker = read_and_parse(file_path)
    # Get the totals aggregates
    totals_aggregates = aggregate_data(tracker)
    # Get the percentages
    percentages = get_highest_percentage(tracker)
    # Join them
    rows = [
    ]  # Initialize list to hold all the rows for the data set, it will be used to write to the output
    for product, complaints in totals_aggregates.items():
        # Loop through all products we have tracked
        for year, aggr in complaints.items():
            # WE have to loop through years too
            total_complaints = aggr.get(
                'total')  # Get total fo this product in this year
            total_companies_at_least_one_complaint = aggr.get(
                'companies_receiving_complaint'
            )  # Get companies that received at least one complaint for this product in this year
            highest_percentage = percentages[product][year].get(
                'max'
            )  # Get the highest percentage for this product in this year
            # Create the row to be written to the csv file
            row = {
                'product': product,
                'year': int(year),
                'total_complaints': total_complaints,
                'total_companies_at_least_one_complaint':
                total_companies_at_least_one_complaint,
                'highest_percentage': highest_percentage
            }
            # Write this row here or append them and write at the end once
            rows.append(row)
    # Write the rows to the csv file, these are the headers names for the output
    file_field_names = [
        'product', 'year', 'total_complaints',
        'total_companies_at_least_one_complaint', 'highest_percentage'
    ]
    # Sort by year first since it's not the primary need for sort then product finally
    rows.sort(key=itemgetter('year'))
    # Then sort by the product since it's the primary sort
    rows.sort(key=itemgetter('product'))

    with open(output, 'w') as fh:
        writer = csv.DictWriter(fh, fieldnames=file_field_names)
        writer.writeheader()
        writer.writerows(rows)  # Write the rows to the output file
    print("Written the output of {} rows , to {}".format(len(rows), output))


def usage():
    print("Wrong number of arguments.\n")
    print("Call script as $ {} <input_complaints_csv> <output_report_csv>".
          format(sys.argv[0]))
    sys.exit(1)


if __name__ == '__main__':
    try:
        if len(sys.argv) < 3:
            usage()
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print(
            "Using the file {} as the input. Report will be sent to {}".format(
                input_file, output_file))
        combine_aggregated_data(file_path=input_file, output=output_file)
    except Exception as e:
        print(f"Error {e}")
