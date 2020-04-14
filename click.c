#include <iostream>
#include <time.h>
#include <chrono>
#include <thread>
#include <cstring>
#include <Windows.h>

void mouseCoordsToConsole() {
    POINT p;
    GetCursorPos(&p);
    std::cout << "X: " << p.x << " Y: " << p.y << std::endl;
}

// TODO: CLI Arguments
int main() {
    // mouseCoordsToConsole();
    while (1)
    {
        time_t now = time(NULL);
        struct tm* _tm;
        _tm = localtime(&now);

        char hours[3];
        strftime(hours, sizeof(hours), "%H", _tm);

        char minutes[3];
        strftime(minutes, sizeof(minutes), "%M", _tm);

        if (!strcmp(hours, "10") && !strcmp(minutes, "00")) {
            break;
        }

        std::this_thread::sleep_for(std::chrono::seconds(60));
    }
    
    SetCursorPos(1853, 99);
    // I could do it in one function call but oh well...
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);

    return 0;
}