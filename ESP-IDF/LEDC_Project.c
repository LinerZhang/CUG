#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_err.h"
#include "esp_log.h"
#include "esp_check.h"

#include "driver/ledc.h"

static const char *TAG = "siggen";

// 全局可调参数
#define LEDC_MODE          LEDC_LOW_SPEED_MODE // LEDC 的 speed mode: high/low
#define DEFAULT_DUTY_RES   LEDC_TIMER_4_BIT    // 修改为 4 位分辨率
#define TIMER_COUNT        2 // timer的数量
#define CHANNEL_COUNT      4 // 输出波形的通道数

// 设置 timer 的频率
static uint32_t g_timer_freq[TIMER_COUNT] = {
    2000000,  // timer0: 2 MHz
    4000000   // timer1: 4 MHz
};

// 每个通道的配置：GPIO、用哪个 timer、初始 duty
typedef struct {
    int gpio;
    int timer_id;
    int ch_id;
    int duty_percent; // 0-100(%),只能写 k/DEFAULT_DUTY_RES
} sig_channel_cfg_t;

// 自由定义通道
static sig_channel_cfg_t g_channels[CHANNEL_COUNT] = {
    { .gpio = 4,  .timer_id = 0, .ch_id = 0, .duty_percent = 50 }, // CH0：GPIO4, timer0(2MHz)
    { .gpio = 5,  .timer_id = 0, .ch_id = 1, .duty_percent = 25 }, // CH1：GPIO5, timer0(2MHz)
    { .gpio = 6,  .timer_id = 1, .ch_id = 2, .duty_percent = 50 }, // CH2：GPIO6, timer1(4MHz)
    { .gpio = 7,  .timer_id = 1, .ch_id = 3, .duty_percent = 75 }, // CH3：GPIO7, timer1(4MHz)
};

// 用一个全局变量记住当前 duty 分辨率
static ledc_timer_bit_t g_duty_res = DEFAULT_DUTY_RES;

// 把百分比映射到 duty 计数值
static inline uint32_t duty_max(ledc_timer_bit_t res) {
    return (1u << (uint32_t)res) - 1u;
}

static uint32_t duty_from_percent(int percent) {
    if (percent < 0) percent = 0;
    if (percent > 100) percent = 100;
    uint32_t max = duty_max(g_duty_res);
    return (uint32_t)((percent * (int)(max + 1) + 50) / 100);
}

// 初始化 timer
static esp_err_t siggen_init_timers(void) {
    for (int i = 0; i < TIMER_COUNT; i++) {
        ledc_timer_config_t tcfg = {
            .speed_mode       = LEDC_MODE,
            .timer_num        = (ledc_timer_t)i,
            .duty_resolution  = g_duty_res,
            .freq_hz          = g_timer_freq[i],
            .clk_cfg          = LEDC_USE_APB_CLK,  // 固定时钟源
        };
        ESP_RETURN_ON_ERROR(ledc_timer_config(&tcfg), TAG, "timer%d config failed", i);
        
        // 打印实际的频率
        uint32_t real_freq = ledc_get_freq(LEDC_MODE, (ledc_timer_t)i);
        ESP_LOGI(TAG, "Real Timer%d Frequency: %u Hz", i, real_freq);

        ESP_LOGI(TAG, "Timer%d: freq=%u Hz, duty_res=%d-bit", i, (unsigned)g_timer_freq[i], (int)g_duty_res);
    }
    return ESP_OK;
}

// 初始化 channels
static esp_err_t siggen_init_channels(void) {
    for (int i = 0; i < CHANNEL_COUNT; i++) {
        sig_channel_cfg_t *c = &g_channels[i];
        if (c->timer_id < 0 || c->timer_id >= TIMER_COUNT) {
            ESP_LOGE(TAG, "Channel idx %d: invalid timer_id=%d", i, c->timer_id);
            return ESP_ERR_INVALID_ARG;
        }
        if (c->ch_id < 0 || c->ch_id > 15) {
            ESP_LOGE(TAG, "Channel idx %d: invalid ch_id=%d", i, c->ch_id);
            return ESP_ERR_INVALID_ARG;
        }

        ledc_channel_config_t ccfg = {
            .speed_mode     = LEDC_MODE,
            .channel        = (ledc_channel_t)c->ch_id,
            .timer_sel      = (ledc_timer_t)c->timer_id,
            .intr_type      = LEDC_INTR_DISABLE,
            .gpio_num       = c->gpio,
            .duty           = duty_from_percent(c->duty_percent),
            .hpoint         = 0,
        };
        ESP_RETURN_ON_ERROR(ledc_channel_config(&ccfg), TAG, "channel%d config failed", c->ch_id);
        ESP_LOGI(TAG, "CH%d -> GPIO%d, timer%d, duty=%d%% (raw=%u)",
                 c->ch_id, c->gpio, c->timer_id, c->duty_percent,
                 (unsigned)ccfg.duty);
    }
    return ESP_OK;
}

void app_main(void) {
    ESP_ERROR_CHECK(siggen_init_timers());
    ESP_ERROR_CHECK(siggen_init_channels());

    ESP_LOGI(TAG, "Signal generator running. (LEDC)");

    // 主循环不做事，LEDC 硬件照样输出
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
