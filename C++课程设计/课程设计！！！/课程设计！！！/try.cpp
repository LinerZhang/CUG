#if 0
#include<iostream>
#include<thread>//线程库
#include<string.h>
#include<windows.h>//windows是用来使用system语句和插入图标，这里主要用于sleep(ms)，代表计算机暂停特定时间
#include<conio.h>//conio是控制台字符输入输出操作
#include<stdlib.h>//C
#include<fstream>
#include<mmsystem.h>//mmsystem是与多媒体有关的大多数接口
#pragma comment(lib,"winmm.lib")
using namespace std;
#define kd(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

int play_sound_drum(char keyboard_key) {
	char sound_name[5] = { 0 }; //音名
	char temp_command[127] = { 0 }; //mciSendString的命令
	if (keyboard_key == '1') { strcpy(sound_name, "A2"); }//这里放了另一个成功的文件夹里的MP3

	else if (keyboard_key == '2') { strcpy(sound_name, "Dong"); }
	else if (keyboard_key == '3') { strcpy(sound_name, "De"); }
	else { cout << "Error" << endl; }
	sprintf_s(temp_command, "open drum\\%s.mp3 alias %s", sound_name, sound_name);
	cout << temp_command << endl;
	mciSendString(temp_command, 0, 0, 0); //打开音名.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //播放
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //关闭
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}

int main() {
	while (1) {
		cout << "11111" << endl;
		char keyboard_key = _getch();
		thread newThread1(play_sound_drum, keyboard_key);//创建线程
		newThread1.detach();
	}
}
#endif