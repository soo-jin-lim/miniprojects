﻿using MahApps.Metro.Controls;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// RealTimeControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RealTimeControl : UserControl
    {
        public RealTimeControl()
        {
            InitializeComponent();

            LvcLivingTemp.Value = LvcDiningTemp.Value = LvcBedTemp.Value = LvcBedTemp.Value = 0;
            LvcLivingHumid.Value = LvcDiningHumid.Value = LvcBedHumid.Value = LvcBathHumid.Value = 0;
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            { // DB 모니터링을 실행한 뒤 실시간 모니터링으로 넘어왔다면
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;

            }
            else
            { // DB 모니터링은 실행하지 않고 바로 실시간 모니터링 메뉴를 클릭했으면
                Commons.MQTT_CLIENT = new MqttClient(Commons.BROKERHOST);
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                    new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE });
            }
        }
        //MQTTclient는 단독 스레드 사용 ,UI 스레드에 접근이 안됨
        // this.Invoke(); 스레드에 접근 가능
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            Debug.WriteLine(msg);
            var currSensor = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);

            if (currSensor["Home_Id"] == "D101H703") // D101H703은 사용자 DB에서 동적으로 가져와야할 값
            {
                switch (currSensor["Room_Name"].ToUpper())
                {
                    case "LIVING":
                        this.Invoke(() => // UI와 충돌 나지 않도록
                        {
                            LvcLivingTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcLivingHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "DINING":
                        this.Invoke(() =>
                        {
                            LvcDiningTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcDiningHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "BED":
                        this.Invoke(() =>
                        {
                            LvcBedTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcBedHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "BATH":
                        this.Invoke(() =>
                        {
                            LvcBathTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcBathHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    default:
                        break;
                }
            }
        }
    }
}