#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/rmt.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_err.h"

#define GPIO_OUTPUT_PIN1     4
#define GPIO_OUTPUT_PIN2     5

#define RMT_TX_CHANNEL1      RMT_CHANNEL_0
#define RMT_TX_CHANNEL2      RMT_CHANNEL_1

#define TARGET_HZ            2000000

// APB 80MHz 
#define RMT_SRC_HZ           80000000
#define RMT_CLK_DIV          1

static const char *TAG = "RMT_2MHz";

//初始化
static void rmt_tx_init_one(rmt_channel_t ch, gpio_num_t gpio)
{
    rmt_config_t cfg = {
        .rmt_mode = RMT_MODE_TX,
        .channel = ch,
        .gpio_num = gpio,
        .clk_div = RMT_CLK_DIV,
        .mem_block_num = 1,
        .tx_config = {
            .loop_en = true,//循环输出
            .carrier_en = false,
            .idle_output_en = true,
            .idle_level = RMT_IDLE_LEVEL_LOW,
        },
    };

    ESP_ERROR_CHECK(rmt_config(&cfg));

    //APB 作为 RMT 源时钟
    ESP_ERROR_CHECK(rmt_set_source_clk(ch, RMT_BASECLK_APB));

    ESP_ERROR_CHECK(rmt_driver_install(ch, 0, 0));
    ESP_ERROR_CHECK(rmt_set_tx_loop_mode(ch, true));
}

void app_main(void)
{
    rmt_tx_init_one(RMT_TX_CHANNEL1, GPIO_OUTPUT_PIN1);
    rmt_tx_init_one(RMT_TX_CHANNEL2, GPIO_OUTPUT_PIN2);

    //half_period_ticks = tick_hz / (2 * TARGET_HZ)
    //tick_hz = RMT_SRC_HZ / RMT_CLK_DIV
    const uint32_t tick_hz = (RMT_SRC_HZ / RMT_CLK_DIV);
    const uint32_t half_ticks = (tick_hz / (TARGET_HZ * 2));

    //half_ticks = 80000000 / (2*2000000) = 20 ticks，250ns
    if (half_ticks == 0 || half_ticks > 32767) {
        ESP_LOGE(TAG, "half_ticks out of range: %u (tick_hz=%u)", (unsigned)half_ticks, (unsigned)tick_hz);
        return;
    }

    rmt_item32_t item = {
        .level0 = 1,
        .duration0 = half_ticks,
        .level1 = 0,
        .duration1 = half_ticks,
    };

    ESP_ERROR_CHECK(rmt_write_items(RMT_TX_CHANNEL1, &item, 1, false));
    ESP_ERROR_CHECK(rmt_write_items(RMT_TX_CHANNEL2, &item, 1, false));

    ESP_LOGI(TAG, "Continuous %d Hz started on GPIO%d/GPIO%d. (tick_hz=%u, half_ticks=%u)",
             TARGET_HZ, GPIO_OUTPUT_PIN1, GPIO_OUTPUT_PIN2,
             (unsigned)tick_hz, (unsigned)half_ticks);

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
