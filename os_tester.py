from modules.parser import process_parser, check_valid_params

def test_process_parser():
    assert process_parser('./data/processes.txt') == [
        {'boot_time': 0, 'priority': 0, 'cpu_time': 4, 'blocks': 64,
        'printer_id': 0, 'scanner_req': 0, 'modem_req': 0, 'disk_id': 0, 'pid': 0},
        {'boot_time': 1, 'priority': 1, 'cpu_time': 4, 'blocks': 128,
        'printer_id': 0, 'scanner_req': 0, 'modem_req': 0, 'disk_id': 0, 'pid': 1}
    ]
