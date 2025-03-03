class comm_utils:
    def send_message(soc, msg):
        msg_size = str(len(msg))
        filled_size = msg_size.zfill(4)
        msg = filled_size + msg
        soc.send(msg.encode())
    
    def receive_message(soc):
        try:
            msg_len = soc.recv(4).decode()
            msg_len = int(msg_len.lstrip('0'))
            msg = soc.recv(msg_len).decode()
            return msg
        except:
            return None