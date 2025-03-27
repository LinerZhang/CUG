#if 0
#include <windows.h>
#include <fcntl.h>  
#include <process.h> 
#include <iostream>
#include <unistd.h>
using namespace std;
int hpipe[2];

void setbgm(int b)//��������ã���������������BGM
{
	int bgm = b;
	write(hpipe[1], &bgm, sizeof(int));
}

int main(int argc, char* argv[])
{
	char hstr[20];
	int pid;
	if (argc == 1)//������
	{
		//�ܵ���ʼ��
		setvbuf(stdout, NULL, _IONBF, 0);
		if (_pipe(hpipe, 256, O_BINARY) == -1)exit(1);
		itoa(hpipe[0], hstr, 10);
		if ((pid = spawnl(P_NOWAIT, argv[0], argv[0], hstr, NULL)) == -1)exit(1);

		//����Ϊ������������	
		PlaySound("3.wav", NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);//�����̲��ŵ�����
		setbgm(1);//֪ͨ�ӽ����л�1��BGM
		Sleep(5000);
		setbgm(2);//֪ͨ�ӽ����л�2��BGM
		Sleep(10000);
		setbgm(-1);//�������ǰ�������ر��ӳ���
	}
	else//�ӽ���
	{
		system("title BGM");
		int bgm;
		hpipe[0] = atoi(argv[1]);
		while (1)
		{
			if (read(hpipe[0], &bgm, sizeof(int)))//������Ϣ
			{
				switch (bgm)
				{
					//�ӳ����˳�
				case -1:exit(0);
					//1��BGM
				case 1:PlaySound("1.wav", NULL, SND_FILENAME | SND_ASYNC | SND_LOOP); break;
					//2��BGM
				case 2:PlaySound("2.wav", NULL, SND_FILENAME | SND_ASYNC | SND_LOOP); break;
				}
			}
			Sleep(100);//��ֹCPUռ�ù���
		}
	}
}
#endif

