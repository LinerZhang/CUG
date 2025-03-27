#if 1
#include<iostream>
#include<thread>//线程库
#include<string.h>
#include<windows.h>//windows是用来使用system语句
#include<conio.h>//conio是控制台字符输入输出操作
#include<stdlib.h>//C
#include<fstream>
#include <stdio.h>
#include<mmsystem.h>//mmsystem是与多媒体有关的大多数接口
#pragma comment(lib,"winmm.lib")
using namespace std;
#define kd(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

void HideCursor() {
	HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO cursorInfo;
	GetConsoleCursorInfo(hStdOut, &cursorInfo);
	cursorInfo.bVisible = FALSE; // 设置光标不可见
	SetConsoleCursorInfo(hStdOut, &cursorInfo);
}//不显示光标

void ShowCursor() {
	HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO cInfo{};
	GetConsoleCursorInfo(hOutput, &cInfo); //获取现有光标信息
	cInfo.bVisible = TRUE;
	SetConsoleCursorInfo(hOutput, &cInfo);  //重新设置光标信息
}
void position(int x, int y){
	COORD pos = { (short)x,(short)y };
	HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hOut, pos);
	return;
}//定位到指定坐标

void prin(string s, int X, int Y)
{
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFO bInfo;
	GetConsoleScreenBufferInfo(hConsole, &bInfo);
	int y = bInfo.dwMaximumWindowSize.Y, x = bInfo.dwMaximumWindowSize.X;
	position((x - s.size()) / 2 + X, y / 2 + Y);
	cout << s;
}//居中输出

void print_kuang() {
	short start_x = 20, start_y = 5;
	short page_x = 80, page_y = 20;
	position(start_x + page_x - 8, start_y + page_y - 3);
	cout << "<ESC>";
	position(start_x + 3, start_y + 2);
	cout << "<BACK>";
	position(start_x, start_y);
	for (short y = 0; y < page_y; y++) {
		if (y == 0 || y == page_y - 1) {
			position(start_x, start_y + y);
			for (short x = 0; x <= page_x; x++) {
				cout << "=";     //若为第一行或最后一行，则打印page_x个=
			}
		}
		else {
			position(start_x, start_y + y);
			cout << '|';
			position(start_x + page_x, start_y + y);
			cout << '|';      //每行开头和末尾打印|
		}
	}
}//打印边框

void print_pkeys() {
	int ystart = 8;
	position(20 + 1, ystart++);//第八行，start=9
	cout << " _____________________________________________________________________________";
	for (short i = 0; i < 4; i++) {//打印4行
		position(20 + 1, ystart++);
		cout << " |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | |  |";
	}//此时ystart=12
	position(20 + 1, ystart++);
	cout << " |  |!| |@|  |  |$| |%| |^|  |  |*| |(|  |  |Q| |W| |E|  |  |T| |Y|  |  |I|  |";
	for (short i = 0; i < 1; i++) {
		position(20 + 1, ystart++);
		cout << " |  |S| |D|  |  |G| |H| |J|  |  |L| |Z|  |  |C| |V| |B|  |  |M| | |  |  | |  |";
	}
	position(20 + 1, ystart++);
	cout << " |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_|  |";
	for (short i = 0; i < 1; i++) {
		position(20 + 1, ystart++);
		cout << " |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |";
	}
	position(20 + 1, ystart++);
	cout << " | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | q | w | e | r | t | y | u | i | o |";
	position(20 + 1, ystart++);
	cout << " | C1| D1| E1| F1| G1| A1| B1| C2| D2| E2| F2| G2| A2| B2| C3| D3| E3| F3| G3|";
	position(20 + 1, ystart++);
	cout << " | s | d | f | g | h | j | k | l | z | x | c | v | b | n | m |   |   |   |   |";
	position(20 + 1, ystart++);
	cout << " | C4| D4| E4| F4| G4| A4| B4| C5| D5| E5| F5| G5| A5| B5| C6|   |   |   |   |";
	position(20 + 1, ystart++);
	cout << " |___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|";
}

