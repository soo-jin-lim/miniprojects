using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
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
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        public bool IsConnected { get; set; }

        public DataBaseControl()
        {
            InitializeComponent();
        }
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false;//아직 접속이 안되어있음
            BtnConnDb.IsChecked = false;
        }
        //토글버튼 클릭 이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            if (IsConnected == false)
            {
                BtnConnDb.IsChecked = true;
                IsConnected = true;

                //MQTT 브로커에 접속
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    //Mqtt subscribe(구독할) 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        //Mqtt 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR");
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE }); // QOS는 네트워크 통신에 옵션
                        UpdateLog(">>> MQTT Broker Connected");

                        BtnConnDb.IsChecked = true;
                        IsConnected = true; // 예외가 발생하면 true 변경할 필요없습


                    }
                }
                catch 
                { 
                    //pass
                }

            }
            else
            {
                BtnConnDb.IsChecked = false;
                IsConnected = false;

            }
        }
        private void UpdateLog(string msg)
        {
            this.Invoke(() => {
                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();

            });

        }
        //Subscribe가 발생할 때 이벤트 핸들러
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, uPLibrary.Networking.M2Mqtt.Messages.MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetTodataBase(msg, e.Topic);

        }

        private void SetTodataBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null)
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);
                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = "INSERT INTO smarthomesensor ...";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["Home_Id"]);
                        if(cmd.ExecuteNonQuery()==1)
                        {
                            UpdateLog(">>> DB Insert succeed");
                        }
                        else
                        {
                            UpdateLog(">>> DB Insert failed");
                        }
                    }
                    


            }
        }
    }
}
