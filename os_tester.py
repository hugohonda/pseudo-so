from modules import ProcessManager, process_parser, disk_info_parser, DiskManager

def test_process_parser():
    assert process_parser('./data/processes.txt') == [
        {'boot_time': 2, 'priority': 0, 'cpu_time': 3, 'blocks': 64,
        'printer_id': 0, 'scanner_req': 0, 'modem_req': 0, 'disk_id': 0, 'pid': 0},
        {'boot_time': 8, 'priority': 0, 'cpu_time': 4, 'blocks': 64,
        'printer_id': 0, 'scanner_req': 0, 'modem_req': 0, 'disk_id': 0, 'pid': 1}
    ]