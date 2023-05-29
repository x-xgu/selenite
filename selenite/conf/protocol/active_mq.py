import stomp


class MQConfig:
    activemq_ip: str = ''
    activemq_port: int = None
    activemq_username: str = ''
    activemq_password: str = ''

    def send_active_mq_msg(self, mq_topic, mq_msg):
        conn = stomp.Connection10(
            [(self.activemq_ip, self.activemq_port)],
            auto_content_length=False
        )
        conn.connect(
            username=self.activemq_username,
            passcode=self.activemq_password,
            wait=True,
            headers={'activemq.prefetchSize': '1'}
        )
        conn.send(mq_topic, mq_msg)
        conn.disconnect()
