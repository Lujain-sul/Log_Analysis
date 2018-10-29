#!/usr/bin/env python3

# Import nedded modules
import decimal
import datetime
import psycopg2

# Connect to news database
db = psycopg2.connect("dbname=news")


# Below function is used to execute a given query
# and return the returned data
def generate_results(query):
    cursor = db.cursor()  # Create a database cursor
    cursor.execute(query)  # Execute the query
    rows = cursor.fetchall()  # Fetch all rows
    return rows


# Below function is used to write a given list of tuples
# which represents the returned data into a text file
def log_results(header, results):
    file = open("log_analysis.txt", "a")  # Create file if not exists or append
    file.write("\n\n %s \n" % header)  # Write the header of the query
    for result in results:  # Iterate through the list of tuples (rows)
        for column in result:  # Iterate through each tuple's item (columns)
            # Check the type of the tuple item,
            # append the item value and a phrase accordingly
            if type(column) is int:
                file.write(" - %d views" % column)
            elif type(column) is decimal.Decimal:
                file.write(" - %.2f%%" % column)
            elif type(column) is datetime.date:
                file.write(column.strftime(" - %B %d, %Y"))
            else:
                file.write(" - %s" % column)
        file.write("\n")  # Add a blank line between queries
    file.close()  # Close the file


# pop_art_query is a string representation of the first query
pop_art_query = """SELECT articles.title,
                          COUNT(*) AS views_count
                   FROM log,
                        articles
                   WHERE SUBSTRING(log.path,
                                   POSITION('/article/' IN log.path)+9)
                                   = articles.slug
                   GROUP BY articles.title
                   ORDER BY views_count desc
                   LIMIT 3;"""
# Call generate_results to execute the given query,
# then call log_results for logging results into the file
pop_art = generate_results(pop_art_query)
log_results("What are the most popular three articles of all time?", pop_art)


# pop_auth_query is a string representation of the second query
pop_auth_query = """SELECT authors.name,
                           SUM(a.views_count::INTEGER) AS views_sum
                    FROM (SELECT COUNT(*) AS views_count,
                                 articles.slug AS title,
                                 articles.author AS author
                          FROM log,
                               articles
                          WHERE SUBSTRING(log.path,
                                          POSITION('/article/' IN log.path)+9)
                                          = articles.slug
                          GROUP BY articles.slug,
                                   articles.author) a,
                                                    authors
                    WHERE authors.id = a.author
                    GROUP BY authors.id
                    ORDER BY views_sum DESC;"""
# Call generate_results to execute the given query,
# then call log_results for logging results into the file
pop_auth = generate_results(pop_auth_query)
log_results("Who are the most popular article authors of all time?", pop_auth)


# error_rate_query is a string representation of the third query
error_rate_query = """SELECT a.date_time,
                            (a.error_count * 100)::NUMERIC
                                                 / COUNT(*) AS error_rate
                      FROM (SELECT time::DATE AS date_time,
                                   COUNT(*) AS error_count
                            FROM log
                            WHERE status <> '200 OK'
                            GROUP BY time::DATE) a,
                                                 log
                      WHERE log.time::DATE = a.date_time
                      GROUP BY a.date_time, a.error_count
                      HAVING (a.error_count * 100)::NUMERIC / COUNT(*) > 1;"""
# Call generate_results to execute the given query,
# then call log_results for logging results into the file
error_rate = generate_results(error_rate_query)
log_results("When did more than 1% of requests lead to errors?",
            error_rate)

db.close()  # Close the database connection
