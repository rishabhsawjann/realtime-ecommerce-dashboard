import os
import json
import boto3
import time

ATHENA_WORKGROUP = os.environ.get('ATHENA_WORKGROUP')
ATHENA_OUTPUT_BUCKET = os.environ.get('ATHENA_OUTPUT_BUCKET')
ATHENA_DATABASE = os.environ.get('ATHENA_DATABASE', 'ecommerce_sales')
ATHENA_TABLE = os.environ.get('ATHENA_TABLE', 'sales_data')

athena = boto3.client('athena')

# Athena query templates
QUERIES = {
    'top-products': f"""
        SELECT product_id, COUNT(*) as sales_count
        FROM {ATHENA_TABLE}
        GROUP BY product_id
        ORDER BY sales_count DESC
        LIMIT 5
    """,
    'sales-by-location': f"""
        SELECT location, COUNT(*) as sales_count
        FROM {ATHENA_TABLE}
        GROUP BY location
        ORDER BY sales_count DESC
        LIMIT 10
    """,
    'revenue-trends': f"""
        SELECT substr(timestamp, 1, 10) as date, SUM(price) as total_revenue
        FROM {ATHENA_TABLE}
        GROUP BY date
        ORDER BY date DESC
        LIMIT 30
    """,
    'sales-by-category': f"""
        SELECT category, COUNT(*) as sales_count
        FROM {ATHENA_TABLE}
        GROUP BY category
        ORDER BY sales_count DESC
        LIMIT 10
    """
}

def run_athena_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': ATHENA_DATABASE
        },
        WorkGroup=ATHENA_WORKGROUP,
        ResultConfiguration={
            'OutputLocation': f's3://{ATHENA_OUTPUT_BUCKET}/athena-results/'
        }
    )
    query_execution_id = response['QueryExecutionId']
    # Wait for query to complete
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = result['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
    if state != 'SUCCEEDED':
        raise Exception(f'Athena query failed: {state}')
    # Fetch results
    result = athena.get_query_results(QueryExecutionId=query_execution_id)
    columns = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    rows = result['ResultSet']['Rows'][1:]  # skip header
    data = [dict(zip(columns, [field.get('VarCharValue', None) for field in row['Data']])) for row in rows]
    return data

def handler(event, context):
    try:
        path = event.get('resource', '') or event.get('path', '')
        if 'top-products' in path:
            query = QUERIES['top-products']
        elif 'sales-by-location' in path:
            query = QUERIES['sales-by-location']
        elif 'revenue-trends' in path:
            query = QUERIES['revenue-trends']
        elif 'sales-by-category' in path:
            query = QUERIES['sales-by-category']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unknown analytics endpoint'})
            }
        data = run_athena_query(query)
        return {
            'statusCode': 200,
            'body': json.dumps({'data': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 