void print_drum() {
	int ystart = 8;
	int xstart = 37;
	position(xstart, ystart++);//第八行，第39列
	cout << "__________  __________  __________  __________";
	position(xstart, ystart++);//第九行
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "|  踏钹  |  |  铙钹  |  | 小军鼓 |  |  脚鼓  |";
	position(xstart, ystart++);
	cout << "|   1    |  |   2    |  |   3    |  |   4    |";
	position(xstart, ystart++);
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "|________|  |________|  |________|  |________|";
	position(xstart, ystart++);//中间空一行
	cout << endl;
	position(xstart, ystart++);
	cout << "__________  __________  __________  __________";
	position(xstart, ystart++);
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "| 嗵嗵鼓 |  |  铃鼓  |  |  沙锤  |  | 康家鼓 |";
	position(xstart, ystart++);
	cout << "|   5    |  |   6    |  |   7    |  |   8    |";
	position(xstart, ystart++);
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "|________|  |________|  |________|  |________|";
}

void print_guitar() {
	int ystart = 10;
	int xstart = 28;
	position(xstart, ystart++);//第10行，第25列
	cout << " ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___ ";
	for (int i = 1; i < 4; i++) {
		position(xstart, ystart++);
		cout << "|   ||   ||   ||   ||   ||   ||   ||   ||   ||   ||   ||   ||   |";
	}
	position(xstart, ystart++);//
	cout << "| 1 || 2 || 3 || 4 || 5 || 6 || 7 || 8 || 9 || q || w || e || r |";
	position(xstart, ystart++);//
	cout << "| A ||Am || B ||Bj ||Bm || C || D ||Dm ||Ej ||Em || F ||Fm || G |";
	for (int i = 1; i < 3; i++) {
		position(xstart, ystart++);
		cout << "|   ||   ||   ||   ||   ||   ||   ||   ||   ||   ||   ||   ||   |";
	}
	position(xstart, ystart++);//
	cout << "|___||___||___||___||___||___||___||___||___||___||___||___||___| ";
}
void cls_kuang() {//第八行到第22行
	position(20 + 1, 8);
	for (short c = 0; c < 80 - 1; c++) {
		printf(" ");
	}
	for (short c = 0; c < 15; c++) {
		position(20 + 1, 8 + c);
		for (short c = 0; c < 80 - 1; c++) {
			printf(" ");
		}
	}
	position(20 + 1, 8);
}//只清除边框内的内容

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
}//根据输入按键得出piano对应音频文件名的函数

