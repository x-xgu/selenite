import stomp


class MQConfig:
    activemq_ip: str = ''
    activemq_port: int = None

    def send_active_mq_msg(self, mq_topic, mq_msg):
        conn = stomp.Connection10(
            [(self.activemq_ip, self.activemq_port)],
            auto_content_length=False
        )
        conn.connect()
        conn.send(mq_topic, mq_msg)
        conn.disconnect()
