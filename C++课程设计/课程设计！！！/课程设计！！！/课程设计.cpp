#if 1
#include<iostream>
#include<thread>//�߳̿�
#include<string.h>
#include<windows.h>//windows������ʹ��system���
#include<conio.h>//conio�ǿ���̨�ַ������������
#include<stdlib.h>//C
#include<fstream>
#include <stdio.h>
#include<mmsystem.h>//mmsystem�����ý���йصĴ�����ӿ�
#pragma comment(lib,"winmm.lib")
using namespace std;
#define kd(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

void HideCursor() {
	HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO cursorInfo;
	GetConsoleCursorInfo(hStdOut, &cursorInfo);
	cursorInfo.bVisible = FALSE; // ���ù�겻�ɼ�
	SetConsoleCursorInfo(hStdOut, &cursorInfo);
}//����ʾ���

void ShowCursor() {
	HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO cInfo{};
	GetConsoleCursorInfo(hOutput, &cInfo); //��ȡ���й����Ϣ
	cInfo.bVisible = TRUE;
	SetConsoleCursorInfo(hOutput, &cInfo);  //�������ù����Ϣ
}
void position(int x, int y){
	COORD pos = { (short)x,(short)y };
	HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hOut, pos);
	return;
}//��λ��ָ������

void prin(string s, int X, int Y)
{
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFO bInfo;
	GetConsoleScreenBufferInfo(hConsole, &bInfo);
	int y = bInfo.dwMaximumWindowSize.Y, x = bInfo.dwMaximumWindowSize.X;
	position((x - s.size()) / 2 + X, y / 2 + Y);
	cout << s;
}//�������

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
				cout << "=";     //��Ϊ��һ�л����һ�У����ӡpage_x��=
			}
		}
		else {
			position(start_x, start_y + y);
			cout << '|';
			position(start_x + page_x, start_y + y);
			cout << '|';      //ÿ�п�ͷ��ĩβ��ӡ|
		}
	}
}//��ӡ�߿�

void print_pkeys() {
	int ystart = 8;
	position(20 + 1, ystart++);//�ڰ��У�start=9
	cout << " _____________________________________________________________________________";
	for (short i = 0; i < 4; i++) {//��ӡ4��
		position(20 + 1, ystart++);
		cout << " |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | |  |";
	}//��ʱystart=12
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
	position(xstart, ystart++);//�ڰ��У���39��
	cout << "__________  __________  __________  __________";
	position(xstart, ystart++);//�ھ���
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "|  ̤��  |  |  ����  |  | С���� |  |  �Ź�  |";
	position(xstart, ystart++);
	cout << "|   1    |  |   2    |  |   3    |  |   4    |";
	position(xstart, ystart++);
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "|________|  |________|  |________|  |________|";
	position(xstart, ystart++);//�м��һ��
	cout << endl;
	position(xstart, ystart++);
	cout << "__________  __________  __________  __________";
	position(xstart, ystart++);
	cout << "|        |  |        |  |        |  |        |";
	position(xstart, ystart++);
	cout << "| ���̹� |  |  ���  |  |  ɳ��  |  | ���ҹ� |";
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
	position(xstart, ystart++);//��10�У���25��
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
void cls_kuang() {//�ڰ��е���22��
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
}//ֻ����߿��ڵ�����

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
}//�������밴���ó�piano��Ӧ��Ƶ�ļ����ĺ���

