from machine import Pin, SPI
import ssd1306


spi = SPI(0, baudrate=10000000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# display = Display(spi,dc=Pin(4),cs=Pin(5),rst=Pin(6))
# SDA Line connects to SPI-TX == Mosi GP3
# SCL - SPI-RX GP4 == Miso
# CS is GP5

dc = Pin(4)  # data/command
rst = Pin(6)  # reset
cs = Pin(5)  # chip select, some modules do not have a pin for this
display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)
display.text("hi", 15, 15)
display.show()

## Display function prints text commands
def display(text):
    display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)
    display.text(text, 30, 30)
    display.show()
