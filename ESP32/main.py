from umqttsimple import MQTTClient
import network
import time
import ujson
import random
import mfrc522
from machine import Pin
from machine import Timer


SSID = "hola"
PASSWORD = "hola123456789"
leer = mfrc522.MFRC522(14, 13, 12, 27, 26)
led_v=Pin(23,Pin.OUT)
led_a=Pin(21,Pin.OUT)

def readrfid():
    valor_tar= leer.getCardValue()
    if valor_tar != "":
        print(valor_tar)
        led_a.off()
        led_v.on()
        time.sleep(1)
        return(valor_tar)
    else:
        led_a.on()
        led_v.off()

def do_connect(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Hola")
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())


def run():
    do_connect(SSID, PASSWORD)
    
    SERVER = "54.224.88.194"
    client = MQTTClient("test", SERVER)

    topic = "test"

    client.connect()
    while True:
        if leer.getCardValue()!="":
            readrfid()
            led_a.off()
            led_v.on()
            variables = {
                "rfid": leer.getCardValue(),
            }
            payload = ujson.dumps(variables)
            print(payload)
            client.publish(topic, payload)
            time.sleep(1)
        else:
            led_a.on()
            led_v.off()
            continue
    client.disconnect()


if __name__ == "__main__":
    run()

