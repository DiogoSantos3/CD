// Arduino UNO: envia os primeiros N termos da sequência de Fibonacci
// via Serial (USB), em modo simplex.

/*
 * Para configurar o número de termos:
 *  - altere a constante N
 *  - ou, para uma versão mais avançada, leia N do Serial ao arrancar
 */
const uint16_t N = 20;      // quantos termos enviar
const unsigned long DELAY_MS = 500;  // intervalo entre envios

void setup() {
  Serial.begin(9600);
  // opcional: esperar que o PC abra a porta
  while(!Serial) {;}
}

void loop() {
  unsigned long f0 = 0, f1 = 1;
  for (uint16_t i = 0; i < N; i++) {
    unsigned long fi = (i < 2 ? i : f0 + f1);
    // enviar em ASCII, um número por linha
    Serial.println(fi);

    // atualizar Fibonacci
    if (i >= 1) {
      f0 = f1;
      f1 = fi;
    }
    delay(DELAY_MS);
  }
  // após enviar N termos, pára aqui
  while(true) { }
}
