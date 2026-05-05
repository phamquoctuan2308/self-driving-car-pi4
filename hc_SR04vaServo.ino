// ====== L298 ======
#define ENA 8
#define IN1 7
#define IN2 6

#define ENB 2
#define IN3 4
#define IN4 3

int speedMotor = 110;

String data = "";
int angle = 0;
int motor_cmd = 0;

// ================= SETUP =================
void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

// ================= BASIC =================
void tien() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, speedMotor);
  analogWrite(ENB, speedMotor);
}

void dung() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

// ================= RẼ TRÁI =================
void reTrai1() { // nhẹ
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 225);  // phải (nhanh)
  analogWrite(ENB, 150); 
}

void reTrai2() { // vừa
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 225);
  analogWrite(ENB, 80);
}

void reTrai3() { // gắt (quay tại chỗ)
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  // trái lùi
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, 200);
  analogWrite(ENB, 100);

}

// ================= RẼ PHẢI =================
void rePhai1() { // nhẹ
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  // trái
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150);  // phải (chậm)
  analogWrite(ENB, 225);  // trái (nhanh)
}

void rePhai2() { // vừa
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  // trái
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 80);
  analogWrite(ENB, 225);
}

void rePhai3() { // gắt
  // phải lùi
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  // trái tiến
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 100);
  analogWrite(ENB, 200);
}

// ================= LOOP =================
void loop() {

  // ===== ĐỌC SERIAL =====
  if (Serial.available()) {
    data = Serial.readStringUntil('\n');

    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      angle = data.substring(0, commaIndex).toInt();
      motor_cmd = data.substring(commaIndex + 1).toInt();
    }
  }

  // ===== STOP =====
  if (motor_cmd == 0) {
    dung();
    return;
  }

  // ===== DEAD ZONE =====
  if (abs(angle) < 5) {
    tien();
    return;
  }

  // ===== GIẢM TỐC KHI CUA GẮT =====
  if (abs(angle) > 30) speedMotor = 120;
  else speedMotor = 160;

  // ===== MAP GÓC → MỨC RẼ =====
  if (angle > 0) {
    // rẽ phải
    if (angle > 30) rePhai3();
    else if (angle > 15) rePhai2();
    else rePhai1();
  } 
  else {
    // rẽ trái
    if (angle < -30) reTrai3();
    else if (angle < -15) reTrai2();
    else reTrai1();
  }
}