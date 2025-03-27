#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

std::mutex print_mutex; // ȫ�ֻ�����

// ͬ����ӡ����
void synchronized_print(const std::string& message, char end = ' ') {
    std::lock_guard<std::mutex> lock(print_mutex); // �Զ������ͽ���
    std::cout << message << end;
}

void play_sound(const std::string& sound_name) {
    for (char note : sound_name) {
        std::string note_str(1, note); // ����һ�����������ַ��� std::string
        synchronized_print(note_str); // ��ȷ�ش��� std::string ����
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int main() {
    std::thread t1(play_sound, "CDE");
    std::thread t2(play_sound, "FGA");

    t1.join();
    t2.join();

    return 0;
}