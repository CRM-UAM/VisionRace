using System.Collections;
using System.Collections.Generic;

using System;
using System.IO;
using System.Net;
using System.Text;
using System.Net.Sockets;

using UnityEngine;
using UnityEngine.UI;

public class ClientTCP : MonoBehaviour {

    public GUIText txt;
    public bool start = false;

    Texture2D ScreenShot = null;
    TcpClient tcpclnt;

    public int dir;
    public Text dr_txt;
    public Text yRot;
    public Slider sld;
    public InputField ip, port;

    void Start()
    {
        tcpclnt = new TcpClient();
        ScreenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
    }

    void Update()
    {
        if (tcpclnt.Connected)
            transform.Translate(new Vector3(transform.forward.x, 0, transform.forward.z) * 0.01f, Space.World);
        dr_txt.text = dir.ToString();
        yRot.text = transform.eulerAngles.y.ToString();

        transform.Rotate(Vector3.down * dir / sld.value, Space.World);

        if (Input.GetKey(KeyCode.Escape))
            Application.LoadLevel(0);
    }

    void LateUpdate()
    {

        if (ScreenShot == null || start == false)
            return;

        if (tcpclnt.Connected == false){
            try{
                tcpclnt.Connect(ip.text, Int32.Parse(port.text));
            }
            catch (Exception e){
                yRot.text = e.Message;
                Application.LoadLevel(0);
            }            
        }

        Stream stm = tcpclnt.GetStream();

        ASCIIEncoding asen = new ASCIIEncoding();
        byte[] ba = ScreenShot.EncodeToJPG();
       
        stm.Write(ba, 0, ba.Length); // Send image over TCP connection to Python Server

        byte[] bb = new byte[100];
        stm.Read(bb, 0, 100);

        txt.text = asen.GetString(bb);
        Int32.TryParse(asen.GetString(bb), out dir);
    }

    void OnPostRender() // Capture screen
    {
        ScreenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        ScreenShot.Apply();
	}

    public void StartConnection()
    {
        start = true;

        ip.gameObject.SetActive(false);
        port.gameObject.SetActive(false);
        GameObject.Find("Button").SetActive(false);
        GameObject.Find("Background").SetActive(false);
        GameObject.Find("ServerDetails").SetActive(false);
    }
}
