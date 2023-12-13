import serial
from serial import SerialException
import serial.tools.list_ports
import time
import re

baudrate = 115200

pico_vid = "2E8A"  # ベンダーID

def main():
    ports = serial.tools.list_ports.comports()
    if ports:
        print("利用可能なCOMポート:")
        for port, desc, hwid in sorted(ports):
            print(f"{port}: {desc} [{hwid}]")
            if (re.search(f'VID:PID={pico_vid}', hwid)):
                print(f"find:{hwid}")
                break
    else:
        print("利用可能なCOMポートが見つかりませんでした。")
    
    try:
        ser = serial.Serial(port, baudrate)
        ser.close()
        ser.open()
        print("open >> "+ser.port)

        modulationFreq = input("変調周波数を入力 >> ")
        ser.write((str(modulationFreq)+'\n').encode())
        
        while True:
            try:
                # Arduinoからのデータを受信
                data_raw = ser.readline()
                data_received = data_raw.decode()
                # print("Arduinoからのデータ:", data_received)
                print("Arduinoからのデータ:", data_raw)
                time.sleep(0.1)  # 適宜適切な待ち時間を設定
            except KeyboardInterrupt:
                print("quit! in")
                break
    except SerialException:
        print("can't open port:"+ser.port)
    finally:
        print("closing port")
        ser.close()


if __name__ == "__main__":
    # print()
    main()
