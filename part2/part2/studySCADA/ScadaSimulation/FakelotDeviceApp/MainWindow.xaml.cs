using Bogus;
using FakeIoTDeviceApp.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt;

namespace FakeIotDevice
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {
        Faker<SensorInfo> FakeHomeSensor = null;  // 가짜 스마트 홈 센서값 변수
        MqttClient client;
        Thread MqttThread { get; set; }
        public MainWindow()
        {
            InitializeComponent();

            InitFakeData();
        }

        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Bath", "Living", "Dining" };

            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H703")           // 임의로 픽스된 홈 아이디 101동 703gh 
                .RuleFor(s => s.Room_Name, f => f.PickRandom(Rooms))   // 실행할 때마다 방 이름이 계속 변경
                .RuleFor(s => s.Sensing_DateTime, f => f.Date.Past(0))        // 현재 시작이 생성
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f))      // 20~30  사이 온도 값
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f));  // 40~64% 사이의 습도값    
        }

        private void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TxtMqttBrokerIp.Text))
            {
                //await this.ShowMessageAsync("오류", "브로커 아이디를 입력하세요");
                return;
            }

            // 브로커 아이피로 접속 
            ConnectMqttBroker();
            // 무한 반복 (하위의 것들을 )
            StartPublish();
        }

        private void StartPublish()
        {
          
            MqttThread = new Thread(() => {
                while (true)
                {
                    // 가짜 스마트홈 센서값을 생성
                    SensorInfo info = FakeHomeSensor.Generate();
                    Debug.WriteLine($"{info.Home_Id}/ {info.Room_Name}/{info.Sensing_DateTime}/{info.Temp}");
                    // 센서값 MQTT브로커에 전송

                    // RtbLog에 출력 

                    Thread.Sleep(1000);
                }                 
            });
        }

        private void ConnectMqttBroker()
        {
            client = new MqttClient(TxtMqttBrokerIp.Text);
            client.Connect("SmartHomeDev");//public client ID를 지정
        }
    }
}