int play_sound_piano(char keyboard_key) {
	char sound_name[5] = { 0 }; //音名
	char temp_command[127] = { 0 }; //mciSendString的命令
	if (keyboard_key == '-') {
		strcpy(sound_name, "0");
	}//无声音
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

int play_sound_drum(char keyboard_key) {
	char sound_name[5] = { 0 }; //音名
	char temp_command[127] = { 0 }; //mciSendString的命令
	char key[] = {'0','1','2','3','4','5','6','7','8' };
	char letter[][5] = { "0","1","2","3","4","5","6","7","8" };
	for (int i = 0; i < 9; i++) {
		if (keyboard_key == key[i]) {
			strcpy(sound_name, letter[i]); break;
		}
		else continue;
	}
	sprintf_s(temp_command, "open drum\\%s.mp3 alias %s", sound_name, sound_name);
	mciSendString(temp_command, 0, 0, 0); //打开音名.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //播放
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //关闭
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}
int play_sound_guitar(char keyboard_key) {
	char sound_name[5] = { 0 }; //音名
	char temp_command[127] = { 0 }; //mciSendString的命令
	char key[] = { '0','1','2','3','4','5','6','7','8','9','q','w','e','r' };
	char letter[][5] = { "0","A","Am","B","Bj","Bm","C","D","Dm","Ej","Em","F","Fm","G" };
	for (int i = 0; i < 14; i++) {
		if (keyboard_key == key[i]) {
			strcpy(sound_name, letter[i]); break;
		}
		else continue;
	}
	sprintf_s(temp_command, "open E.L.guitar\\%s.mp3 alias %s", sound_name, sound_name);
	mciSendString(temp_command, 0, 0, 0); //打开音名.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //播放
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //关闭
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}

void Read_puzi(int k, char i, int bmp) {//假设读出来的是i,乐器是k
	if (i == '|') {}//小节分隔
	else {
		if (k == 1) {
			thread newThread1(play_sound_piano, i);//创建线程
			newThread1.detach();
			Sleep(bmp);//相当于四分音符
		}//piano
		else if (k == 2) {
			thread newThread1(play_sound_drum, i);//创建线程
			newThread1.detach();
			Sleep(bmp);
		}//drum
		else if (k == 3) {
			thread newThread1(play_sound_guitar, i);//创建线程
			newThread1.detach();
			Sleep(bmp);
		}
	}
}//读取谱子文件

void Open_puzi(int k, const char* puzi_command, int sudu) {//传入文件地址
	FILE* puzi = fopen(puzi_command, "r");

	if (puzi != NULL) {
		char c = fgetc(puzi);
		while (c != EOF) {
			if (kd(VK_BACK)) {
				break;
			}
			else Read_puzi(k, c, 30000 / sudu);
			c = fgetc(puzi);
		}// 打开文件成功，进行文件读写操作
		fclose(puzi); // 关闭文件
	}
	else {
		printf("Error!");
	}
}//读取键盘播放音符


int Begin_page() {
	HideCursor();//光标不显示
	char line_1[] = "Welcome to my music room !";
	char line_2[] = "START!";
	print_kuang();//打印边框
	prin(line_1, 0, -1);
	prin(line_2, 0, 1);
	if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//退出键直接跳转结束页面
	}
	else if (kd(VK_SPACE)) {
		cls_kuang();
		return 1;
	}
}

int ModeSelect_page() {
	HideCursor();//光标不显示
	char line_1[] = "Please select a mode:";
	char line_2[] = "1.AutoPlay";
	char line_3[] = "2.ManualPlay";
	print_kuang();//打印边框
	prin(line_1, 0, -2);
	prin(line_2, 0, 0);
	prin(line_3, 0, 2);
	Sleep(100);
	if (kd(VK_NUMPAD1) || kd('1')) {
		cls_kuang();
		return 2;//跳转自动播放
	}
	else if (kd(VK_NUMPAD1) || kd('2')) {
		cls_kuang();
		return 3;//跳转手动
	}
	else if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//退出键直接跳转结束页面
	}
	else if (kd(VK_BACK)) {
		cls_kuang();
		return 0;//返回上一个界面
	}
	else return 1;
}

void piano1(int sudu) {
	HideCursor();//光标不显示
	Open_puzi(1, "BigBanana_Piano1.txt", sudu);
}
void piano2(int sudu) {
	HideCursor();//光标不显示
	Open_puzi(1, "BigBanana_Piano2.txt", sudu);
}
void drum1(int sudu) {
	HideCursor();//光标不显示
	Open_puzi(2, "BigBanana_Drum1.txt", sudu);
}
void drum2(int sudu) {
	HideCursor();//光标不显示
	Open_puzi(2, "BigBanana_Drum2.txt", sudu);
}
void drum3(int sudu) {
	HideCursor();//光标不显示
	Open_puzi(2, "BigBanana_Drum3.txt", sudu);
}
void guitar(int sudu) {
	HideCursor();//光标不显示
	Open_puzi(3, "BigBanana_Guitar.txt", sudu);
}
int play_1() {
	print_kuang(); // 打印边框
	int sudu;
	prin("Speed:", 0, 0);
	ShowCursor();
	cin >> sudu;
	HideCursor(); // 光标不显示
	Sleep(500);
	cls_kuang();
	print_kuang();
	prin("<Big Banana> is playing...", 0, 0);
	Sleep(500);
	cls_kuang();
	print_kuang();
	prin("Piano1:33333333|11111111|22222222|33333333|...", 0, -4);
	prin("piano2:o-o-u-uo|p-poo---|p-poppoa|a-------|...", 0, -2);
	prin("drum1 :21111111|11111111|11111111|11110000|...", 0, 0);
	prin("drum2 :40304030|40304030|40304030|40303333|...", 0, 2);
	prin("drum3 :00000077|00000077|00000077|00000077|...", 0, 4);
	std::thread t1(piano1, sudu);
	std::thread t2(piano2, sudu);
	std::thread t3(drum1, sudu);
	std::thread t4(drum2, sudu);
	std::thread t5(drum3, sudu);
	//std::thread t6(guitar, sudu);
	t1.join();
	t2.join();
	t3.join();
	t4.join();
	t5.join();
	//t6.join();
	Sleep(500);//播放结束后自动退出
	cls_kuang(); // 清除屏幕
	return 0;
}

