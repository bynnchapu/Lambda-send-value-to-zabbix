import os
from pyzabbix import ZabbixMetric, ZabbixSender

def send_metric_data(zabbix_data):
    try:
        zabbix_server_host = os.environ['ZABBIX_SERVER_HOST']
    except KeyError:
        print ('Error: Environment variable for ZABBIX_SERVER_HOST is missing.')
        result_info = {
            'failed': 1
        }
        return result_info

    print('[Sending data]')
    print(zabbix_data)

    send_data = []
    metric_data = ZabbixMetric(zabbix_data['target_host'],
                               zabbix_data['target_key'],
                               zabbix_data['target_value'])
    send_data.append(metric_data)

    zabbix_server = ZabbixSender(zabbix_server_host)
    result = zabbix_server.send(send_data)
    result_info = {
        'failed': result.failed,
        'total': result.total,
        'time': result.time,
        'chunk': result.chunk
    }
    print('[Result data]')
    print(result_info)
    return result_info


def lambda_handler(event, context):
    print('=== Input DATA ===')
    print(event)

    zabbix_data = {
        'target_host': event['requestPayload']['target']['host'],
        'target_key': event['requestPayload']['target']['key'],
        'target_value': event['responsePayload']['value']

    }
    result = send_metric_data(zabbix_data)
    status_code = 200 if result['failed'] == 0 else 500
    return_data = {
        'statusCode': status_code,
        'result': result
    }
    
    print('=== Output DATA ===')
    print(return_data)
    return return_data
