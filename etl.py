import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    
    """ queries that loads data from S3 buckets
to Redshift"""

    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    
    """ INSERT statements from staging tables to 
the dimension and fact tables"""

    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Extract songs metadata and user activity data from S3, transform it using a staging table, and load it into dimensional tables for analysis
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
#    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()