int play_sound_piano(char keyboard_key) {
	char sound_name[5] = { 0 }; //����
	char temp_command[127] = { 0 }; //mciSendString������
	if (keyboard_key == '-') {
		strcpy(sound_name, "0");
	}//������
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

int play_sound_drum(char keyboard_key) {
	char sound_name[5] = { 0 }; //����
	char temp_command[127] = { 0 }; //mciSendString������
	char key[] = {'0','1','2','3','4','5','6','7','8' };
	char letter[][5] = { "0","1","2","3","4","5","6","7","8" };
	for (int i = 0; i < 9; i++) {
		if (keyboard_key == key[i]) {
			strcpy(sound_name, letter[i]); break;
		}
		else continue;
	}
	sprintf_s(temp_command, "open drum\\%s.mp3 alias %s", sound_name, sound_name);
	mciSendString(temp_command, 0, 0, 0); //������.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //����
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //�ر�
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}
int play_sound_guitar(char keyboard_key) {
	char sound_name[5] = { 0 }; //����
	char temp_command[127] = { 0 }; //mciSendString������
	char key[] = { '0','1','2','3','4','5','6','7','8','9','q','w','e','r' };
	char letter[][5] = { "0","A","Am","B","Bj","Bm","C","D","Dm","Ej","Em","F","Fm","G" };
	for (int i = 0; i < 14; i++) {
		if (keyboard_key == key[i]) {
			strcpy(sound_name, letter[i]); break;
		}
		else continue;
	}
	sprintf_s(temp_command, "open E.L.guitar\\%s.mp3 alias %s", sound_name, sound_name);
	mciSendString(temp_command, 0, 0, 0); //������.mp3
	sprintf_s(temp_command, "play %s  ", sound_name);
	mciSendString(temp_command, 0, 0, 0);    //����
	Sleep(1000);//
	sprintf_s(temp_command, "close %s", sound_name);   //�ر�
	mciSendString(temp_command, 0, 0, 0);
	return 1;
}

void Read_puzi(int k, char i, int bmp) {//�������������i,������k
	if (i == '|') {}//С�ڷָ�
	else {
		if (k == 1) {
			thread newThread1(play_sound_piano, i);//�����߳�
			newThread1.detach();
			Sleep(bmp);//�൱���ķ�����
		}//piano
		else if (k == 2) {
			thread newThread1(play_sound_drum, i);//�����߳�
			newThread1.detach();
			Sleep(bmp);
		}//drum
		else if (k == 3) {
			thread newThread1(play_sound_guitar, i);//�����߳�
			newThread1.detach();
			Sleep(bmp);
		}
	}
}//��ȡ�����ļ�

void Open_puzi(int k, const char* puzi_command, int sudu) {//�����ļ���ַ
	FILE* puzi = fopen(puzi_command, "r");

	if (puzi != NULL) {
		char c = fgetc(puzi);
		while (c != EOF) {
			if (kd(VK_BACK)) {
				break;
			}
			else Read_puzi(k, c, 30000 / sudu);
			c = fgetc(puzi);
		}// ���ļ��ɹ��������ļ���д����
		fclose(puzi); // �ر��ļ�
	}
	else {
		printf("Error!");
	}
}//��ȡ���̲�������


int Begin_page() {
	HideCursor();//��겻��ʾ
	char line_1[] = "Welcome to my music room !";
	char line_2[] = "START!";
	print_kuang();//��ӡ�߿�
	prin(line_1, 0, -1);
	prin(line_2, 0, 1);
	if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//�˳���ֱ����ת����ҳ��
	}
	else if (kd(VK_SPACE)) {
		cls_kuang();
		return 1;
	}
}

int ModeSelect_page() {
	HideCursor();//��겻��ʾ
	char line_1[] = "Please select a mode:";
	char line_2[] = "1.AutoPlay";
	char line_3[] = "2.ManualPlay";
	print_kuang();//��ӡ�߿�
	prin(line_1, 0, -2);
	prin(line_2, 0, 0);
	prin(line_3, 0, 2);
	Sleep(100);
	if (kd(VK_NUMPAD1) || kd('1')) {
		cls_kuang();
		return 2;//��ת�Զ�����
	}
	else if (kd(VK_NUMPAD1) || kd('2')) {
		cls_kuang();
		return 3;//��ת�ֶ�
	}
	else if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//�˳���ֱ����ת����ҳ��
	}
	else if (kd(VK_BACK)) {
		cls_kuang();
		return 0;//������һ������
	}
	else return 1;
}

