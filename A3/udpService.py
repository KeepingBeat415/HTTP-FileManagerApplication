import socket, logging, socket, threading, sys

from packet import *
from const import *
from window import Window

class udpService():

    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.router_addr = None
        self.packet_builder = None

        logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)
    
    # Three-way handshaking, Auto Attempt establish connection
    def connect_server(self):

         # Set up packet builder
        self.router_addr = (ROUTER_IP, ROUTER_PORT)
        peer_ip_addr = ipaddress.ip_address(socket.gethostbyname(SERVER_IP))

        self.packet_builder = PacketBuilder(peer_ip_addr, SERVER_PORT)

        while True:

            logging.info(f"Client Attempt Connecting To Server -- {SERVER_IP}:{SERVER_PORT}")
            # Prepare SYN Packet, and send to Server
            self.send_packet(PACKET_TYPE_SYN)
            # send_syn_pkt = self.packet_builder.build(PACKET_TYPE_SYN)
            # self.conn.sendto(send_syn_pkt.to_bytes(), self.router_addr)

            logging.debug("Client send SYN, and wait for SYN-ACK response from Server.")
            # Server response msg
            recv_pkt = self.get_packet(TIME_OUT, "Client Connection")

            if recv_pkt is None:
                logging.debug("Client Fail To Connection -- Time Out.")
            
            elif recv_pkt.packet_type == PACKET_TYPE_SYN_ACK:

                # Send ACK, then establish connection
                self.send_packet(PACKET_TYPE_ACK)
                # send_ack_pkt = self.packet_builder.build(PACKET_TYPE_ACK)
                # self.conn.sendto(send_ack_pkt.to_bytes(), self.router_addr)

                logging.info("Client To Server Connection Established.")
                break
            else:
                logging.debug("Client Fail To Connection -- Expect for receive SYN packet")


    def connect_client(self):

        while True:
            # Server always waiting for Connection
            recv_pkt = self.get_packet(TIME_TO_ALIVE, "Server Connection")

            if recv_pkt is None:
                logging.info("HTTP File Manager Server Wait For Connection...")
            else:
                # Create packet builder depends on Client's addr
                self.packet_builder = PacketBuilder(recv_pkt.peer_ip_addr, recv_pkt.peer_port)

                # 3-way handshake to say Hello
                if recv_pkt.packet_type == PACKET_TYPE_SYN:

                    while True:
                        # Send SYN-ACK to Client
                        self.send_packet(PACKET_TYPE_SYN_ACK)
                        # send_pkt = self.packet_builder.build(PACKET_TYPE_SYN_ACK)
                        # self.conn.sendto(send_pkt.to_bytes(), self.router_addr)
                        # Client's response
                        recv_pkt = self.get_packet(TIME_OUT, "Server Connection")

                        # In case, response ACK msg lost
                        if recv_pkt is not None and (recv_pkt.packet_type == PACKET_TYPE_ACK or recv_pkt.packet_type == PACKET_TYPE_DATA):
                            logging.info("Server To Client Connection Established.")
                            break
                        else:
                            logging.debug("Server Fail To Connection -- Expect for receive ACK Packet.")
                    break
                # In case, some delay FIN_ACK from current Client
                elif recv_pkt.packet_type == PACKET_TYPE_FIN_ACK:
                    
                    #self.packet_builder = PacketBuilder(recv_pkt.peer_ip_addr, recv_pkt.peer_port)
                    self.send_packet(PACKET_TYPE_ACK)
                    # ack_pkt = self.packet_builder.build(PACKET_TYPE_ACK)

                    # self.conn.sendto(ack_pkt.to_bytes(), self.router_addr)
                    logging.debug("Server To Connection -- Type: FIN-ACK, Recovery with Packet Lost and sent back ACK.")
                else:
                    logging.debug("Server Fail To Connection -- Expect for receive SYN Packet.")

    
    def send_data(self, data):
        # Initial data window
        window = Window(data)

        threading.Thread(target=self.send_listener, args=(window,)).start()

        while window.has_pending_packet():

            for frame in window.get_process_frames():
                # Prepare data packet
                self.send_packet(PACKET_TYPE_DATA, frame.seq_num, frame.payload)
                # pkt = self.packet_builder.build(PACKET_TYPE_DATA, frame.seq_num, frame.payload)
                # self.conn.sendto(pkt.to_bytes(), self.router_addr)

                logging.debug(f"Send Data Packet -- Type: DATA, Num: {frame.seq_num}, payload: {frame.payload}")
                frame.send = True

        # 3-way handshake say Good-bye
        while True:
            # Send FIN msg
            self.send_packet(PACKET_TYPE_FIN)
            # send_fin_pkt = self.packet_builder.build(PACKET_TYPE_FIN)
            # self.conn.sendto(send_fin_pkt.to_bytes(), self.router_addr)

            logging.debug(f"Send Data Packet -- Type: FIN, and Wait for FIN-ACK.")
            # Received response msg
            recv_pkt = self.get_packet(TIME_TO_BEY, "Send Data")

            if recv_pkt is None:
                logging.debug("Send Data Packet -- Time Out.")
                continue
            if recv_pkt.packet_type == PACKET_TYPE_FIN_ACK:
                # Send ACK msg
                self.send_packet(PACKET_TYPE_ACK)
                # send_ack_pkt = self.packet_builder.build(PACKET_TYPE_ACK)
                # self.conn.sendto(send_ack_pkt.to_bytes(), self.router_addr)
                logging.debug("Send Data Packet -- Type: FIN-ACK, and Finished.")
                break

    # Received response for ACK msg
    def send_listener(self, window):

        while window.has_pending_packet():

            try:
                self.conn.settimeout(TIME_OUT)
                # Response msg for send packets
                data, addr = self.conn.recvfrom(PACKET_SIZE)
                pkt = Packet.from_bytes(data)

                logging.debug(f"Received ACK Packet -- Type: {self.get_packet_type(pkt.packet_type)}, Num: {pkt.seq_num}, Payload: {pkt.payload.decode('utf-8')}")
                
                # In case some delay or drop FIN_ACK packets
                if pkt.packet_type == PACKET_TYPE_FIN_ACK:
                    # Send back ACK
                    self.packet_builder = PacketBuilder(pkt.peer_ip_addr, pkt.peer_port)
                    self.send_packet(PACKET_TYPE_ACK)
                    # ack_pkt = self.packet_builder.build(PACKET_TYPE_ACK)

                    # self.conn.sendto(ack_pkt.to_bytes(), self.router_addr)
                    logging.debug("Received ACK Packet -- Type: FIN-ACK, Recovery With Packet Lost and sent back ACK.")
                # Packets ACK
                if pkt.packet_type == PACKET_TYPE_ACK:
                    window.update_ack_window(pkt.seq_num)

            except socket.timeout:
                logging.debug("Received ACK Packet -- Time Out")
                window.update_timeout_window()

    
    def received_data(self):
        # Initial window
        window = Window()

        while True:
            
            pkt = self.get_packet(TIME_OUT, "Received Data")

            if pkt is None:
                logging.debug("Received Data Packet -- Time Out")
            elif pkt.packet_type == PACKET_TYPE_DATA:
                window.process_packet(pkt)
                # send ACK
                self.packet_builder = PacketBuilder(pkt.peer_ip_addr, pkt.peer_port)
                self.send_packet(PACKET_TYPE_ACK, pkt.seq_num, "")
                # ack_pkt = self.packet_builder.build(PACKET_TYPE_ACK, pkt.seq_num, "")

                # self.conn.sendto(ack_pkt.to_bytes(), self.router_addr)

            # In case some delay or drop FIN_ACK packets
            elif pkt.packet_type == PACKET_TYPE_FIN_ACK:
                # Send FIN-ACK msg 
                self.packet_builder = PacketBuilder(pkt.peer_ip_addr, pkt.peer_port)
                self.send_packet(PACKET_TYPE_ACK)

                # ack_pkt = self.packet_builder.build(PACKET_TYPE_ACK)
                # self.conn.sendto(ack_pkt.to_bytes(), self.router_addr)
                logging.debug("Received Data Packet -- Type: FIN-ACK, Recovery with Packet Lost and sent back ACK.")
            # 3-way handshake say Good-bye
            elif pkt.packet_type == PACKET_TYPE_FIN:

                while True:
                    # Send FIN-ACK msg 
                    self.packet_builder = PacketBuilder(pkt.peer_ip_addr, pkt.peer_port)
                    self.send_packet(PACKET_TYPE_FIN_ACK)

                    # ack_pkt = self.packet_builder.build(PACKET_TYPE_FIN_ACK)
                    # self.conn.sendto(ack_pkt.to_bytes(), self.router_addr)
                    logging.debug("Received Data Packet -- Type: FIN, and sent back FIN-ACK.")
                    # Get response msg
                    recv_pkt = self.get_packet(TIME_TO_BEY, "Received Data")

                    if recv_pkt is not None and recv_pkt.packet_type == PACKET_TYPE_ACK:
                        break
                break
            # In case some delay or drop ACK, SYN, SYN-ACK msg from Connection 3-way handshake
            else:
                continue

        data = self.process_data(window)
        return data
    
    # Help method for Waiting packets
    def get_packet(self, timeout, msg=""):

        self.conn.settimeout(timeout)

        try:
            data, addr = self.conn.recvfrom(PACKET_SIZE)
            pkt = Packet.from_bytes(data)

            # logging.debug(f"Packet Received: Type - {self.get_packet_type(pkt.packet_type)}, Payload - {pkt.payload}, Address - {pkt.peer_ip_addr}:{pkt.peer_port}")
            logging.debug(f"{msg} Packet -- Type: {self.get_packet_type(pkt.packet_type)}, Num: {pkt.seq_num}, Payload: {pkt.payload}.")

            self.router_addr = addr
            return pkt
        except socket.timeout:
            return None

    #Help method for Sending 
    def send_packet(self, packet_type, seq_num=0, payload=""): #(self, packet_type, seq_num, peer_ip_addr, peer_port, payload)

        pkt = self.packet_builder.build(packet_type, seq_num, payload)
        self.conn.sendto(pkt.to_bytes(), self.router_addr)

    # def send_packet(self, packet_type, peer_ip, peer_port, seq_num=0, payload=""): #(self, packet_type, seq_num, peer_ip_addr, peer_port, payload)

    #     pkt = Packet(packet_type, seq_num, peer_ip, peer_port, payload)
    #     self.conn.sendto(pkt.to_bytes(), self.router_addr)
    
    # Convert data into String type
    def process_data(self, window):
        window.display_frames_content()
        data = b''
        for frame in window.frames:
            if frame is not None:
                data = data + frame.payload
        return data

    def get_packet_type(self, type):
        types = {0:"NONE", 1:"SYN", 2:"SYN-ACK", 3:"DATA", 4:"ACK", 5:"FIN", 6:"FIN-ACK"}
        return types.get(type)

    def close(self):
        logging.info("============ UDP Service is Closed. ============")
        self.conn.close()
