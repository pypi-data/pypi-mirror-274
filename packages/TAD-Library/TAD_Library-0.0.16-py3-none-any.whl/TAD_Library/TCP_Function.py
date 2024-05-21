import os.path
import sys
from socket import *
from time import sleep
from TCP_Packet_Lib import *
from threading import Thread
import io
import glob;

class TAD:
    __ip_address = '127.0.0.1'
    port = 111
    __max_packet_size = 2048
    __client_socket = None
    __server_socket = None
    __tcp_thread_exit_flag = False

    @classmethod
    def Start_Server(cls, device, callback):
        try:
            cls.__server_socket = socket(AF_INET, SOCK_STREAM)
            cls.__server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # if device == WEBCAM:
            #     self.server_socket.bind(self.ip_address, WEBCAM_PORT)
            # elif device == CANOE_COM:
            #     self.server_socket.bind(self.ip_address, CANOE_COM_PORT)
            # elif device == SSH:
            #     self.server_socket.bind(self.ip_address, SSH_PORT)
            # elif device == AVN:
            #     self.server_socket.bind(self.ip_address, AVN_PORT)
            # elif device == DLT:
            #     self.server_socket.bind(self.ip_address, DLT_PORT)
            # elif device == CCA:
            #     self.server_socket.bind(self.ip_address, CCA_PORT)
            if device == SSH:
                cls.__server_socket.bind((cls.__ip_address, SSH_PORT))
            else:
                printAK('Start_Server device type error: %s' % str(device))
                return False
            server_connection_thread = Thread(target=cls.__Server_ConnectionThread, args=(callback,))
            server_connection_thread.daemon = True
            server_connection_thread.start()
            return True
        except Exception as e:
            printAK('Start_Server error occurred: %s' % str(e))
            return False

    @classmethod
    def __Server_ConnectionThread(cls, callback):
        try:
            cls.__tcp_thread_exit_flag = False
            while not cls.__tcp_thread_exit_flag:
                cls.__server_socket.listen()
                client_socket, addr = cls.__server_socket.accept()
                server_thread = Thread(target=cls.__Server_Thread, args=(client_socket, callback,))
                server_thread.daemon = True
                server_thread.start()
        except Exception as e:
            printAK('Server_ConnectionThread error occurred: %s' % str(e))

    @classmethod
    def __Server_Thread(cls, client_socket, callback):
        try:
            cls.__tcp_thread_exit_flag = False
            while not cls.__tcp_thread_exit_flag:
                packet = client_socket.recv(cls.__max_packet_size)
                if (len(packet) == 0):
                    break
                print('Recv: ' + ''.join('%02x ' % i for i in packet))
                ret_packet = callback(packet)
                print('ret:  ' + ''.join('%02x ' % i for i in ret_packet))
                client_socket.send(bytes(ret_packet))
        except Exception as e:
            printAK('Server_Thread error occurred: %s' % str(e))

    @classmethod
    def __send(cls, packet):
        recv_packet = bytes()
        try:
            packet = TCP_Packet.check_length(packet)
            # print('Send  : ' + ''.join('%02x ' % i for i in packet))
            # print(TCP_Packet.check_packet(packet))
            # print(self.client_socket.send(bytes(packet)))
            cls.__client_socket.send(bytes(packet))
            recv_packet = cls.__client_socket.recv(cls.__max_packet_size)
            if recv_packet[0] == 0x11:
                # print('Recv  : ' + ''.join('%02x ' % i for i in recv_packet))
                pass
            elif recv_packet[0] == 0x12:  # 230622 Protocol 기준
                print('RecvEx: ' + ''.join('%02x ' % i for i in recv_packet))
                ex_packet = cls.__client_socket.recv(cls.__max_packet_size)
                # print('RecvEx:%d' %len(ex_packet))
                # print('RecvEx: ' + ''.join('%02x ' % i for i in ex_packet))
                recv_packet += ex_packet[7:-2]
                send_count = 1
                while ex_packet[2] == 0x01:
                    ex_packet = cls.__client_socket.recv(cls.__max_packet_size)
                    # print('RecvEx:%d' % len(ex_packet))
                    # print('RecvEx: ' + ''.join('%02x ' % i for i in ex_packet))
                    recv_packet += ex_packet[7:-2]
                    send_count += 1
                print('RecvEx Send %d times' % send_count)
        except Exception as e:
            printAK('send error occurred: %s' % str(e))
        sleep(0.1)
        return recv_packet

    @staticmethod
    def __get_status(status):
        _status = str(status).lower()
        if _status in ['on', '1', 'true']:
            return 0x01
        elif _status in ['off', '0', 'false']:
            return 0x00
        else:
            printAK('get_status value error: %s' % _status)
            return ERROR

    @staticmethod
    def __get_direction(direction):
        _direction = str(direction).lower()
        if _status in ['anti_clockwise', 'anti clockwise', 'left']:
            return 0x01
        elif _status in ['clockwise', 'right']:
            return 0x00
        else:
            printAK('value error: %s' % _status)
            return ERROR

    @staticmethod
    def __get_monitor(monitor):
        _monitor = str(monitor).lower()
        if _monitor in ['front', 'avn', '0']:
            return 0x00
        elif _monitor in ['rear_left', 'rear left', 'left', '1']:
            return 0x01
        elif _monitor in ['rear_right', 'rear right', 'right', '2']:
            return 0x02
        elif _monitor in ['cluster', '3']:
            return 0x03
        elif _monitor in ['hud', '4']:
            return 0x04
        else:
            printAK('get_monitor value error: %s' % _monitor)
            return ERROR

    @classmethod
    def Connect(cls, ip, port):
        try:
            printAK(f'Connect [{ip},{port}]')
            cls.__client_socket = socket(AF_INET, SOCK_STREAM)
            cls.__client_socket.connect((ip, port))
            return 1
        except Exception as e:
            printAK('ConnectCCA error occurred: %s' % str(e))
            return 0

    @classmethod
    def Disconnect(cls):
        try:
            printAK('DisconnectCCA')
            cls.__client_socket.close()
            return 1
        except Exception as e:
            printAK('DisconnectCCA error occurred: %s' % str(e))
            return 0

    @classmethod
    def GetWebcamImage(cls, path: str):
        try:
            printAK('GetWebcamImage: %s' % path)
            packet = TCP_Packet.get_base_packet('webcam', CMD_GetWebcamImage)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('GetWebcamImage error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Save Image
    def GetWebcamImage(cls, HDMI_index: int, path: str):
        try:
            printAK('GetWebcamImage: %s' % path)
            packet = TCP_Packet.get_base_packet('HDMI', CMD_GetWebcamImage)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('GetWebcamImage error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Save ROI Image
    def GetCamROIImage(cls, HDMI_index: int, x1: int, y1: int, x2: int, y2: int, path: str):
        try:
            printAK('GetCamROIImage: %s' % path)
            packet = TCP_Packet.get_base_packet('HDMI', CMD_GetWebcamImage)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('GetCamROIImage error occurred: %s' % str(e))
            return 0

    @classmethod
    def SaveWebcamVideo(cls, path: str):
        try:
            printAK('SaveWebcamVideo: %s' % path)
            packet = TCP_Packet.get_base_packet('webcam', CMD_SaveWebcamVideo)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SaveWebcamVideo error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Video save
    def SaveWebcamVideo(cls, HDMI_index: int, path: str):
        try:
            printAK('SaveWebcamVideo: %s' % path)
            packet = TCP_Packet.get_base_packet('HDMI', CMD_SaveWebcamVideo)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SaveWebcamVideo error occurred: %s' % str(e))
            return 0

    @classmethod
    def CamConnect(cls, cam_index: int):
        try:
            printAK('CamConnect: %s' % cam_index)
            packet = TCP_Packet.get_base_packet('webcam', CMD_CamConnect)
            packet = TCP_Packet.add_sub_command(packet, cam_index, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CamConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK CamConnect
    def CamConnect(cls, HDMI_index: int, cam_index: int):
        try:
            printAK('CamConnect: %s' % cam_index)
            packet = TCP_Packet.get_base_packet('HDMI', CMD_CamConnect)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, cam_index - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CamConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def CamDisconnect(cls):
        try:
            # print('CamDisconnect')
            printAK('CamDisconnect')
            packet = TCP_Packet.get_base_packet('webcam', CMD_CamDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CamDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK CamDisconnect
    def CamDisconnect(cls, HDMI_index: int):
        try:
            # print('CamDisconnect')
            printAK('CamDisconnect')
            packet = TCP_Packet.get_base_packet('HDMI', CMD_CamDisconnect)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CamDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetCamRecordingTime(cls, recording_time: int):
        try:
            # printAK('SetCamRecordingTime')
            packet = TCP_Packet.get_base_packet('webcam', CMD_SetCamRecordingTime)
            packet = TCP_Packet.add_sub_command(packet, recording_time, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d초) -> PASS' % recording_time)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SetCamRecordingTime error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Recording Time
    def SetCamRecordingTime(cls, HDMI_index: int, recording_time: int):
        try:
            # printAK('SetCamRecordingTime')
            packet = TCP_Packet.get_base_packet('HDMI', CMD_SetCamRecordingTime)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, recording_time, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d초) -> PASS' % recording_time)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SetCamRecordingTime error occurred: %s' % str(e))
            return 0

    @classmethod
    def CamHeartbeat(cls):
        try:
            printAK('CamHeartbeat')
            packet = TCP_Packet.get_base_packet('webcam', CMD_CamHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CamHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK CamImgCompare(Time)
    def CamCompare(cls, HDMI_index, Base_image, Cutline):
        try:
            # print('CamDisconnect')
            printAK('CompareTime Start')
            packet = TCP_Packet.get_base_packet('HDMI', CMD_CamCompare)
            packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, Base_image, str)
            packet = TCP_Packet.add_sub_command(packet, Cutline, float)

            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)

            if sub_command[0][0] == 0x1:
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                score = struct.unpack('f', sub_command[1])[0]
                score_round = round(score, 2)
                return 1, score_round
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                score = struct.unpack('f', sub_command[1])[0]
                score_round = round(score, 2)
                return 0, score_round

        except Exception as e:
            printAK('CamCompare error occurred: %s' % str(e))
            return 0

    # @classmethod
    # # PRK CamImgCompare(Time)
    # def CompareTime(cls, HDMI_index, Base_image, Result_Path, Cutline, seconds):
    #     try:
    #         # print('CamDisconnect')
    #         printAK('CompareTime Start')
    #         packet = TCP_Packet.get_base_packet('webcam', CMD_CompareTime)
    #         packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
    #         packet = TCP_Packet.add_sub_command(packet, Base_image, str)
    #         packet = TCP_Packet.add_sub_command(packet, Result_Path, str)
    #         packet = TCP_Packet.add_sub_command(packet, Cutline, float)
    #         packet = TCP_Packet.add_sub_command(packet, seconds, int, 1)
    #
    #         recv = cls.__send(packet)
    #         sub_command = TCP_Packet.GetSubCommand(recv)
    #         if (sub_command[0][0] == 0x1):
    #             printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
    #         else:
    #             printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
    #         return sub_command[0][0]
    #     except Exception as e:
    #         printAK('CamDisconnect error occurred: %s' % str(e))
    #         return 0

    # @classmethod
    # # PRK CamImgCompare(Frame)
    # def CompareFrame(cls, HDMI_index, Base_image, Result_Path, Cutline, frame_cnt):
    #     try:
    #         # print('CamDisconnect')
    #         printAK('CompareFrame Start')
    #         packet = TCP_Packet.get_base_packet('webcam', CMD_CompareFrame)
    #         packet = TCP_Packet.add_sub_command(packet, HDMI_index, int, 1)
    #         packet = TCP_Packet.add_sub_command(packet, Base_image, str)
    #         packet = TCP_Packet.add_sub_command(packet, Result_Path, str)
    #         packet = TCP_Packet.add_sub_command(packet, Cutline, float)
    #         packet = TCP_Packet.add_sub_command(packet, frame_cnt, int, 1)
    #
    #         recv = cls.__send(packet)
    #         sub_command = TCP_Packet.GetSubCommand(recv)
    #         if (sub_command[0][0] == 0x1):
    #             printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
    #         else:
    #             printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
    #         return sub_command[0][0]
    #     except Exception as e:
    #         printAK('CamDisconnect error occurred: %s' % str(e))
    #         return 0

    @classmethod
    def GetCANSignal(cls, message_name: str, signal_name: str, channel: int = 1):
        try:
            printAK('GetCANSignal: %s %s %s' % (message_name, signal_name, channel))
            packet = TCP_Packet.get_base_packet('canoe_com', CMD_GetCANSignal)
            packet = TCP_Packet.add_sub_command(packet, message_name, str)
            packet = TCP_Packet.add_sub_command(packet, signal_name, str)
            packet = TCP_Packet.add_sub_command(packet, channel, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x01):
                printAK('1 -> PASS')
                return 1, struct.unpack('f', sub_command[1])[0]
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetCANSignal error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def SetCANSignal(cls, message_name: str, signal_name: str, value: float, channel: int = 1):
        try:
            printAK('SetCANSignal: %s %s %s %s' % (message_name, signal_name, value, channel))
            packet = TCP_Packet.get_base_packet('canoe_com', CMD_SetCANSignal)
            packet = TCP_Packet.add_sub_command(packet, message_name, str)
            packet = TCP_Packet.add_sub_command(packet, signal_name, str)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            packet = TCP_Packet.add_sub_command(packet, channel, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SetCANSignal error occurred: %s' % str(e))
            return 0

    @classmethod
    def StartCANoeCfg(cls, cfg_path: str):
        try:
            printAK('StartCANoeCfg: %s' % cfg_path)
            packet = TCP_Packet.get_base_packet('canoe_com', CMD_StartCANoeCfg)
            packet = TCP_Packet.add_sub_command(packet, cfg_path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('StartCANoeCfg error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANoeConnect(cls):
        try:
            # printAK('CANoeConnect')
            packet = TCP_Packet.get_base_packet('canoe_com', CMD_CANoeConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANoeConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANoeDisconnect(cls):
        try:
            # printAK('CANoeDisconnect')
            packet = TCP_Packet.get_base_packet('canoe_com', CMD_CANoeDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANoeDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANoeHeartbeat(cls):
        try:
            printAK('CANoeHeartbeat')
            packet = TCP_Packet.get_base_packet('canoe_com', CMD_CANoeHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANoeHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    def SendSSHCmd(cls, command: str):
        try:
            packet = TCP_Packet.get_base_packet('ssh', CMD_SendSSHCmd)
            packet = TCP_Packet.add_sub_command(packet, command, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x1:
                printAK(sys._getframe(0).f_code.co_name + '(%s) -> PASS' % command)
                return 1, sub_command[1].decode('utf-8')
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%s) -> FAIL(%d) ' % (command, sub_command[0][0]))
                return 0, ''
        except Exception as e:
            printAK('SendSSHCmd error occurred: %s' % str(e))
            return 0, ''

    @classmethod
    def SSHConnect(cls):
        try:
            # printAK('SSHConnect')
            packet = TCP_Packet.get_base_packet('ssh', CMD_SSHConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SSHConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def SSHDisconnect(cls):
        try:
            # printAK('SSHDisconnect')
            packet = TCP_Packet.get_base_packet('ssh', CMD_SSHDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SSHDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def SSHConvertFile01(cls, command: str):
        try:
            printAK('SSHConvertFile01: %s' % command)
            packet = TCP_Packet.get_base_packet('ssh', CMD_SSHConvertFile01)
            packet = TCP_Packet.add_sub_command(packet, command, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SSHConvertFile01 error occurred: %s' % str(e))
            return 0

    @classmethod
    def SSHHeartbeat(cls):
        try:
            printAK('SSHHeartbeat')
            packet = TCP_Packet.get_base_packet('ssh', CMD_SSHHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('SSHHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqImgSave(cls, savePath: str, x1: int = -1, y1: int = -1, x2: int = -1, y2: int = -1,
                   monitor: Monitor = Monitor.front):
        try:
            if (monitor == Monitor.front):
                monitor_str = "FRONT"
            elif (monitor == Monitor.rear_left):
                monitor_str = "REAR_L"
            elif (monitor == Monitor.rear_right):
                monitor_str = "REAR_R"
            elif (monitor == Monitor.cluster):
                monitor_str = "CLU"
            elif (monitor == Monitor.HUD):
                monitor_str = "HUD"

            fName = os.path.basename(savePath)

            # Image 이름 포맷 안맞추는 경우 예외처리
            if fName.count('.') == 1:  # 단순 확장자만 붙여서 작성한 경우
                name = fName.split('.')[0]
                extension = fName.split('.')[1]
                newName = "%s[%s.%s.%s.%s.%s].%s" % (name, x1, y1, x2, y2, monitor_str, extension)
                savePath = savePath.replace(fName, newName)

            # printAK('ReqImgSave: %s %s %s %s %s %s' %(savePath, x1, y1, x2, y2, monitor))
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqImgSave)
            packet = TCP_Packet.add_sub_command(packet, savePath, str)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            # packet = TCP_Packet.add_sub_command(packet, cls.get_monitor(monitor), int, 1)
            packet = TCP_Packet.add_sub_command(packet, monitor.value, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (경로 : %s / 좌표 : %s,%s,%s,%s / 모니터 : %s) -> PASS' % (
                    savePath, x1, y1, x2, y2, monitor_str))
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('ReqImgSave error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqImgBuffer(cls, x1: int = -1, y1: int = -1, x2: int = -1, y2: int = -1, monitor: Monitor = Monitor.front):
        try:
            printAK('ReqImgBuffer: %s %s %s %s %s' % (x1, y1, x2, y2, monitor))
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqImgBuffer)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            # packet = TCP_Packet.add_sub_command(packet, cls.get_monitor(monitor), int, 1)
            packet = TCP_Packet.add_sub_command(packet, monitor.value, int, 1)
            recv = cls.__send(packet)
            print(len(recv))
            sub_command = TCP_Packet.GetSubCommand(recv)
            if recv[8] == 0x01:
                image_stream = io.BytesIO(recv[19:-4])
                printAK('1 -> PASS')
                return 1, Image.open(image_stream)
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, None
        except Exception as e:
            printAK('ReqImgBuffer error occurred: %s' % str(e))
            return 0, None

    @classmethod
    def ReqTouch(cls, x_pos: int, y_pos: int, press_time: float = 0, monitor: Monitor = Monitor.front):
        try:
            # printAK()
            _press_time = int(press_time * 10)
            if _press_time > 0xff:
                _press_time = 0xff
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqTouch)
            packet = TCP_Packet.add_sub_command(packet, x_pos, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y_pos, int, 2)
            packet = TCP_Packet.add_sub_command(packet, _press_time, int, 1)
            # packet = TCP_Packet.add_sub_command(packet, cls.get_monitor(monitor), int, 1)
            packet = TCP_Packet.add_sub_command(packet, monitor.value, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s %s %s %s)' % (
                    x_pos, y_pos, press_time, monitor) + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('ReqTouch error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqDrag(cls, x1: int, y1: int, x2: int, y2: int, drag_time: float = 0, monitor: Monitor = Monitor.front):
        try:
            printAK('ReqDrag: %s %s %s %s %s %s' % (x1, y1, x2, y2, drag_time, monitor))
            _drag_time = int(drag_time * 10)
            if _drag_time > 0xff:
                _drag_time = 0xff
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqDrag)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, _drag_time, int, 1)
            # packet = TCP_Packet.add_sub_command(packet, cls.get_monitor(monitor), int, 1)
            packet = TCP_Packet.add_sub_command(packet, monitor.value, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('ReqDrag error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqHardkey(cls, key_value: Hardkey, direction: Dir = Dir.NONE, long_press=False):
        try:
            printAK('ReqHardkey: %s %s %s' % (key_value, direction, long_press))
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqHardkey)
            packet = TCP_Packet.add_sub_command(packet, key_value.value, int, 2)
            # packet = TCP_Packet.add_sub_command(packet, cls.get_direction(direction), int, 1)
            if direction.value is not None:
                packet = TCP_Packet.add_sub_command(packet, direction.value, int, 1)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(long_press), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('ReqHardkey error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqSystemResource(cls):
        try:
            printAK('ReqSystemResource')
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqSystemResource)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                mem_usage = struct.unpack('f', sub_command[1])[0]
                cpu_usage = sub_command[2][0]
                printAK('1 -> PASS')
                return 1, mem_usage, cpu_usage
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1, -1
        except Exception as e:
            printAK('ReqSystemResource error occurred: %s' % str(e))
            return 0, -1, -1

    @classmethod
    def AVNConnect(cls):
        try:
            # printAK('AVNConnect')
            packet = TCP_Packet.get_base_packet('avn', CMD_AVNConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('AVNConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def AVNDisconnect(cls):
        try:
            # printAK('AVNDisconnect')
            packet = TCP_Packet.get_base_packet('avn', CMD_AVNDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('AVNDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqMainVersion(cls):
        try:
            printAK('ReqMainVersion')
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqMainVersion)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x1:
                printAK('1 -> PASS')
                return 1, sub_command[1].decode('utf-8')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, sub_command[1].decode('utf-8')
        except Exception as e:
            printAK('ReqMainVersion error occurred: %s' % str(e))
            return 0, ''

    @classmethod
    def ReqSubVersion(cls):
        try:
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqSubVersion)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x1:
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                return 1, sub_command[1].decode('utf-8')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return 0, sub_command[1].decode('utf-8')
        except Exception as e:
            printAK('ReqSubVersion error occurred: %s' % str(e))
            return 0, ''

    @classmethod
    def AVNHeartbeat(cls):
        try:
            printAK('AVNHeartbeat')
            packet = TCP_Packet.get_base_packet('avn', CMD_AVNHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('AVNHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqRefreshImage(cls, monitor: Monitor = Monitor.front):
        try:
            # printAK('Refresh AVN Screen')
            packet = TCP_Packet.get_base_packet('avn', CMD_ReqRefreshImage)
            packet = TCP_Packet.add_sub_command(packet, monitor.value, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('Refresh AVN Screen error occurred: %s' % str(e))
            return 0

    @classmethod
    def WaitDLTLog(cls, log_text: str, timeout: int):
        try:
            printAK(sys._getframe(0).f_code.co_name + '(%s, %d) -> START' % (log_text, timeout))
            packet = TCP_Packet.get_base_packet('dlt', CMD_WaitDLTLog)
            packet = TCP_Packet.add_sub_command(packet, log_text, str)
            packet = TCP_Packet.add_sub_command(packet, timeout, int, 2)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s, %d) -> PASS' % (log_text, timeout))
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            print('WaitDLTLog error occurred: %s' % str(e))
            return 0

    @classmethod
    def SaveDLTLog(cls, filename: str):
        try:
            printAK('SaveDLTLog: %s' % filename)
            packet = TCP_Packet.get_base_packet('dlt', CMD_SaveDLTLog)
            packet = TCP_Packet.add_sub_command(packet, filename, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            print('SaveDLTLog error occurred: %s' % str(e))
            return 0

    @classmethod
    def DLTConnect(cls):
        try:
            # printAK('DLTConnect')
            packet = TCP_Packet.get_base_packet('dlt', CMD_DLTConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])

            return sub_command[0][0]
        except Exception as e:
            print('DLTConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def DLTDisconnect(cls):
        try:
            # printAK('DLTDisconnect')
            packet = TCP_Packet.get_base_packet('dlt', CMD_DLTDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            print('DLTDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetDLTRecordingTime(cls, recording_time: int = 10):
        try:
            # printAK('SetDLTRecordingTime: %d' %recording_time)
            packet = TCP_Packet.get_base_packet('dlt', CMD_SetDLTRecordingTime)
            packet = TCP_Packet.add_sub_command(packet, recording_time, int, 2)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d초) -> PASS' % recording_time)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            print('SetDLTRecordingTime error occurred: %s' % str(e))
            return 0

    @classmethod
    def DLTHeartbeat(cls):
        try:
            printAK('DLTHeartbeat')
            packet = TCP_Packet.get_base_packet('dlt', CMD_DLTHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            print('DLTHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    def ConnectCCA(cls):
        try:
            printAK('ConnectCCA')
            cls.__client_socket = socket(AF_INET, SOCK_STREAM)
            cls.__client_socket.connect((cls.__ip_address, cls.port))
            return 1
        except Exception as e:
            printAK('ConnectCCA error occurred: %s' % str(e))
            return 0

    @classmethod
    def DisconnectCCA(cls):
        try:
            printAK('DisconnectCCA')
            cls.__client_socket.close()
            return 1
        except Exception as e:
            printAK('DisconnectCCA error occurred: %s' % str(e))
            return 0

    @classmethod
    def CompareImage(cls, ScrImgPath: str, ROIImagePath: str):
        try:
            printAK('CompareImage: %s %s' % (ScrImgPath, ROIImagePath))
            packet = TCP_Packet.get_base_packet('cca', CMD_CompareImage)
            packet = TCP_Packet.add_sub_command(packet, ScrImgPath, str)
            packet = TCP_Packet.add_sub_command(packet, ROIImagePath, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CompareImage error occurred: %s' % str(e))
            return 0

    @classmethod
    def CompareAVNScreen(cls, ROIImagePath: str):
        try:
            printAK('CompareAVNScreen: %s' % ROIImagePath)
            packet = TCP_Packet.get_base_packet('cca', CMD_CompareAVNScreen)
            packet = TCP_Packet.add_sub_command(packet, ROIImagePath, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK('1 -> PASS')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CompareAVNScreen error occurred: %s' % str(e))
            return 0

    @classmethod
    def ReqWriteReportStart(cls, testTitle: str):
        try:
            packet = TCP_Packet.get_base_packet('cca', CMD_ReqReportWriteStart)
            packet = TCP_Packet.add_sub_command(packet, testTitle, str)

            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)

            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')

                # Savepath Return
                return sub_command[1].decode('utf-8')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return ''

        except Exception as e:
            printAK('Request Report Write start : %s' % str(e))
            return 0

    @classmethod
    def ReqWriteReportStop(cls):
        try:
            packet = TCP_Packet.get_base_packet('cca', CMD_ReqReportWriteStop)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])

            return sub_command[0][0]
        except Exception as e:
            printAK('Request Report Write stop : %s' % str(e))
            return 0

    @classmethod
    def ReqWriteReport(cls, function: str, comment: str, result: int):
        try:
            packet = TCP_Packet.get_base_packet('cca', CMD_ReqReportWrite)
            packet = TCP_Packet.add_sub_command(packet, function, str)
            packet = TCP_Packet.add_sub_command(packet, comment, str)
            packet = TCP_Packet.add_sub_command(packet, result, int, 1)

            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('Request Report Write : %s' % str(e))
            return 0

    @classmethod
    def SetCCAManualControl(cls, status):
        try:
            # printAK('SetCCAManualControl: %s' %status)
            packet = TCP_Packet.get_base_packet('cca', CMD_SetCCAManualControl)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '%s -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + '%s -> FAIL(%d)' % (status, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('SetCCAManualControl error occurred: %s' % str(e))
            return 0

    @classmethod
    def BenchConnect(cls, bench_type: int):
        try:
            # printAK('BenchConnect: %s' %bench_type)
            packet = TCP_Packet.get_base_packet('cca', CMD_BenchConnect)
            packet = TCP_Packet.add_sub_command(packet, bench_type, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(Type : %s) -> PASS' % bench_type)
            else:
                printAK(sys._getframe(0).f_code.co_name + '(Type : %s) -> FAIL(%d)' % (bench_type, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('BenchConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK 자동화를 위한 벤치 연결 함수
    def BenchConnect(cls, bench_number: int, bench_type: int):
        try:
            # printAK('BenchConnect: %s' %bench_type)
            packet = TCP_Packet.get_base_packet('cca', CMD_BenchConnect)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            packet = TCP_Packet.add_sub_command(packet, bench_type, int, 1)

            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)

            if (sub_command[0][0] == 0x1):
                printAK(
                    sys._getframe(0).f_code.co_name + '(Number : %s, Type : %s) -> PASS' % (bench_number, bench_type))
            else:
                printAK(sys._getframe(0).f_code.co_name + '(Number : %s, Type : %s) -> FAIL(%d)' % (
                    bench_number, bench_type, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('BenchConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def BenchDisconnect(cls):
        try:
            # printAK('BenchDisconnect')
            packet = TCP_Packet.get_base_packet('cca', CMD_BenchDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])

            return sub_command[0][0]
        except Exception as e:
            printAK('BenchDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK 자동화를 위한 벤치 연결 해제 함수
    def BenchDisconnect(cls, bench_number: int):
        try:
            # printAK('BenchDisconnect')
            packet = TCP_Packet.get_base_packet('cca', CMD_BenchDisconnect)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)

            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])

            return sub_command[0][0]
        except Exception as e:
            printAK('BenchDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetBenchBPlus(cls, status):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'
            # printAK('SetBenchBPlus: %s' %_status)
            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchBPlus)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchBPlus error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Bench B+
    def SetBenchBPlus(cls, bench_number: int, status):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'
            # printAK('SetBenchBPlus: %s' %_status)
            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchBPlus)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchBPlus error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetBenchAcc(cls, status):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'
            # printAK('SetBenchAcc: %s' %_status)
            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchAcc)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchAcc error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Bench ACC
    def SetBenchAcc(cls, bench_number: int, status):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'
            # printAK('SetBenchAcc: %s' %_status)
            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchAcc)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchAcc error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetBenchIgn(cls, status):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'
            # printAK('SetBenchIgn: %s' %_status)
            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchIgn)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchIgn error occurred: %s' % str(e))
            return 0

    @classmethod
    # PRK Bench IGN
    def SetBenchIgn(cls, bench_number: int, status):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'

            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchIgn)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchIgn error occurred: %s' % str(e))
            return 0

    @classmethod
    def GetBenchVolt(cls):
        try:
            printAK('GetBenchVolt')
            packet = TCP_Packet.get_base_packet('cca', CMD_GetBenchVolt)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                volt = struct.unpack('f', sub_command[1])[0]
                volt_round = round(volt, 2)
                printAK('1 -> PASS, %.2fV' % volt_round)
                return 1, volt_round
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetBenchVolt error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def GetBenchVolt(cls, bench_number: int):
        try:
            printAK('GetBenchVolt')
            packet = TCP_Packet.get_base_packet('cca', CMD_GetBenchVolt)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)

            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                volt = struct.unpack('f', sub_command[1])[0]
                volt_round = round(volt, 2)
                printAK('1 -> PASS, %.2fV' % volt_round)
                return 1, volt_round
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetBenchVolt error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def GetBenchCurr(cls):
        try:
            printAK('GetBenchCurr')
            packet = TCP_Packet.get_base_packet('cca', CMD_GetBenchCurr)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                current = struct.unpack('f', sub_command[1])[0]
                current_round = round(current, 2)
                printAK('1 -> PASS, %.2fA' % current_round)
                return 1, current_round
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetBenchCurr error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def GetBenchCurr(cls, bench_number: int):
        try:
            printAK('GetBenchCurr')
            packet = TCP_Packet.get_base_packet('cca', CMD_GetBenchCurr)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                current = struct.unpack('f', sub_command[1])[0]
                current_round = round(current, 2)
                printAK('1 -> PASS, %.2fA' % current_round)
                return 1, current_round
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetBenchCurr error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def GetBenchWatt(cls):
        try:
            printAK('GetBenchWatt')
            packet = TCP_Packet.get_base_packet('cca', CMD_GetBenchWatt)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                watt = struct.unpack('f', sub_command[1])[0]
                watt_round = round(watt, 2)
                printAK('1 -> PASS, %.2fW' % watt_round)
                return 1, watt_round
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetBenchWatt error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def GetBenchWatt(cls, bench_number: int):
        try:
            printAK('GetBenchWatt')
            packet = TCP_Packet.get_base_packet('cca', CMD_GetBenchWatt)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                watt = struct.unpack('f', sub_command[1])[0]
                watt_round = round(watt, 2)
                printAK('1 -> PASS, %.2fW' % watt_round)
                return 1, watt_round
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return 0, -1
        except Exception as e:
            printAK('GetBenchWatt error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockConnect(cls):
        try:
            packet = TCP_Packet.get_base_packet('cca', CMD_ClockConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
        except Exception as e:
            printAK('ClockConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetBenchVolt(cls, bench_number: int, voltage: float):
        try:
            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchVolt)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            packet = TCP_Packet.add_sub_command(packet, voltage, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%.2fV) -> PASS' % voltage)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%.2fV) -> FAIL(%d)' % (voltage, sub_command[0][0]))

            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchVolt error occurred: %s' % str(e))
            return 0

    @classmethod
    def SetBenchPower(cls, bench_number: int, status: bool):
        try:
            if status:
                _status = 'on'
            else:
                _status = 'off'

            packet = TCP_Packet.get_base_packet('cca', CMD_SetBenchPower)
            packet = TCP_Packet.add_sub_command(packet, bench_number, int, 1)
            packet = TCP_Packet.add_sub_command(packet, cls.__get_status(status), int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % _status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (_status, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('SetBenchPower error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlConnect(cls):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlDisconnect(cls):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlDisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlLoadDBC(cls, dbc_path: str):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlLoadDBC)
            packet = TCP_Packet.add_sub_command(packet, dbc_path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> PASS' % dbc_path)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s) -> FAIL(%d)' % (dbc_path, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlLoadDBC error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlSendSignal(cls, message_name: str, signal_name: str, value: float, channel: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlSendSignal)
            packet = TCP_Packet.add_sub_command(packet, message_name, str)
            packet = TCP_Packet.add_sub_command(packet, signal_name, str)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            packet = TCP_Packet.add_sub_command(packet, channel - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s %s %f %d) -> PASS' % (
                message_name, signal_name, value, channel))
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s %s %f %d) -> FAIL(%d)' % (
                message_name, signal_name, value, channel, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlSendSignal error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlGetSignal(cls, message_name: str, signal_name: str, channel: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlGetSignal)
            packet = TCP_Packet.add_sub_command(packet, message_name, str)
            packet = TCP_Packet.add_sub_command(packet, signal_name, str)
            packet = TCP_Packet.add_sub_command(packet, channel - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = int(struct.unpack('f', sub_command[1])[0])
                printAK(sys._getframe(0).f_code.co_name + ' (%s %s %d) -> PASS(0x%x)' % (
                message_name, signal_name, channel, value))
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s %s %d) -> FAIL(%d)' % (
                message_name, signal_name, channel, sub_command[0][0]))
                return sub_command[0][0], -1
        except Exception as e:
            printAK('CANxlGetSignal error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def CANxlGetSignalEx(cls, message_name: str, signal_name: str, channel: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlGetSignal)
            packet = TCP_Packet.add_sub_command(packet, message_name, str)
            packet = TCP_Packet.add_sub_command(packet, signal_name, str)
            packet = TCP_Packet.add_sub_command(packet, channel - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = int(struct.unpack('f', sub_command[1])[0])
                time = struct.unpack('i', sub_command[2])[0]
                timestamp = struct.unpack('Q', sub_command[3])[0]
                printAK(sys._getframe(0).f_code.co_name + ' (%s %s %d) -> PASS(0x%x %dms timestamp:%d)' % (
                message_name, signal_name, channel, value, time, timestamp))
                return sub_command[0][0], value, time, timestamp
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s %s %d) -> FAIL(%d)' % (
                message_name, signal_name, channel, sub_command[0][0]))
                return sub_command[0][0], -1, -1, 0
        except Exception as e:
            printAK('CANxlGetSignal error occurred: %s' % str(e))
            return 0, -1, -1, 0

    @classmethod
    def CANxlSetRecordingTime(cls, recording_time: int):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlSetRecordingTime)
            packet = TCP_Packet.add_sub_command(packet, recording_time, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x1:
                printAK(sys._getframe(0).f_code.co_name + ' (%d) -> PASS' % (recording_time))
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%d) -> FAIL(%d)' % (recording_time, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlSetRecordingTime error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlSaveMessageBuffer(cls, path: str):
        try:
            printAK('CANxlSaveMessageBuffer: %s' % path)
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlSaveMessageBuffer)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x1:
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlSaveMessageBuffer error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlStopMessage(cls, message_name: str, channel: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlStopMessage)
            packet = TCP_Packet.add_sub_command(packet, message_name, str)
            packet = TCP_Packet.add_sub_command(packet, channel, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x1:
                printAK(sys._getframe(0).f_code.co_name + '(%s ch%d) -> PASS' % (message_name, channel))
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%s ch%d) -> FAIL(%d)' % (
                message_name, channel, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlStopMessage error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlCheckPeriodStart(cls, message_id: int, channel: int, period_limit: int, timeout: int):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlCheckPeriodStart)
            packet = TCP_Packet.add_sub_command(packet, message_id, int, 4)
            packet = TCP_Packet.add_sub_command(packet, channel, int, 1)
            packet = TCP_Packet.add_sub_command(packet, period_limit, int, 4)
            packet = TCP_Packet.add_sub_command(packet, timeout, int, 4)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%d %d %d %d) -> PASS' % (
                message_id, channel, period_limit, timeout))
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%d %d %d %d) -> FAIL(%d)' % (
                message_id, channel, period_limit, timeout, sub_command[0][0]))
                return sub_command[0][0]
        except Exception as e:
            printAK('CANxl CheckPeriodStart error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlCheckPeriodStop(cls, message_id: int, channel: int):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlCheckPeriodStop)
            packet = TCP_Packet.add_sub_command(packet, message_id, int, 4)
            packet = TCP_Packet.add_sub_command(packet, channel, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                failPeriodCount = int(struct.unpack('i', sub_command[1])[0])
                printAK(
                    sys._getframe(0).f_code.co_name + ' (%d %d) -> PASS(%d)' % (message_id, channel, failPeriodCount))
                return sub_command[0][0], failPeriodCount
            else:
                printAK(
                    sys._getframe(0).f_code.co_name + ' (%d %d) -> FAIL(%d)' % (message_id, channel, sub_command[0][0]))
                return sub_command[0][0], -1
        except Exception as e:
            printAK('CANxl CheckPeriodStop error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def CANxlStartSaveCANLog(cls, saveFolder: str, interval: int):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlStartSaveCANLog)
            packet = TCP_Packet.add_sub_command(packet, saveFolder, str)
            packet = TCP_Packet.add_sub_command(packet, interval, int)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' (%s interval:%d분) -> PASS' % (saveFolder, interval))
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' (%s interval:%d분) -> FAIL(%d)' % (
                saveFolder, interval, sub_command[0][0]))
                return sub_command[0][0]
        except Exception as e:
            printAK('CANxl StartSaveCANLog error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlStopSaveCANLog(cls):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlStopSaveCANLog)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('CANxl StopSaveCANLog error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANxlHeartbeat(cls):
        try:
            packet = TCP_Packet.get_base_packet('canxl', CMD_CANxlHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('CANxlHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockStart(cls, index: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('clock', CMD_ClockStart)
            packet = TCP_Packet.add_sub_command(packet, index - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % index)
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> FAIL(%d)' % (index, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('ClockStart error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockStop(cls, index: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('clock', CMD_ClockStop)
            packet = TCP_Packet.add_sub_command(packet, index - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % index)
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> FAIL(%d)' % (index, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('ClockStop error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockSetText1(cls, text: str, index: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('clock', CMD_ClockSetText1)
            packet = TCP_Packet.add_sub_command(packet, text, str)
            packet = TCP_Packet.add_sub_command(packet, index - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s %d) -> PASS' % (text, index))
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%s %d) -> FAIL(%d)' % (text, index, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('ClockSetText1 error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockSetText2(cls, text: str, index: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('clock', CMD_ClockSetText2)
            packet = TCP_Packet.add_sub_command(packet, text, str)
            packet = TCP_Packet.add_sub_command(packet, index - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s %d) -> PASS' % (text, index))
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%s %d) -> FAIL(%d)' % (text, index, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('ClockSetText2 error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockReset(cls, index: int = 1):
        try:
            packet = TCP_Packet.get_base_packet('clock', CMD_ClockReset)
            packet = TCP_Packet.add_sub_command(packet, index - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % index)
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> FAIL(%d)' % (index, sub_command[0][0]))
            return sub_command[0][0]
        except Exception as e:
            printAK('ClockReset error occurred: %s' % str(e))
            return 0

    @classmethod
    def ClockHeartbeat(cls):
        try:
            packet = TCP_Packet.get_base_packet('clock', CMD_ClockHeartbeat)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('ClockHeartbeat error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610Connect(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610Connect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 Connect error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610Disconnect(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610Disconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 Disconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610SetMode(cls, mode: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetMode)
            packet = TCP_Packet.add_sub_command(packet, mode - 1, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % mode)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetMode error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetMode(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetMode)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = int.from_bytes(sub_command[1], byteorder='big', signed=True) + 1
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetMode error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetOutput(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetOutput)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetOutput error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetOutput(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetOutput)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetOutput error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetRCAL(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetRCAL)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetRCAL error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetRCAL(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetRCAL)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetRCAL error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetDCVal(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetDCVal)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.3f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetDCVal error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetDCVal(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetDCVal)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.3f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetDCVal error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetACVal(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetACVal)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.2f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetACVal error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetACVal(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetACVal)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.2f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetACVal error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetFreq(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetFreq)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.1f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetFreq error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetFreq(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetFreq)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetFreq error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetWave(cls, wave: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetWave)
            packet = TCP_Packet.add_sub_command(packet, wave, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % wave)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetWave error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetWave(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetWave)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetWave error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetLMVP(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetLMVP)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.1f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetLMVP error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetLMVP(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetLMVP)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetLMVP error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetLMVM(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetLMVM)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.1f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetLMVM error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetLMVM(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetLMVM)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetLMVM error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetLMCP(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetLMCP)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.1f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetLMCP error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetLMCP(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetLMCP)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetLMCP error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetLMCM(cls, value: float):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetLMCM)
            packet = TCP_Packet.add_sub_command(packet, value, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%.1f) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetLMCM error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetLMCM(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetLMCM)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetLMCM error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SequenceLoad(cls, path: str):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SequenceLoad)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s) -> PASS' % path)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SequenceLoad error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610SequenceControl(cls, value: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SequenceControl)
            packet = TCP_Packet.add_sub_command(packet, value, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s) -> PASS' % value)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SequenceControl error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610SequenceGetStatus(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SequenceGetStatus)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 SequenceGetStatus error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SequenceClear(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SequenceClear)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SequenceClear error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610MemoryStore(cls, number: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610MemoryStore)
            packet = TCP_Packet.add_sub_command(packet, number, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s) -> PASS' % number)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 MemoryStore error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610MemoryRecall(cls, number: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610MemoryRecall)
            packet = TCP_Packet.add_sub_command(packet, number, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s) -> PASS' % number)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 MemoryRecall error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610MeasureDCVolt(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610MeasureDCVolt)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 MeasureDCVolt error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610MeasureACVolt(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610MeasureACVolt)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.0f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 MeasureACVolt error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610MeasureDCCurr(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610MeasureDCCurr)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.2f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 MeasureDCCurr error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610MeasureACCurr(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610MeasureACCurr)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = struct.unpack('f', sub_command[1])[0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%.1f)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 MeasureACCurr error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610GetModel(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetModel)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                number = sub_command[1].decode('utf-8')
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%s)' % number)
                return sub_command[0][0], number
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], ''
        except Exception as e:
            printAK('BP4610 GetModel error occurred: %s' % str(e))
            return 0, ''

    @classmethod
    def BP4610GetVersion(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetVersion)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                number = sub_command[1].decode('utf-8')
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%s)' % number)
                return sub_command[0][0], number
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], ''
        except Exception as e:
            printAK('BP4610 GetVersion error occurred: %s' % str(e))
            return 0, ''

    @classmethod
    def BP4610SetBeep(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetBeep)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetBeep error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetBeep(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetBeep)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetBeep error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetHeader(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetHeader)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetHeader error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetHeader(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetHeader)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetHeader error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetIOUT(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetIOUT)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetIOUT error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetIOUT(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetIOUT)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetIOUT error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetIRSP(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetIRSP)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetIRSP error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetIRSP(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetIRSP)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetIRSP error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SetXCTL(cls, status: int):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SetXCTL)
            packet = TCP_Packet.add_sub_command(packet, status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % status)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
            return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 SetXCTL error occurred: %s' % str(e))
            return 0

    @classmethod
    def BP4610GetXCTL(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610GetXCTL)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 GetXCTL error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610SelfTest(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610SelfTest)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                value = sub_command[1][0]
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS(%d)' % value)
                return sub_command[0][0], value
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('BP4610 SelfTest error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def BP4610ResetDevice(cls):
        try:
            packet = TCP_Packet.get_base_packet('bp4610', CMD_BP4610ResetDevice)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('BP4610 ResetDevice error occurred: %s' % str(e))
            return 0

    @classmethod
    def FPGAConnect(cls):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGAConnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('FPGA Connect error occurred: %s' % str(e))
            return 0

    @classmethod
    def FPGADisconnect(cls):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGADisconnect)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + ' -> PASS')
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('FPGA Disconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def FPGASaveImage(cls, path: str, dev_num: int, channel: int, x1: int = 0, y1: int = 0, x2: int = 1280,
                      y2: int = 944):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGASaveImage)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            # packet = TCP_Packet.add_sub_command(packet, channel-1, int, 1)
            ch = (dev_num - 1) * 4 + channel - 1
            packet = TCP_Packet.add_sub_command(packet, ch, int, 1)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s Ch:%d %d %d %d %d) -> PASS' % (
                path, channel, x1, y1, x2, y2))
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%s Ch:%d %d %d %d %d) -> FAIL(%d)' % (
                path, channel, x1, y1, x2, y2, sub_command[0][0]))
                return sub_command[0][0]
        except Exception as e:
            printAK('FPGA SaveImage error occurred: %s' % str(e))
            return 0

    @classmethod
    def FPGASaveVideo(cls, path: str, dev_num: int, channel: int):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGASaveVideo)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            # packet = TCP_Packet.add_sub_command(packet, channel-1, int, 1)
            ch = (dev_num - 1) * 4 + channel - 1
            packet = TCP_Packet.add_sub_command(packet, ch, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%s Ch:%d) -> PASS' % (path, channel))
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + '(%s Ch:%d) -> FAIL(%d)' % (path, channel, sub_command[0][0]))
                return sub_command[0][0]
        except Exception as e:
            printAK('FPGA SaveVideo error occurred: %s' % str(e))
            return 0

    @classmethod
    def FPGACompare(cls, baseImagePath: str, cutLine: float, dev_num: int, channel: int):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGACompare)
            packet = TCP_Packet.add_sub_command(packet, baseImagePath, str)
            packet = TCP_Packet.add_sub_command(packet, cutLine, float)
            # packet = TCP_Packet.add_sub_command(packet, channel-1, int, 1)
            ch = (dev_num - 1) * 4 + channel - 1
            packet = TCP_Packet.add_sub_command(packet, ch, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            # print(''.join('%02x ' % i for i in recv))
            if (sub_command[0][0] == 0x1):
                score = struct.unpack('f', sub_command[1])[0]
                score_round = round(score, 2)
                printAK(sys._getframe(0).f_code.co_name + '(%s %.2f Ch%d) -> PASS(%.2f%%)' % (
                baseImagePath, cutLine, channel, score_round))
                return sub_command[0][0], score_round
            else:
                score = struct.unpack('f', sub_command[1])[0]
                score_round = round(score, 2)
                printAK(sys._getframe(0).f_code.co_name + '(%s %.2f Ch%d) -> FAIL(%.2f%%)' % (
                baseImagePath, cutLine, channel, score_round))
                return sub_command[0][0], score_round
        except Exception as e:
            printAK('FPGA Compare error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def FPGAGetBuffer(cls, dev_num: int, channel: int, x1: int = 0, y1: int = 0, x2: int = 1280, y2: int = 944):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGAGetBuffer)
            # packet = TCP_Packet.add_sub_command(packet, channel-1, int, 1)
            ch = (dev_num - 1) * 4 + channel - 1
            packet = TCP_Packet.add_sub_command(packet, ch, int, 1)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(Ch%d %d %d %d %d) -> PASS' % (channel, x1, y1, x2, y2))
                image_stream = io.BytesIO(recv[10:])
                return sub_command[0][0], Image.open(image_stream)
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0], -1
        except Exception as e:
            printAK('FPGA GetBuffer error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def FPGASetType(cls, device_type: int):
        try:
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGASetType)
            packet = TCP_Packet.add_sub_command(packet, device_type, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(Type%d) -> PASS' % device_type)
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('FPGA FPGASetType error occurred: %s' % str(e))
            return 0

    @classmethod
    def FPGASetUndistort(cls, status):
        try:
            _status = 1 if status else 0
            packet = TCP_Packet.get_base_packet('fpga', CMD_FPGASetUndistort)
            packet = TCP_Packet.add_sub_command(packet, _status, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '(%d) -> PASS' % _status)
                return sub_command[0][0]
            else:
                printAK(sys._getframe(0).f_code.co_name + ' -> FAIL(%d)' % sub_command[0][0])
                return sub_command[0][0]
        except Exception as e:
            printAK('FPGA FPGASetUndistort error occurred: %s' % str(e))
            return 0

    @classmethod
    def CANLog_PeriodCheck(cls, log_path, CAN_CH: int, CAN_ID, CAN_Period, CAN_range):
        try:
            packet = TCP_Packet.get_base_packet('LOG_ANALYZER', CMD_PeriodCheck)
            packet = TCP_Packet.add_sub_command(packet, log_path, str)
            packet = TCP_Packet.add_sub_command(packet, CAN_CH, int, 1)
            packet = TCP_Packet.add_sub_command(packet, CAN_ID, str)
            packet = TCP_Packet.add_sub_command(packet, CAN_Period, float)
            packet = TCP_Packet.add_sub_command(packet, CAN_range, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                currentPercent = sub_command[1][0]
                currentPercent = struct.unpack('f', sub_command[1])[0]
                currentPercent_round = round(currentPercent, 2)
                failCount = int.from_bytes(sub_command[2], byteorder='little', signed=False)
                return currentPercent_round, failCount
            else:
                return -1;
        except Exception as e:
            printAK('CAN log period check error occurred: %s' % str(e))
            return 100, -1

    # CAN_LogPath,CAN_CH,CAN_ID, CAN_Sbit, CAN_Blen, CAN_Min, CAN_Max
    @classmethod
    def CANLog_SignalCheck(cls, log_path, CAN_CH: int, CAN_ID, CAN_Sbit, CAN_Blen, CAN_Min, CAN_Max):
        try:
            packet = TCP_Packet.get_base_packet('LOG_ANALYZER', CMD_SignalCheck)
            packet = TCP_Packet.add_sub_command(packet, log_path, str)
            packet = TCP_Packet.add_sub_command(packet, CAN_CH, int, 1)
            packet = TCP_Packet.add_sub_command(packet, CAN_ID, str)
            packet = TCP_Packet.add_sub_command(packet, CAN_Sbit, int, 1)
            packet = TCP_Packet.add_sub_command(packet, CAN_Blen, int, 1)
            packet = TCP_Packet.add_sub_command(packet, CAN_Min, int, 1)
            packet = TCP_Packet.add_sub_command(packet, CAN_Max, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                currentPercent = sub_command[1][0]
                currentPercent = struct.unpack('f', sub_command[1])[0]
                currentPercent_round = round(currentPercent, 2)
                failCount = int.from_bytes(sub_command[2], byteorder='little', signed=False)
                return currentPercent_round, failCount
            else:
                return -1;
        except Exception as e:
            printAK('CAN log signal check error occurred: %s' % str(e))
            return 100, -1

    @classmethod
    def CANLog_StopCheck(cls):
        try:
            packet = TCP_Packet.get_base_packet('LOG_ANALYZER', CMD_StopCheck)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                currentPercent = sub_command[1][0]
                currentPercent = struct.unpack('f', sub_command[1])[0]
                currentPercent_round = round(currentPercent, 2)
                failCount = int.from_bytes(sub_command[2], byteorder='little', signed=False)
                return currentPercent_round, failCount
            else:
                return -1
        except Exception as e:
            printAK('CAN log check stop error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_ButtonEvent(cls, btn_num, on_off):
        try:
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_BtnEvent)
            packet = TCP_Packet.add_sub_command(packet, btn_num, int, 1)
            packet = TCP_Packet.add_sub_command(packet, on_off, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('TT_ButtonEvent error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_PowerSupply(cls, on_off):
        try:
            printAK('TT Power supply control Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_PowerSupply)
            packet = TCP_Packet.add_sub_command(packet, on_off, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('TT_PowerSupply error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_SetVoltage(cls, voltage):
        try:
            printAK('TT Set voltage Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_SetVoltage)
            voltage_round = round(voltage, 2)
            packet = TCP_Packet.add_sub_command(packet, voltage_round, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('TT_SetVoltage error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_GetVoltage(cls):
        try:
            printAK('TT Get voltage Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_GetVoltage)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                return sub_command[1].decode('utf-8')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return ''
        except Exception as e:
            printAK('TT_GetVoltage error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_GetAmpere(cls):
        try:
            printAK('TT Get ampere Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_GetAmpere)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                return sub_command[1].decode('utf-8')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return ''
        except Exception as e:
            printAK('TT_GetAmpere error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_GetWatt(cls):
        try:
            printAK('TT Get watt Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_GetWatt)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if sub_command[0][0] == 0x01:
                return sub_command[1].decode('utf-8')
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return ''
        except Exception as e:
            printAK('TT_GetWatt error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_StartMeasurement(cls):
        try:
            printAK('TT Measurement Start Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_MeasurementStart)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('TT_StartMeasurement error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_StopMeasurement(cls):
        try:
            printAK('TT Measurement Stop Event')
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_MeasurementStop)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('TT_StopMeasurement error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_SetMeasurementUnit(cls, UnitValue):
        try:
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_MeasurementUnit)
            packet = TCP_Packet.add_sub_command(packet, UnitValue, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('TT_SetMeasurementUnit error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_GetMeasurementData(cls, UnitValue: int):
        try:
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_MeasurementGet)
            packet = TCP_Packet.add_sub_command(packet, UnitValue, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)

            if sub_command[0][0] == 0x01:
                unit = 'A'
                if (UnitValue == 1):
                    unit = 'A'
                elif (UnitValue == 2):
                    unit = '㎃'
                elif (UnitValue == 3):
                    unit = '㎂'

                return sub_command[1].decode('utf-8') + unit
            else:
                printAK('%d -> FAIL' % sub_command[0][0])
                return '', ''
        except Exception as e:
            printAK('TT_GetMeasurementData error occurred: %s' % str(e))
            return 0

    @classmethod
    def TT_StartPWM(cls, ch, onTime, offTime, repeatCnt, lastmode):
        try:
            packet = TCP_Packet.get_base_packet('TAD_TT', CMD_TT_PWM)
            packet = TCP_Packet.add_sub_command(packet, ch, int, 1)
            packet = TCP_Packet.add_sub_command(packet, onTime, int, 1)
            packet = TCP_Packet.add_sub_command(packet, offTime, int, 1)
            packet = TCP_Packet.add_sub_command(packet, repeatCnt, int, 1)
            packet = TCP_Packet.add_sub_command(packet, lastmode, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)

            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')

            return sub_command[0][0]

        except Exception as e:
            printAK('TT_StartPWM error occurred: %s' % str(e))
            return 0

    @classmethod
    def VCConnect(cls, index: int, monikerString: str):
        try:
            packet = TCP_Packet.get_base_packet('VIDEO_CAPTURE', CMD_VCConnect)
            packet = TCP_Packet.add_sub_command(packet, index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, monikerString, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('VCConnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def VCDisconnect(cls, index: int):
        try:
            packet = TCP_Packet.get_base_packet('VIDEO_CAPTURE', CMD_VCDisconnect)
            packet = TCP_Packet.add_sub_command(packet, index, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('VCDisconnect error occurred: %s' % str(e))
            return 0

    @classmethod
    def VCSaveImage(cls, index: int, path: str, x1: int = 0, y1: int = 0, x2: int = 1920, y2: int = 1080):
        try:
            packet = TCP_Packet.get_base_packet('VIDEO_CAPTURE', CMD_VCSaveImage)
            packet = TCP_Packet.add_sub_command(packet, index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            packet = TCP_Packet.add_sub_command(packet, x1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y1, int, 2)
            packet = TCP_Packet.add_sub_command(packet, x2, int, 2)
            packet = TCP_Packet.add_sub_command(packet, y2, int, 2)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('VCSaveImage error occurred: %s' % str(e))
            return 0

    @classmethod
    def VCSaveVideo(cls, index: int, path: str):
        try:
            packet = TCP_Packet.get_base_packet('VIDEO_CAPTURE', CMD_VCSaveVideo)
            packet = TCP_Packet.add_sub_command(packet, index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('VCSaveVideo error occurred: %s' % str(e))
            return 0

    @classmethod
    def VCCompare(cls, index: int, path: str, cutLine: float):
        try:
            packet = TCP_Packet.get_base_packet('VIDEO_CAPTURE', CMD_VCCompare)
            packet = TCP_Packet.add_sub_command(packet, index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, path, str)
            packet = TCP_Packet.add_sub_command(packet, cutLine, float)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            score = int(struct.unpack('f', sub_command[1])[0])
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0], score
        except Exception as e:
            printAK('VCCompare error occurred: %s' % str(e))
            return 0, -1

    @classmethod
    def VCSetRecordingTime(cls, index: int, recordingTime: int):
        try:
            packet = TCP_Packet.get_base_packet('VIDEO_CAPTURE', CMD_VCSetRecordingTime)
            packet = TCP_Packet.add_sub_command(packet, index, int, 1)
            packet = TCP_Packet.add_sub_command(packet, recordingTime, int, 1)
            recv = cls.__send(packet)
            sub_command = TCP_Packet.GetSubCommand(recv)
            if (sub_command[0][0] == 0x1):
                printAK(sys._getframe(0).f_code.co_name + '-> PASS')
            else:
                printAK(sys._getframe(0).f_code.co_name + '-> FAIL')
            return sub_command[0][0]
        except Exception as e:
            printAK('VCSetRecordingTime error occurred: %s' % str(e))
            return 0

