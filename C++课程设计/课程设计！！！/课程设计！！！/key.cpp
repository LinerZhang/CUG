#if 0
#include<iostream>
#include<thread>//线程库
#include<string.h>
#include<windows.h>//windows是用来使用system语句和插入图标，这里主要用于sleep(ms)，代表计算机暂停特定时间
#include<conio.h>//conio是控制台字符输入输出操作
#include<stdlib.h>//C
#include<fstream>
#include <stdio.h>
#include<mmsystem.h>//mmsystem是与多媒体有关的大多数接口
#pragma comment(lib,"winmm.lib")
using namespace std;

void map_func(char keyboard_key, char* sound_name) {
	char key[] = { '1','!','2','@','3','4','$','5','%','6','^','7',
				   '8','*','9','(','0','q','Q','w','W','e','E','r',
				   't','T','y','Y','u','i','I','o','O','p','P','a',
				   's','S','d','D','f','g','G','h','H','j','J','k',
				   'l','L','z','Z','x','c','C','v','V','b','B','n',
				   'm' }; //所有音名对应的按键(键盘按键有限，仅表示61键)
	char key_letter[][3] = { "C","Cs","D","Ds","E","F","Fs","G","Gs","A","As","B" }; //音名字母部分
	char key_num[][2] = { "1","2","3","4","5","6" };  //音名数字部分

	for (int i = 0; i < sizeof(key); i++) {
		if (keyboard_key == key[i]) {
			int LetterName = (i % 12); //key中的每一个按键对应的字母的名字，字母部分12个一轮回
			int NumName = (i / 12);  //key中的每一个按键对应的数字的名字，数字部分每十二个音+1
			char ss_letter[5], ss_num[2]; //建立两个空数组，存放字母名和数字名
			strcpy_s(ss_letter, key_letter[LetterName]);
			strcpy_s(ss_num, key_num[NumName]); //用strcpy拷贝存放
			strcat_s(ss_letter, ss_num);//用stract合并到ss_letter
			strcpy(sound_name, ss_letter);//最终存放在sound_name 
		}
		else {
			continue;
		}
	}
}//根据输入按键得出对应音频文件名的函数

int play_sound(char keyboard_key) {
	char sound_name[5] = { 0 }; //音名
	char temp_command[127] = { 0 }; //mciSendString的命令
	if (keyboard_key == ' ') {
		return 0;//空格键退出
	}
	else {
		map_func(keyboard_key, sound_name);   //将键盘上的键对应地解码成音名
	}
	sprintf_s(temp_command, "open piano\\%s.mp3 alias %s", sound_name, sound_name);
	mciSendString(temp_command, 0, 0, 0); //打开音名.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //播放
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //关闭
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}//播放单音音频

int main() {
	string look1  = "| | || | | | || || | | | || | | | || || | | | || | | | || || | |";
	string look9  = "| |!||@| | |$||%||^| | |*||(| | |W||E||R| | |Y||U| | |O||P||A| |";
	string look10 = "| |D||F| | |H||J||K| | |Z||X| | |V||B||N| | | || | | | || || | |";
	string look11 = "| |_||_| | |_||_||_| | |_||_| | |_||_||_| | |_||_| | |_||_||_| |";
	string look12 = "|1 |2 |3 |4 |5 |6 |7 |8 |9 |q |w |e |r |t |y |u |i |o |p |a |s |"; 
	string look13 = "|d |f |g |h |j |k |l |z |x |c |v |b |n |m |  |  |  |  |  |  |  |";
	string look14 = "|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|";
	for (int i = 0; i < 8; i++) {
		cout << look1 << endl;
	}
	cout << look9 << endl;
	cout << look10<< endl;
	cout << look11<< endl;
	cout << look12<< endl;
	cout << look13<< endl;
	cout << look14<< endl;
}
#endif