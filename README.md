IoT GateWay 제작
======================

# 1. G/W HardWare 선정
## 1.1. CPi-A070WR(제조사: 컴파일 테크놀로지)
(이미지)
제품의 제조사인 컴파일 테크놀로지에서는 Raspberry Pi Zero와 같은 가격이 비교적 저렴한 MCU에 OS를 올려 임베디드 장비를 판매하고 있다. 이러한 장비들은 대부분 산업용 설비를 제어하거나 모니터링 하는 곳에 쓰이며, 그에 따른 UI를 사용자가 직접개발 하여 사용할 수 있도록 서비스를 운영하고 있다. 
 이에 B2B 사업을 진행하고 있으며 S/W 회사에서는 H/W에 대한 부담을 줄이고 개발된 S/W를 H/W에 올려 직접판매 할 수 있도록 되어 있다. 또한 H/W에 회사의 로고와 재포장하여 얼마든지 판매가 가능하다는 답변을 컴파일 테크놀로지로부터 받을 수 있었다. 단, H/W의 제조사가 컴파일 테크놀로지 라는 것을 알 수 있도록 되어 있는 스티커를 제거하지는 말라는 당부의 내용도 함께 알려주었다.

# 2. Software Architecture
## 2.1 Platform Software Architecture Design
(이미지)
Devices의 G/W 역할을 하게 된다. Web Service를 통하여 사용자는 Local 환경에서 디바이스 제어가 가능하며, AWS를 통하여 AWS IoTCore Serivce를 이용할 수 있다. AWS IoTCore Service에 대해서는 아래에 자세히 설명하도록 하겠다. 그리고 AWS IoTCore를 통하여 외부의 3rd Party Platform이 G/W를 제어 및 모니터링 할 수 있도록 지원하고 있다. System Management Service는 G/W에 동작되어야 할 Process들의 PID 값을 받아 Process 죽더라도 다시 살려주는 역할을 한다. 더 나아가 H/W Rebooting 되더라도 다시 원상 복구가 될 수 있도록 지원한다.
## 2.2 G/W Software Architecture Layer
(이미지)
SoC(System on Chip) 위에 Raspberry Pi 재단에서 제공하는 Debian Linux 기반의 Raspberry Pi 전용 OS를 설치한 후 G/W에 필요한 Software 들을 모두 설치하고 개발한 Application들을 실행시킴으로써 G/W가 정상 운영될 수 있다.
## 2.3 AWS Software Architecture Design
(이미지)
AWS IoT Core는 Device가 쉽고 안전하게 Cloud Application 및 다른 Device와 상호 작용할 수 있도록 관리해주는 관리형 Cloud Service 이다. 이미 수십억 개의 Device와 수조 건의 메시지를 지원하며, 안전하고 안정적으로 메시지를 처리하여 AWS End-Point 및 다른 디바이스로 라우팅 할 수 있는 서비스이다.
G/W Platform 에서는 위의 내용을 근거하여 AWS IoT Core를 사용하였고 비용은 5 GB 당 1.2 USD 이기 때문에 Device 하나 기준으로 약 19년 동안 사용하면 1.2 USD 이기에 현재는 거의 무료로 사용할 수 있다고 할 수 있다.
AWS IoT Core는 Device와의 통신을 IoT MQTT protocol를 사용하고 있으며 받은 데이터들 또는 전달해주어야 하는 데이터들은 MQTT Broker가 Subscript 하고 있는 대상자에게 메시지를 전달하는 역할을 한다.
Device로부터 메시지가 올라올 경우 AWS IoT Core는 Rule의해 전달된 메시지에 따라 Lambda에 전달을 하고 Lambda는 ninewatt에서 개발한 내용에 따라 데이터들을 DynamoDB에 계속 저장을 하게 되며 3rd Party Platform에서는 저장된 데이터를 활용하여 사용자에게 제공할 수 있다. 그리고 3rd Party Platform으로써 제어 명령이 내려온다면 API Gateway를 통하여 Lambda에서 MQTT broker에게 메시지를 전달한다. MQTT broker는 해당 메시지를 Subscript 하는 Device에게 전달해줌으로써 Device는 메시지를 받고 제어 명령을 수행할 수 있다. 다시 말해서 AWS IoT Core를 통하여 원격에서 Device의 모니터링과 제어를 할 수 있다.
Reference: https://gist.github.com/ihoneymon/652be052a0727ad59601