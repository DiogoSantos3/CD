import serial
import time

# parâmetros
PORT = 'COM4'          # substitua pela sua porta (e.g. '/dev/ttyACM0' no Linux)
BAUD  = 9600
N     = 20             # deve corresponder ao N do sketch
OUTPUT = 'fib_received.txt'

def main():
    # abre a porta serial
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # dá tempo ao Arduino para resetar

    with open(OUTPUT, 'w') as f_out:
        for _ in range(N):
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line:
                print(line)
                f_out.write(line + '\n')
            else:
                print("Timeout ou linha vazia!")
    ser.close()
    print(f"Guardado em {OUTPUT}")

if __name__ == "__main__":
    main()