void piano1(int sudu) {
	HideCursor();//��겻��ʾ
	Open_puzi(1, "BigBanana_Piano1.txt", sudu);
}
void piano2(int sudu) {
	HideCursor();//��겻��ʾ
	Open_puzi(1, "BigBanana_Piano2.txt", sudu);
}
void drum1(int sudu) {
	HideCursor();//��겻��ʾ
	Open_puzi(2, "BigBanana_Drum1.txt", sudu);
}
void drum2(int sudu) {
	HideCursor();//��겻��ʾ
	Open_puzi(2, "BigBanana_Drum2.txt", sudu);
}
void drum3(int sudu) {
	HideCursor();//��겻��ʾ
	Open_puzi(2, "BigBanana_Drum3.txt", sudu);
}
void guitar(int sudu) {
	HideCursor();//��겻��ʾ
	Open_puzi(3, "BigBanana_Guitar.txt", sudu);
}
int play_1() {
	print_kuang(); // ��ӡ�߿�
	int sudu;
	prin("Speed:", 0, 0);
	ShowCursor();
	cin >> sudu;
	HideCursor(); // ��겻��ʾ
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
	Sleep(500);//���Ž������Զ��˳�
	cls_kuang(); // �����Ļ
	return 0;
}

int play_2() {
	char filename[127] = { 0 };//�ļ���
	char file[127] = { 0 };//�������ļ�����+txt��
	int instrument;
	char showwords[127] = { 0 };
	int sudu;
	cls_kuang();//����
	prin("Fliename:", -2, 0);
	ShowCursor();//��ʾ���
	cin >> filename;//�����ļ���
	sprintf_s(file, "%s.txt", filename);//��ϳ�Ϊ�������ļ���
	HideCursor();//��겻��ʾ
	Sleep(1000);
	cls_kuang();//����
	prin("1.Piano     ", 0, -3);
	prin("2.Drum      ", 0, -1);
	prin("3.E.L.Guitar", 0, 1);
	prin("Instrument:", -1, 3);
	ShowCursor();//��ʾ���
	cin >> instrument;
	HideCursor();//��겻��ʾ
	Sleep(1000);
	cls_kuang();//����
	prin("Speed:", -2, 0);
	ShowCursor();//��ʾ���
	cin >> sudu;
	HideCursor();//��겻��ʾ
	sprintf(showwords, "<%s> is playing...", filename);
	prin(showwords, 0, 0);
	if (instrument == 1) {
		Open_puzi(1, file, sudu);
		Sleep(500);//���Ž������Զ��˳�
		cls_kuang(); // �����Ļ
	}
	else if (instrument == 2) {
		Open_puzi(2, file, sudu);
		Sleep(500);//���Ž������Զ��˳�
		cls_kuang(); // �����Ļ
	}
	else if (instrument == 3) {
		Open_puzi(3, file, sudu);
		Sleep(500);//���Ž������Զ��˳�
		cls_kuang(); // �����Ļ
	}
	else {
		prin("Error!", 0, 0);
		Sleep(500);
		cls_kuang(); // �����Ļ
	}
	return 2;
	//���ﲥ�ŵڶ��ף���ʾ���ӣ�����ɣ�
}
int SongSelect_page() {
	HideCursor();//��겻��ʾ
	char line_1[] = "Please select a song to play";
	char line_2[] = "1.Big Banana";
	char line_3[] = "2.local file";//�ӱ��ػ�ȡ¼�Ƶ�����
	print_kuang();//��ӡ�߿�
	prin(line_1, 0, -2);
	prin(line_2, 0, 0);
	prin(line_3, 0, 2);
	Sleep(100);
	if (kd(VK_NUMPAD1) || kd('1')) {
		cls_kuang();
		play_1();
		return 2;//��һ�׸�
	}
	else if (kd(VK_NUMPAD1) || kd('2')) {
		cls_kuang();
		play_2();
		return 2;//��ת�ֶ�
	}
	else if (kd(VK_ESCAPE)) {
		cls_kuang();
		return 4;//�˳���ֱ����ת����ҳ��
	}
	else if (kd(VK_BACK)) {
		cls_kuang();
		return 1;//������һ������
	}
	else return 2;
}

