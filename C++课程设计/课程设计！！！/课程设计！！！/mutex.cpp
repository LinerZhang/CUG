#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

std::mutex print_mutex; // 全局互斥锁

// 同步打印函数
void synchronized_print(const std::string& message, char end = ' ') {
    std::lock_guard<std::mutex> lock(print_mutex); // 自动加锁和解锁
    std::cout << message << end;
}

void play_sound(const std::string& sound_name) {
    for (char note : sound_name) {
        std::string note_str(1, note); // 创建一个包含单个字符的 std::string
        synchronized_print(note_str); // 正确地传递 std::string 对象
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