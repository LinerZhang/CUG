#if 0
#include<iostream>
#include<thread>//�߳̿�
#include<string.h>
#include<windows.h>//windows������ʹ��system���Ͳ���ͼ�꣬������Ҫ����sleep(ms)������������ͣ�ض�ʱ��
#include<conio.h>//conio�ǿ���̨�ַ������������
#include<stdlib.h>//C
#include<fstream>
#include<mmsystem.h>//mmsystem�����ý���йصĴ�����ӿ�
#pragma comment(lib,"winmm.lib")
using namespace std;
#define kd(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

int play_sound_drum(char keyboard_key) {
	char sound_name[5] = { 0 }; //����
	char temp_command[127] = { 0 }; //mciSendString������
	if (keyboard_key == '1') { strcpy(sound_name, "A2"); }//���������һ���ɹ����ļ������MP3

	else if (keyboard_key == '2') { strcpy(sound_name, "Dong"); }
	else if (keyboard_key == '3') { strcpy(sound_name, "De"); }
	else { cout << "Error" << endl; }
	sprintf_s(temp_command, "open drum\\%s.mp3 alias %s", sound_name, sound_name);
	cout << temp_command << endl;
	mciSendString(temp_command, 0, 0, 0); //������.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //����
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //�ر�
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}

int main() {
	while (1) {
		cout << "11111" << endl;
		char keyboard_key = _getch();
		thread newThread1(play_sound_drum, keyboard_key);//�����߳�
		newThread1.detach();
	}
}
#endif