int play_2() {
	char filename[127] = { 0 };//文件名
	char file[127] = { 0 };//完整的文件名（+txt）
	int instrument;
	char showwords[127] = { 0 };
	int sudu;
	cls_kuang();//清屏
	prin("Fliename:", -2, 0);
	ShowCursor();//显示光标
	cin >> filename;//输入文件名
	sprintf_s(file, "%s.txt", filename);//组合成为完整的文件名
	HideCursor();//光标不显示
	Sleep(1000);
	cls_kuang();//清屏
	prin("1.Piano     ", 0, -3);
	prin("2.Drum      ", 0, -1);
	prin("3.E.L.Guitar", 0, 1);
	prin("Instrument:", -1, 3);
	ShowCursor();//显示光标
	cin >> instrument;
	HideCursor();//光标不显示
	Sleep(1000);
	cls_kuang();//清屏
	prin("Speed:", -2, 0);
	ShowCursor();//显示光标
	cin >> sudu;
	HideCursor();//光标不显示
	sprintf(showwords, "<%s> is playing...", filename);
	prin(showwords, 0, 0);
	if (instrument == 1) {
		Open_puzi(1, file, sudu);
		Sleep(500);//播放结束后自动退出
		cls_kuang(); // 清除屏幕
	}
	else if (instrument == 2) {
		Open_puzi(2, file, sudu);
		Sleep(500);//播放结束后自动退出
		cls_kuang(); // 清除屏幕
	}
	else if (instrument == 3) {
		Open_puzi(3, file, sudu);
		Sleep(500);//播放结束后自动退出
		cls_kuang(); // 清除屏幕
	}
	else {
		prin("Error!", 0, 0);
		Sleep(500);
		cls_kuang(); // 清除屏幕
	}
	return 2;
	//这里播放第二首，显示谱子（待完成）
}
int SongSelect_page() {
	HideCursor();//光标不显示
	char line_1[] = "Please select a song to play";
	char line_2[] = "1.Big Banana";
	char line_3[] = "2.local file";//从本地获取录制的谱子
	print_kuang();//打印边框
	prin(line_1, 0, -2);
	prin(line_2, 0, 0);
	prin(line_3, 0, 2);
	Sleep(100);
	if (kd(VK_NUMPAD1) || kd('1')) {
		cls_kuang();
		play_1();
		return 2;//第一首歌
	}
	else if (kd(VK_NUMPAD1) || kd('2')) {
		cls_kuang();
		play_2();
		return 2;//跳转手动
	}
	else if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//退出键直接跳转结束页面
	}
	else if (kd(VK_BACK)) {
		cls_kuang();
		return 1;//返回上一个界面
	}
	else return 2;
}

