#if 0
#include<iostream>
#include<thread>//�߳̿�
#include<string.h>
#include<windows.h>//windows������ʹ��system���Ͳ���ͼ�꣬������Ҫ����sleep(ms)������������ͣ�ض�ʱ��
#include<conio.h>//conio�ǿ���̨�ַ������������
#include<stdlib.h>//C
#include<fstream>
#include <stdio.h>
#include<mmsystem.h>//mmsystem�����ý���йصĴ�����ӿ�
#pragma comment(lib,"winmm.lib")
using namespace std;

void map_func(char keyboard_key, char* sound_name) {
	char key[] = { '1','!','2','@','3','4','$','5','%','6','^','7',
				   '8','*','9','(','0','q','Q','w','W','e','E','r',
				   't','T','y','Y','u','i','I','o','O','p','P','a',
				   's','S','d','D','f','g','G','h','H','j','J','k',
				   'l','L','z','Z','x','c','C','v','V','b','B','n',
				   'm' }; //����������Ӧ�İ���(���̰������ޣ�����ʾ61��)
	char key_letter[][3] = { "C","Cs","D","Ds","E","F","Fs","G","Gs","A","As","B" }; //������ĸ����
	char key_num[][2] = { "1","2","3","4","5","6" };  //�������ֲ���

	for (int i = 0; i < sizeof(key); i++) {
		if (keyboard_key == key[i]) {
			int LetterName = (i % 12); //key�е�ÿһ��������Ӧ����ĸ�����֣���ĸ����12��һ�ֻ�
			int NumName = (i / 12);  //key�е�ÿһ��������Ӧ�����ֵ����֣����ֲ���ÿʮ������+1
			char ss_letter[5], ss_num[2]; //�������������飬�����ĸ����������
			strcpy_s(ss_letter, key_letter[LetterName]);
			strcpy_s(ss_num, key_num[NumName]); //��strcpy�������
			strcat_s(ss_letter, ss_num);//��stract�ϲ���ss_letter
			strcpy(sound_name, ss_letter);//���մ����sound_name 
		}
		else {
			continue;
		}
	}
}//�������밴���ó���Ӧ��Ƶ�ļ����ĺ���

int play_sound(char keyboard_key) {
	char sound_name[5] = { 0 }; //����
	char temp_command[127] = { 0 }; //mciSendString������
	if (keyboard_key == ' ') {
		return 0;//�ո���˳�
	}
	else {
		map_func(keyboard_key, sound_name);   //�������ϵļ���Ӧ�ؽ��������
	}
	sprintf_s(temp_command, "open piano\\%s.mp3 alias %s", sound_name, sound_name);
	mciSendString(temp_command, 0, 0, 0); //������.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //����
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //�ر�
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}//���ŵ�����Ƶ

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