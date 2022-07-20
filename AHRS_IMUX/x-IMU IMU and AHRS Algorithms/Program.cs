using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;
using System.Threading;
using System.Windows.Forms;
using System.ComponentModel;
using System.IO.Ports;

namespace x_IMU_IMU_and_AHRS_Algorithms
{
    class Program
    {
        /// <summary>
        /// Algorithm object.
        /// </summary>
        static AHRS.MadgwickAHRS AHRS = new AHRS.MadgwickAHRS(1f / (512f*10f), 2f);
        //static AHRS.MahonyAHRS AHRS = new AHRS.MahonyAHRS(1f / 256f, 5f);

        /// <summary>
        /// Main method.
        /// </summary>
        /// <param name="args">
        /// Unused.
        /// </param>
        /// 
        static float[] quat_BNO = new float[4] { 1.0f, 0.0f, 0.0f, 0.0f };
        static float[] quat_MPU = new float[4] { 1.0f, 0.0f, 0.0f, 0.0f };
        static float[] omega = new float[4] { 0.0f, 0.0f, 0.0f, 0.0f };
        static float[] acc  = new float[4] { 0.0f, 0.0f, 0.0f, 0.0f };
        static Form_3Dcuboid bno_cube, mpu_cube;
        static x_IMU_API.QuaternionData Q_bno = new x_IMU_API.QuaternionData(quat_BNO);
        static x_IMU_API.QuaternionData Q_mpu = new x_IMU_API.QuaternionData(quat_MPU);

        static void Main(string[] args)
        {
            Console.WriteLine(Assembly.GetExecutingAssembly().GetName().Name + " " + Assembly.GetExecutingAssembly().GetName().Version.Major.ToString() + "." + Assembly.GetExecutingAssembly().GetName().Version.Minor.ToString());
            try
            {
                Console.WriteLine("Showing 3D Cuboid forms...");
                Form_3Dcuboid form_3DcuboidA = new Form_3Dcuboid(Form_3Dcuboid.CameraViews.Front);
                form_3DcuboidA.Text += " BNO055";
                Form_3Dcuboid form_3DcuboidB = new Form_3Dcuboid();
                form_3DcuboidB.Text += " MPU9250";
                BackgroundWorker backgroundWorkerA = new BackgroundWorker();
                BackgroundWorker backgroundWorkerB = new BackgroundWorker();
                backgroundWorkerA.DoWork += new DoWorkEventHandler(delegate { form_3DcuboidA.ShowDialog();});
                backgroundWorkerA.RunWorkerAsync();
                backgroundWorkerB.DoWork += new DoWorkEventHandler(delegate { form_3DcuboidB.ShowDialog(); });
                backgroundWorkerB.RunWorkerAsync();
                bno_cube = form_3DcuboidA;
                mpu_cube = form_3DcuboidB;
                SerialPort serialPort = new SerialPort("COM4", 115200);
                serialPort.DataReceived += SerialPort_DataReceived;
                serialPort.Open();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }

            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }

        private static void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            SerialPort port = sender as SerialPort;

            if (port.BytesToRead < 64)
                return;

            byte[] bytes = { 0, 0, 0, 0 };

            for (int i = 0; i<4; i++)
            {
                for(int j = 0; j<4; j++)
                {
                    bytes[j] = (byte)port.ReadByte();
                }

                Q_bno.Quaternion[i] = (float)Math.Round(BitConverter.ToSingle(bytes,0),4);
            }

            for (int i = 0; i < bytes.Length; i++)
            {
                bytes[i] = 0;
            }

            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 4; j++)
                {
                    bytes[j] = (byte)port.ReadByte();
                }

                Q_mpu.Quaternion[i] = (float)Math.Round(BitConverter.ToSingle(bytes, 0), 4);

            }

            Console.WriteLine("BNO055: " + Q_bno.Quaternion[0].ToString() + "   " + Q_bno.Quaternion[1].ToString() + "   " + Q_bno.Quaternion[2].ToString() + "   " + Q_bno.Quaternion[3].ToString() + '\n');

            Console.WriteLine("MPU9250: " + Q_mpu.Quaternion[0].ToString() + "   " + Q_mpu.Quaternion[1].ToString() + "   " + Q_mpu.Quaternion[2].ToString() + "   " + Q_mpu.Quaternion[3].ToString() + '\n');

            Q_mpu = Q_mpu.ConvertToConjugate();

            Q_bno = Q_bno.ConvertToConjugate();

            bno_cube.RotationMatrix = Q_bno.ConvertToRotationMatrix();

            mpu_cube.RotationMatrix = Q_mpu.ConvertToRotationMatrix();
        }

        /// <summary>
        /// xIMUserial CalInertialAndMagneticDataReceived event to update algorithm in IMU mode.
        /// </summary>
        static void xIMUserial_CalInertialAndMagneticDataReceived_updateIMU(object sender, x_IMU_API.CalInertialAndMagneticData e)
        {
            AHRS.Update(deg2rad(e.Gyroscope[0]), deg2rad(e.Gyroscope[1]), deg2rad(e.Gyroscope[2]), e.Accelerometer[0], e.Accelerometer[1], e.Accelerometer[2]);
        }

        /// <summary>
        /// xIMUserial CalInertialAndMagneticDataReceived event to update algorithm in AHRS mode.
        /// </summary>
        static void xIMUserial_CalInertialAndMagneticDataReceived_updateAHRS(object sender, x_IMU_API.CalInertialAndMagneticData e)
        {
            AHRS.Update(deg2rad(e.Gyroscope[0]), deg2rad(e.Gyroscope[1]), deg2rad(e.Gyroscope[2]), e.Accelerometer[0], e.Accelerometer[1], e.Accelerometer[2], e.Magnetometer[0], e.Magnetometer[1], e.Magnetometer[2]);
        }

        /// <summary>
        /// Converts degrees to radians.
        /// </summary>
        /// <param name="degrees">
        /// Angular quantity in degrees.
        /// </param>
        /// <returns>
        /// Angular quantity in radians.
        /// </returns>
        static float deg2rad(float degrees)
        {
            return (float)(Math.PI / 180) * degrees;
        }
    }
}