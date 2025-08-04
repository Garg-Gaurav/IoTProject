# IoTProject

Indoor tracking with Industrial Ultrasonic sensor. The tracker device (mounted on moving device) is connected to PICO WH controller. 
![Project Screenshot](SensorConn.png)

On pico umqtt is installed to publish data over io.adafruit mqtt broker. And UART library is used to communicate with sensor over 500000 baud rate. For this operation PublishMQTTData.py is used. 

On system, to subscribe to location data SubscribeData.py is used. It has functions to subscribe to adafruit broker, and write the same info to SQLite database. 

The information recieved is byte string, for instance b'\xffG\x81\x00\x1a\xd5\x14\x7f`\x98\x01\x00\x00y\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02.\x00\x00\x85\x00\x0fC\xffG\x84\x00$.\x1bI\x0c\x00\x00\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd5\x14\x7f`\x98\x01\x00\x00\x85\x00\x00\xd4c\xff'

This information is parsed through the marvelmind.py file, Marvel Mind library decodes various information such as position, distance, rawIMU. Out of all this information, only position data is being saved in the database. 

```
if hedge.positionUpdated:
    write_data_sqlite(hedge.position())
    return hedge.print_position()
```

parse hedge function on marvlemind.py supports decoding the byte string:

```
    def parse_hedge_packet(self, packet):
        # This is a simplified version of what `run()` does
        self._bufferSerialDeque.extend(packet)

        # Reuse the same parsing logic from run()
        bufferList = list(self._bufferSerialDeque)
        strbuf = b''.join(bufferList)

        pktHdrOffset = strbuf.find(b'\xff\x47')
        if pktHdrOffset == -1:
            pktHdrOffset = strbuf.find(b'\xff\x4a')

        if pktHdrOffset == -1 or pktHdrOffset + 5 > len(strbuf):
            return  # Not enough data yet

        msgLen = strbuf[pktHdrOffset + 4]

        if len(strbuf) < pktHdrOffset + msgLen + 7:
            return  # Wait for more data

        self._bufferSerialDeque.clear()  # avoid double reads

        # Simulate run() logic
        self.dataEvent.set()
```

Note: the baove function or library is provided by marvelmind (sensor provider)