void Record_piano() {
	char filename[127] = { 0 };//保存的文件名字
	char file[127] = { 0 };//完整的文件名（+txt）
	cls_kuang();//先清屏，选择输入
	prin("Filename:", -2, 0);
	ShowCursor();//显示光标
	cin >> filename;
	HideCursor();//不显示光标
	sprintf_s(file, "%s.txt", filename);//融合成正确的
	Sleep(200);
	cls_kuang();//清屏
	prin("START RECORDING...", 0, 0);//录制提示
	Sleep(1000);
	print_pkeys();//打印琴键
	FILE* writefile = fopen(file, "w");//只写
	if (file == NULL) {
		prin("Error!", 0, 0);
	}
	else {
		while (1) {
			char keyboard_key = _getch();
			thread newThread1(play_sound_piano, keyboard_key);//创建线程
			newThread1.detach();
			fwrite(&keyboard_key, sizeof(keyboard_key), 1, writefile);
			if (kd(VK_SPACE)) {
				break; //再次按空格键结束
			}
		}
	}
	fclose(writefile);//关闭文件
	cls_kuang();//清屏
	prin("END RECORDING...", 0, 0);//结束录制提示
	Sleep(1000);
	cls_kuang();//清屏
	print_pkeys();//打印琴键
}//录制所演奏的内容，录入的每个音都是八分音符，间隔的地方用-

