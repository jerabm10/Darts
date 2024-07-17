#include <iostream>
#include <fstream>
#include <cstring>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>

#define SPI_DEVICE "/dev/spidev0.0"
#define SPI_MODE SPI_MODE_0
#define SPI_BITS_PER_WORD 8
#define SPI_SPEED 500000 // Speed in Hz (500 kHz in this case)

int main() {
    int spi_fd = open(SPI_DEVICE, O_RDWR);
    if (spi_fd < 0) {
        std::cerr << "Error opening SPI device: " << strerror(errno) << std::endl;
        return 1;
    }

    // Set SPI mode
    if (ioctl(spi_fd, SPI_IOC_WR_MODE, &SPI_MODE) == -1) {
        std::cerr << "Failed to set SPI mode: " << strerror(errno) << std::endl;
        close(spi_fd);
        return 1;
    }

    // Set bits per word
    if (ioctl(spi_fd, SPI_IOC_WR_BITS_PER_WORD, &SPI_BITS_PER_WORD) == -1) {
        std::cerr << "Failed to set bits per word: " << strerror(errno) << std::endl;
        close(spi_fd);
        return 1;
    }

    // Set max speed
    if (ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &SPI_SPEED) == -1) {
        std::cerr << "Failed to set max speed: " << strerror(errno) << std::endl;
        close(spi_fd);
        return 1;
    }

    unsigned char data[] = {0x01, 0x02, 0x03, 0x04}; // Example data to send
    struct spi_ioc_transfer spi_transfer;
    memset(&spi_transfer, 0, sizeof(spi_transfer));

    spi_transfer.tx_buf = reinterpret_cast<__u64>(data);
    spi_transfer.rx_buf = reinterpret_cast<__u64>(data);
    spi_transfer.len = sizeof(data);
    spi_transfer.speed_hz = SPI_SPEED;
    spi_transfer.bits_per_word = SPI_BITS_PER_WORD;

    if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &spi_transfer) == -1) {
        std::cerr << "Failed to transfer SPI data: " << strerror(errno) << std::endl;
        close(spi_fd);
        return 1;
    }

    std::cout << "Received data: ";
    for (int i = 0; i < sizeof(data); i++) {
        std::cout << "0x" << std::hex << static_cast<int>(data[i]) << " ";
    }
    std::cout << std::endl;

    close(spi_fd);
    return 0;
}