void Record_piano() {
	char filename[127] = { 0 };//������ļ�����
	char file[127] = { 0 };//�������ļ�����+txt��
	cls_kuang();//��������ѡ������
	prin("Filename:", -2, 0);
	ShowCursor();//��ʾ���
	cin >> filename;
	HideCursor();//����ʾ���
	sprintf_s(file, "%s.txt", filename);//�ںϳ���ȷ��
	Sleep(200);
	cls_kuang();//����
	prin("START RECORDING...", 0, 0);//¼����ʾ
	Sleep(1000);
	print_pkeys();//��ӡ�ټ�
	FILE* writefile = fopen(file, "w");//ֻд
	if (file == NULL) {
		prin("Error!", 0, 0);
	}
	else {
		while (1) {
			char keyboard_key = _getch();
			thread newThread1(play_sound_piano, keyboard_key);//�����߳�
			newThread1.detach();
			fwrite(&keyboard_key, sizeof(keyboard_key), 1, writefile);
			if (kd(VK_SPACE)) {
				break; //�ٴΰ��ո������
			}
		}
	}
	fclose(writefile);//�ر��ļ�
	cls_kuang();//����
	prin("END RECORDING...", 0, 0);//����¼����ʾ
	Sleep(1000);
	cls_kuang();//����
	print_pkeys();//��ӡ�ټ�
}//¼������������ݣ�¼���ÿ�������ǰ˷�����������ĵط���-