int Piano_play() {
	position(23, 22);
	cout << "<RECORD>";//要在边框前面打印，否则会把<ESC>覆盖
	print_kuang();//打印边框
	print_pkeys();//打印琴键
	Sleep(100);
	while (1) {
		char keyboard_key = _getch();
		thread newThread1(play_sound_piano, keyboard_key);//创建线程
		newThread1.detach();
		if (kd(VK_ESCAPE)) {
			cls_kuang();
			return 4;//退出键直接跳转结束页面
		}
		else if (kd(VK_BACK)) {
			cls_kuang();
			return 3;//返回上一个界面
		}
		else if (kd(VK_SPACE)) {
			Record_piano();
			continue;
		}//空格键开始录制
	}//通过循环不断演奏
}
void Record_drum() {
	char filename[127] = { 0 };//保存的文件名字
	char file[127] = { 0 };//完整的文件名（+txt）
	cls_kuang();//先清屏，选择输入
	prin("Filename:", -2, 0);
	ShowCursor();//显示光标
	cin >> filename;
	HideCursor();//不显示光标
	sprintf_s(file, "%s.txt", filename);//融合成正确的
	Sleep(200);
	cls_kuang();//清屏
	prin("START RECORDING...", 0, 0);//录制提示
	Sleep(1000);
	print_drum();//打印琴键
	FILE* writefile = fopen(file, "w");//只写
	if (file == NULL) {
		prin("Error!", 0, 0);
	}
	else {
		while (1) {
			char keyboard_key = _getch();
			thread newThread1(play_sound_drum, keyboard_key);//创建线程
			newThread1.detach();
			fwrite(&keyboard_key, sizeof(keyboard_key), 1, writefile);
			if (kd(VK_SPACE)) {
				break; //再次按空格键结束
			}
		}
	}
	fclose(writefile);//关闭文件
	cls_kuang();//清屏
	prin("END RECORDING...", 0, 0);//结束录制提示
	Sleep(1000);
	cls_kuang();//清屏
	print_drum();//打印琴键
}
int Drum_play() {
	position(23, 22);
	cout << "<RECORD>";
	print_kuang();//打印边框
	print_drum();
	Sleep(100);
	while (1) {
		char keyboard_key = _getch();
		thread newThread1(play_sound_drum, keyboard_key);//创建线程
		newThread1.detach();
		if (kd(VK_ESCAPE)) {
			cls_kuang();
			return 4;//退出键直接跳转结束页面
		}
		if (kd(VK_BACK)) {
			cls_kuang();
			return 3;//返回上一个界面
		}
		else if (kd(VK_SPACE)) {
			Record_drum();
			continue;
		}
	}//通过循环不断演奏
}
void Record_guitar() {
	char filename[127] = { 0 };//保存的文件名字
	char file[127] = { 0 };//完整的文件名（+txt）
	cls_kuang();//先清屏，选择输入
	prin("Filename:", -2, 0);
	ShowCursor();//显示光标
	cin >> filename;
	HideCursor();//不显示光标
	sprintf_s(file, "%s.txt", filename);//融合成正确的
	Sleep(200);
	cls_kuang();//清屏
	prin("START RECORDING...", 0, 0);//录制提示
	Sleep(1000);
	print_guitar();//打印琴键
	FILE* writefile = fopen(file, "w");//只写
	if (file == NULL) {
		prin("Error!", 0, 0);
	}
	else {
		while (1) {
			char keyboard_key = _getch();
			thread newThread1(play_sound_guitar, keyboard_key);//创建线程
			newThread1.detach();
			fwrite(&keyboard_key, sizeof(keyboard_key), 1, writefile);
			if (kd(VK_SPACE)) {
				break; //再次按空格键结束
			}
		}
	}
	fclose(writefile);//关闭文件
	cls_kuang();//清屏
	prin("END RECORDING...", 0, 0);//结束录制提示
	Sleep(1000);
	cls_kuang();//清屏
	print_drum();//打印琴键
}
int Guitar_play() {
	position(23, 22);
	cout << "<RECORD>";
	print_kuang();//打印边框
	print_guitar();
	Sleep(100);
	while (1) {
		char keyboard_key = _getch();
		thread newThread1(play_sound_guitar, keyboard_key);//创建线程
		newThread1.detach();
		if (kd(VK_ESCAPE)) {
			cls_kuang();
			return 4;//退出键直接跳转结束页面
		}
		if (kd(VK_BACK)) {
			cls_kuang();
			return 3;//返回上一个界面
		}
		else if (kd(VK_SPACE)) {
			Record_guitar();
			continue;
		}
	}//通过循环不断演奏
}
int InstrumentSelect_page() {
	HideCursor();//光标不显示
	char line_1[] = "Please select an instrument to play";
	char line_2[] = "1.Piano     ";
	char line_3[] = "2.Drum      ";
	char line_4[] = "3.E.L.Guitar";
	print_kuang();//打印边框
	prin(line_1, 0, -3);
	prin(line_2, 0, -1);
	prin(line_3, 0, 1);
	prin(line_4, 0, 3);
	Sleep(100);
	if (kd(VK_NUMPAD1) || kd('1')) {
		cls_kuang();
		int trans = Piano_play();
		if (trans == 4)return 4;//piano7
		else return 3;
	}
	else if (kd(VK_NUMPAD1) || kd('2')) {
		cls_kuang();
		int trans = Drum_play();
		if (trans == 4)return 4;
		return 3;//drum
	}
	else if (kd(VK_NUMPAD1) || kd('3')) {
		cls_kuang();
		int trans = Guitar_play();
		if (trans == 4)return 4;
		return 3;//guitar
	}
	else if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//退出键直接跳转结束页面
	}
	else if (kd(VK_BACK)) {
		cls_kuang();
		return 1;//返回上一个界面
	}
	else return 3;
}

void End_page() {
	print_kuang();//打印边框
	char sentences[][127] = { "PROGRAMME DESIGN",\
							  "Liner Zhang from 19G231",\
							  "Thank You for Playing My Game!"\

	};
	for (int i = 0; i < 3; i++) {
		position(60, 10 + i);
		prin(sentences[i], 0, -2 + 2 * i);
	}
	cout << endl;
}


int main() {
	system("mode con cols=120 lines=30");//创建控制面板
	int showpage = 0;
	while (1) {
		if (showpage == 0) {
			showpage = Begin_page();//刚开始默认初始页面
		}//初始页面过后返回循环至选择页面
		else if (showpage == 1) {
			showpage = ModeSelect_page();//自动手动模式选择
		}//根据模式选择跳转3或者4
		else if (showpage == 2) {
			showpage = SongSelect_page();//自动模式下歌曲选择
		}//根据歌曲选择播放
		else if (showpage == 3) {
			showpage = InstrumentSelect_page();//手动模式下乐器选择
		}
		else if (showpage == 4) {
			End_page(); // 这里调用 End_page 并获取返回值
			Sleep(2000);
			system("cls");
			break; //结束页面
		}
	}
	return 0;
}
#endif