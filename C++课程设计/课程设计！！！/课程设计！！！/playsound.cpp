#if 0
#include <windows.h>
#include <fcntl.h>  
#include <process.h> 
#include <iostream>
#include <unistd.h>
using namespace std;
int hpipe[2];

void setbgm(int b)//主程序调用，输入数字来设置BGM
{
	int bgm = b;
	write(hpipe[1], &bgm, sizeof(int));
}

int main(int argc, char* argv[])
{
	char hstr[20];
	int pid;
	if (argc == 1)//主进程
	{
		//管道初始化
		setvbuf(stdout, NULL, _IONBF, 0);
		if (_pipe(hpipe, 256, O_BINARY) == -1)exit(1);
		itoa(hpipe[0], hstr, 10);
		if ((pid = spawnl(P_NOWAIT, argv[0], argv[0], hstr, NULL)) == -1)exit(1);

		//以下为程序其他部分	
		PlaySound("3.wav", NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);//主进程播放的声音
		setbgm(1);//通知子进程切换1号BGM
		Sleep(5000);
		setbgm(2);//通知子进程切换2号BGM
		Sleep(10000);
		setbgm(-1);//程序结束前调用来关闭子程序
	}
	else//子进程
	{
		system("title BGM");
		int bgm;
		hpipe[0] = atoi(argv[1]);
		while (1)
		{
			if (read(hpipe[0], &bgm, sizeof(int)))//接收消息
			{
				switch (bgm)
				{
					//子程序退出
				case -1:exit(0);
					//1号BGM
				case 1:PlaySound("1.wav", NULL, SND_FILENAME | SND_ASYNC | SND_LOOP); break;
					//2号BGM
				case 2:PlaySound("2.wav", NULL, SND_FILENAME | SND_ASYNC | SND_LOOP); break;
				}
			}
			Sleep(100);//防止CPU占用过高
		}
	}
}
#endif