int Piano_play() {
	position(23, 22);
	cout << "<RECORD>";//Ҫ�ڱ߿�ǰ���ӡ��������<ESC>����
	print_kuang();//��ӡ�߿�
	print_pkeys();//��ӡ�ټ�
	Sleep(100);
	while (1) {
		char keyboard_key = _getch();
		thread newThread1(play_sound_piano, keyboard_key);//�����߳�
		newThread1.detach();
		if (kd(VK_ESCAPE)) {
			cls_kuang();
			return 4;//�˳���ֱ����ת����ҳ��
		}
		else if (kd(VK_BACK)) {
			cls_kuang();
			return 3;//������һ������
		}
		else if (kd(VK_SPACE)) {
			Record_piano();
			continue;
		}//�ո����ʼ¼��
	}//ͨ��ѭ����������
}
void Record_drum() {
	char filename[127] = { 0 };//������ļ�����
	char file[127] = { 0 };//�������ļ�����+txt��
	cls_kuang();//��������ѡ������
	prin("Filename:", -2, 0);
	ShowCursor();//��ʾ���
	cin >> filename;
	HideCursor();//����ʾ���
	sprintf_s(file, "%s.txt", filename);//�ںϳ���ȷ��
	Sleep(200);
	cls_kuang();//����
	prin("START RECORDING...", 0, 0);//¼����ʾ
	Sleep(1000);
	print_drum();//��ӡ�ټ�
	FILE* writefile = fopen(file, "w");//ֻд
	if (file == NULL) {
		prin("Error!", 0, 0);
	}
	else {
		while (1) {
			char keyboard_key = _getch();
			thread newThread1(play_sound_drum, keyboard_key);//�����߳�
			newThread1.detach();
			fwrite(&keyboard_key, sizeof(keyboard_key), 1, writefile);
			if (kd(VK_SPACE)) {
				break; //�ٴΰ��ո������
			}
		}
	}
	fclose(writefile);//�ر��ļ�
	cls_kuang();//����
	prin("END RECORDING...", 0, 0);//����¼����ʾ
	Sleep(1000);
	cls_kuang();//����
	print_drum();//��ӡ�ټ�
}
int Drum_play() {
	position(23, 22);
	cout << "<RECORD>";
	print_kuang();//��ӡ�߿�
	print_drum();
	Sleep(100);
	while (1) {
		char keyboard_key = _getch();
		thread newThread1(play_sound_drum, keyboard_key);//�����߳�
		newThread1.detach();
		if (kd(VK_ESCAPE)) {
			cls_kuang();
			return 4;//�˳���ֱ����ת����ҳ��
		}
		if (kd(VK_BACK)) {
			cls_kuang();
			return 3;//������һ������
		}
		else if (kd(VK_SPACE)) {
			Record_drum();
			continue;
		}
	}//ͨ��ѭ����������
}
void Record_guitar() {
	char filename[127] = { 0 };//������ļ�����
	char file[127] = { 0 };//�������ļ�����+txt��
	cls_kuang();//��������ѡ������
	prin("Filename:", -2, 0);
	ShowCursor();//��ʾ���
	cin >> filename;
	HideCursor();//����ʾ���
	sprintf_s(file, "%s.txt", filename);//�ںϳ���ȷ��
	Sleep(200);
	cls_kuang();//����
	prin("START RECORDING...", 0, 0);//¼����ʾ
	Sleep(1000);
	print_guitar();//��ӡ�ټ�
	FILE* writefile = fopen(file, "w");//ֻд
	if (file == NULL) {
		prin("Error!", 0, 0);
	}
	else {
		while (1) {
			char keyboard_key = _getch();
			thread newThread1(play_sound_guitar, keyboard_key);//�����߳�
			newThread1.detach();
			fwrite(&keyboard_key, sizeof(keyboard_key), 1, writefile);
			if (kd(VK_SPACE)) {
				break; //�ٴΰ��ո������
			}
		}
	}
	fclose(writefile);//�ر��ļ�
	cls_kuang();//����
	prin("END RECORDING...", 0, 0);//����¼����ʾ
	Sleep(1000);
	cls_kuang();//����
	print_drum();//��ӡ�ټ�
}
int Guitar_play() {
	position(23, 22);
	cout << "<RECORD>";
	print_kuang();//��ӡ�߿�
	print_guitar();
	Sleep(100);
	while (1) {
		char keyboard_key = _getch();
		thread newThread1(play_sound_guitar, keyboard_key);//�����߳�
		newThread1.detach();
		if (kd(VK_ESCAPE)) {
			cls_kuang();
			return 4;//�˳���ֱ����ת����ҳ��
		}
		if (kd(VK_BACK)) {
			cls_kuang();
			return 3;//������һ������
		}
		else if (kd(VK_SPACE)) {
			Record_guitar();
			continue;
		}
	}//ͨ��ѭ����������
}
int InstrumentSelect_page() {
	HideCursor();//��겻��ʾ
	char line_1[] = "Please select an instrument to play";
	char line_2[] = "1.Piano     ";
	char line_3[] = "2.Drum      ";
	char line_4[] = "3.E.L.Guitar";
	print_kuang();//��ӡ�߿�
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
		return 4;//�˳���ֱ����ת����ҳ��
	}
	else if (kd(VK_BACK)) {
		cls_kuang();
		return 1;//������һ������
	}
	else return 3;
}

void End_page() {
	print_kuang();//��ӡ�߿�
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
	system("mode con cols=120 lines=30");//�����������
	int showpage = 0;
	while (1) {
		if (showpage == 0) {
			showpage = Begin_page();//�տ�ʼĬ�ϳ�ʼҳ��
		}//��ʼҳ����󷵻�ѭ����ѡ��ҳ��
		else if (showpage == 1) {
			showpage = ModeSelect_page();//�Զ��ֶ�ģʽѡ��
		}//����ģʽѡ����ת3����4
		else if (showpage == 2) {
			showpage = SongSelect_page();//�Զ�ģʽ�¸���ѡ��
		}//���ݸ���ѡ�񲥷�
		else if (showpage == 3) {
			showpage = InstrumentSelect_page();//�ֶ�ģʽ������ѡ��
		}
		else if (showpage == 4) {
			End_page(); // ������� End_page ����ȡ����ֵ
			Sleep(2000);
			system("cls");
			break; //����ҳ��
		}
	}
	return 0;
}
#endif