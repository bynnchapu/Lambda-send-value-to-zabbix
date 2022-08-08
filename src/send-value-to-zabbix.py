import json
from pyzabbix import ZabbixMetric, ZabbixSender

def send_metric_data(zabbix_data):
    print('[Sending data]')
    print(json.dumps(zabbix_data))

    send_data = []
    metric_data = ZabbixMetric(zabbix_data['target_host'],
                               zabbix_data['target_key'],
                               zabbix_data['target_value'])
    send_data.append(metric_data)

    zabbix_server = ZabbixSender(zabbix_data['zabbix_server_host'])
    result = zabbix_server.send(send_data)
    result_info = {
        'failed': result.failed,
        'total': result.total,
        'time': float(result.time),
        'chunk': result.chunk
    }
    print('[Result data]')
    print(json.dumps(result_info))
    return result_info


def lambda_handler(event, context):
    zabbix_data = {
        'zabbix_server_host': event['zabbix_server_host'],
        'target_host': event['target_host'],
        'target_key': event['target_key'],
        'target_value': event['target_value']

    }
    result = send_metric_data(zabbix_data)

    status_code = 200 if result['failed'] == 0 else 500

    return {
        'statusCode': status_code,
        'result': json.dumps(result)
    }
