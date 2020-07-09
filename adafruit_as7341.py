# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_as7341`
================================================================================

CircuitPython library for use with the Adafruit AS7341 breakout


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* `Adafruit AS7341 Breakout <https://www.adafruit.com/products/45XX>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_AS7341.git"
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device

# from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct, Struct
# from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_register.i2c_bits import ROBits

# pylint: disable=bad-whitespace
_AS7341_DEVICE_ID = const(0b001001)  # Correct content of WHO_AM_I register
_AS7341_I2CADDR_DEFAULT = const(0x39)  # AS7341 default i2c address
_AS7341_CHIP_ID = const(0x09)  # AS7341 default device id from WHOAMI
_AS7341_WHOAMI = const(0x92)  # Chip ID register
_AS7341_CONFIG = const(0x70)  # Enables LED control and sets light sensing mode
_AS7341_GPIO = const(0x73)  # Connects photo diode to GPIO or INT pins
_AS7341_LED = const(0x74)  # LED Register; Enables and sets current limit
_AS7341_ENABLE = const(
    0x80
)  # Main enable register. Controls SMUX, Flicker Detection,Spectral and Power
_AS7341_ATIME = const(0x81)  # Sets ADC integration step count
_AS7341_SP_LOW_TH_L = const(0x84)  # Spectral measurement Low Threshold low byte
_AS7341_SP_LOW_TH_H = const(0x85)  # 0 Spectral measurement Low Threshold high byte
_AS7341_SP_HIGH_TH_L = const(0x86)  # Spectral measurement High Threshold low byte
_AS7341_SP_HIGH_TH_H = const(0x87)  # Spectral measurement High Threshold low byte
_AS7341_STATUS = const(
    0x93
)  # Interrupt status registers. Indicates the occourance of an interrupt
_AS7341_CH0_DATA_L = const(0x95)  # ADC Channel 0 Data
_AS7341_CH0_DATA_H = const(0x96)  # ADC Channel 0 Data
_AS7341_CH1_DATA_L = const(0x97)  # ADC Channel 1 Data
_AS7341_CH1_DATA_H = const(0x98)  # ADC Channel 1 Data
_AS7341_CH2_DATA_L = const(0x99)  # ADC Channel 2 Data
_AS7341_CH2_DATA_H = const(0x9A)  # ADC Channel 2 Data
_AS7341_CH3_DATA_L = const(0x9B)  # ADC Channel 3 Data
_AS7341_CH3_DATA_H = const(0x9C)  # ADC Channel 3 Data
_AS7341_CH4_DATA_L = const(0x9D)  # ADC Channel 4 Data
_AS7341_CH4_DATA_H = const(0x9E)  # ADC Channel 4 Data
_AS7341_CH5_DATA_L = const(0x9F)  # ADC Channel 5 Data
_AS7341_CH5_DATA_H = const(0xA0)  # ADC Channel 5 Data
_AS7341_STATUS2 = const(0xA3)  # Measurement status flags; saturation, validity
_AS7341_STATUS3 = const(0xA4)  # Spectral interrupt source, high or low threshold
_AS7341_CFG0 = const(
    0xA9
)  # Sets Low power mode, Register bank, and Trigger lengthening
_AS7341_CFG1 = const(0xAA)  # Controls ADC Gain
_AS7341_CFG9 = const(
    0xB2
)  # Enables flicker detection and smux command completion system
_AS7341_CFG12 = const(
    0xB5
)  # Spectral threshold channel for interrupts, persistence and auto-gain
_AS7341_PERS = const(
    0xBD
)  # Number of measurement cycles outside thresholds to trigger an interrupt
_AS7341_GPIO2 = const(
    0xBE
)  # GPIO Settings and status: polarity, direction, sets output, reads
_AS7341_ASTEP_L = const(0xCA)  # Integration step size ow byte
_AS7341_ASTEP_H = const(0xCB)  # Integration step size high byte
_AS7341_FD_TIME1 = const(0xD8)  # Flicker detection integration time low byte
_AS7341_FD_TIME2 = const(0xDA)  # Flicker detection gain and high nibble
_AS7341_FD_STATUS = const(
    0xDB
)  # Flicker detection status; measurement valid, saturation, flicker
_AS7341_INTENAB = const(0xF9)  # Enables individual interrupt types
_AS7341_CONTROL = const(0xFA)  # Auto-zero, fifo clear, clear SAI active

# class CV:
#     """struct helper"""

#     @classmethod
#     def add_values(cls, value_tuples):
#         """Add CV values to the class"""
#         cls.string = {}
#         cls.lsb = {}

#         for value_tuple in value_tuples:
#             name, value, string, lsb = value_tuple
#             setattr(cls, name, value)
#             cls.string[value] = string
#             cls.lsb[value] = lsb

#     @classmethod
#     def is_valid(cls, value):
#         """Validate that a given value is a member"""
#         return value in cls.string


# class AccelRange(CV):
#     """Options for ``accelerometer_range``"""
#     pass  # pylint: disable=unnecessary-pass
# AccelRange.add_values(
#   (
#     ("FREQ_196_6HZ_3DB", 0, 196.6, None),
#     ("FREQ_151_8HZ_3DB", 1, 151.8, None),
#     ("FREQ_119_5HZ_3DB", 2, 119.5, None)
#   )

# )


class AS7341:  # pylint:disable=too-many-instance-attributes
    """Library for the AS7341 Sensor


        :param ~busio.I2C i2c_bus: The I2C bus the AS7341 is connected to.
        :param address: The I2C address of the sensor

    """

    _device_id = ROBits(6, _AS7341_WHOAMI, 2)

    def __init__(self, i2c_bus, address=_AS7341_I2CADDR_DEFAULT):

        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        if not self._device_id in [_AS7341_DEVICE_ID]:
            raise RuntimeError("Failed to find an AS7341 sensor - check your wiring!")
        self.reset()
        self.initialize()
        self._buffer = bytearray(2)

    def initialize(self):
        """Configure the sensors with the default settings. For use after calling `reset()`"""

        # self._power_enable = True

    def reset(self):
        """Resets the internal registers and restores the default settings"""
        pass

    def _write_register(self, addr, data):

        self._buffer[0] = addr
        self._buffer[1] = data

        with self.i2c_device as i2c:
            i2c.write(self._buffer)


# #ifndef _ADAFRUIT_AS7341_H
# __ADAFRUIT_AS7341_H = const(
# ) # #include "Arduino.h"
# #include <Adafruit_BusIO_Register.h>
# #include <Adafruit_I2CDevice.h>
# #include <Adafruit_Sensor.h>
# #include <Wire.h>
# _AS7341_I2CADDR_DEFAULT = const(0x39) # AS7341 default i2c address
# _AS7341_CHIP_ID = const(0x09) # AS7341 default device id from WHOAMI

# _AS7341_WHOAMI = const(0x92) # Chip ID register


# _AS7341_CONFIG = const(0x70) # Enables LED control and sets light sensing mode


# _AS7341_GPIO = const(0x73) # Connects photo diode to GPIO or INT pins
# _AS7341_LED = const(0x74) # LED Register; Enables and sets current limit
# _AS7341_ENABLE = const(                                                         \) #
#   0x80 Main enable register. Controls SMUX, Flicker Detection, Spectral
# Measurements and Power
# _AS7341_ATIME = const(0x81) # Sets ADC integration step count

# _AS7341_SP_LOW_TH_L = const(0x84) # Spectral measurement Low Threshold low byte
# _AS7341_SP_LOW_TH_H = const(                                                    \) #
#   0x85 Spectral measurement Low Threshold high byte
# _AS7341_SP_HIGH_TH_L = const(                                                   \) #
#   0x86 Spectral measurement High Threshold low byte
# _AS7341_SP_HIGH_TH_H = const(                                                   \) #
#   0x87 Spectral measurement High Threshold low byte


# _AS7341_STATUS = const(                                                         \) #
#   0x93 Interrupt status registers. Indicates the occourance of an interrupt

# _AS7341_CH0_DATA_L = const(0x95) # ADC Channel Data
# _AS7341_CH0_DATA_H = const(0x96) # ADC Channel Data
# _AS7341_CH1_DATA_L = const(0x97) # ADC Channel Data
# _AS7341_CH1_DATA_H = const(0x98) # ADC Channel Data
# _AS7341_CH2_DATA_L = const(0x99) # ADC Channel Data
# _AS7341_CH2_DATA_H = const(0x9A) # ADC Channel Data
# _AS7341_CH3_DATA_L = const(0x9B) # ADC Channel Data
# _AS7341_CH3_DATA_H = const(0x9C) # ADC Channel Data
# _AS7341_CH4_DATA_L = const(0x9D) # ADC Channel Data
# _AS7341_CH4_DATA_H = const(0x9E) # ADC Channel Data
# _AS7341_CH5_DATA_L = const(0x9F) # ADC Channel Data
# _AS7341_CH5_DATA_H = const(0xA0) # ADC Channel Data
# _AS7341_STATUS2 = const(0xA3) # Measurement status flags; saturation, validity
# _AS7341_STATUS3 = const(                                                        \) #
#   0xA4 Spectral interrupt source, high or low threshold


# _AS7341_CFG0 = const(                                                           \) #
#   0xA9 Sets Low power mode, Register bank, and Trigger lengthening
# _AS7341_CFG1 = const(0xAA) # Controls ADC Gain


# _AS7341_CFG9 = const(                                                           \) #
#   0xB2 Enables flicker detection and smux command completion system
# interrupts

# _AS7341_CFG12 = const(                                                          \) #
#   0xB5 Spectral threshold channel for interrupts, persistence and auto-gain
# _AS7341_PERS = const(                                                           \) #
#   0xBD Number of measurement cycles outside thresholds to trigger an
# interupt
# _AS7341_GPIO2 = const(                                                          \) #
#   0xBE GPIO Settings and status: polarity, direction, sets output, reads
# input
# _AS7341_ASTEP_L = const(0xCA) # Integration step size ow byte
# _AS7341_ASTEP_H = const(0xCB) # Integration step size high byte


# _AS7341_FD_TIME1 = const(0xD8) # Flicker detection integration time low byte
# _AS7341_FD_TIME2 = const(0xDA) # Flicker detection gain and high nibble

# _AS7341_FD_STATUS = const(                                                      \) #
#   0xDB Flicker detection status; measurement valid, saturation, flicker
# type
# _AS7341_INTENAB = const(0xF9) # Enables individual interrupt types
# _AS7341_CONTROL = const(0xFA) # Auto-zero, fifo clear, clear SAI active


# _AS7341_SPECTRAL_INT_HIGH_MSK = const(                                          \) #
#   0b00100000 bitmask to check for a high threshold interrupt
# _AS7341_SPECTRAL_INT_LOW_MSK = const(                                           \) #
#   0b00010000 bitmask to check for a low threshold interrupt

# /**
#  * @brief Allowable gain multipliers for `setGain`
#  *
#  */
# typedef enum {
#   AS7341_GAIN_0_5X,
#   AS7341_GAIN_1X,
#   AS7341_GAIN_2X,
#   AS7341_GAIN_4X,
#   AS7341_GAIN_8X,
#   AS7341_GAIN_16X,
#   AS7341_GAIN_32X,
#   AS7341_GAIN_64X,
#   AS7341_GAIN_128X,
#   AS7341_GAIN_256X,
#   AS7341_GAIN_512X,
# } as7341_gain_t;

# /**
#  * @brief ADC Channel specifiers for configuration
#  *
#  */
# typedef enum {
#   AS7341_CHANNEL_0,
#   AS7341_CHANNEL_1,
#   AS7341_CHANNEL_2,
#   AS7341_CHANNEL_3,
#   AS7341_CHANNEL_4,
#   AS7341_CHANNEL_5,
# } as7341_channel_t;

# /**
#  * @brief The number of measurement cycles with spectral data outside of a
#  * threshold required to trigger an interrupt
#  *
#  */
# typedef enum {
#   AS7341_INT_COUNT_ALL, 0
#   AS7341_INT_COUNT_1, 1
#   AS7341_INT_COUNT_2, 2
#   AS7341_INT_COUNT_3, 3
#   AS7341_INT_COUNT_5, 4
#   AS7341_INT_COUNT_10, 5
#   AS7341_INT_COUNT_15, 6
#   AS7341_INT_COUNT_20, 7
#   AS7341_INT_COUNT_25, 8
#   AS7341_INT_COUNT_30, 9
#   AS7341_INT_COUNT_35, 10
#   AS7341_INT_COUNT_40, 11
#   AS7341_INT_COUNT_45, 12
#   AS7341_INT_COUNT_50, 13
#   AS7341_INT_COUNT_55, 14
#   AS7341_INT_COUNT_60, 15
# } as7341_int_cycle_count_t;

# class Adafruit_AS7341;

# /*!
#  *    @brief  Class that stores state and functions for interacting with
#  *            the AS7341 11-Channel Spectral Sensor
#  */
# class Adafruit_AS7341 {
# public:
#   Adafruit_AS7341();
#   ~Adafruit_AS7341();

#   bool begin(uint8_t i2c_addr = AS7341_I2CADDR_DEFAULT, TwoWire *wire = &Wire,
#              int32_t sensor_id = 0);

#   bool setASTEP(uint16_t astep_value);
#   bool setATIME(uint8_t atime_value);
#   bool setGain(as7341_gain_t gain_value);

#   uint16_t readChannel(as7341_channel_t channel);

#   void readRawValuesMode1(void);
#   void readRawValuesMode2(void);

#   void flickerDetection(void); // merge with 1k
#   void flickerDetection1K(void);

#   void FDConfig(void);

#   int8_t getFlickerDetectStatus(void);

#   void F1F4_Clear_NIR(void);
#   void F5F8_Clear_NIR(void);

#   void powerEnable(bool enable_power);
#   bool enableSpectralMeasurement(bool enable_measurement);

#   bool setHighThreshold(int16_t high_threshold);
#   bool setLowThreshold(int16_t low_threshold);

#   int16_t getHighThreshold(void);
#   int16_t getLowThreshold(void);

#   bool enableSpectralINT(bool enable_int);
#   bool setAPERS(as7341_int_cycle_count_t cycle_count);
#   bool setSpectralThresholdChannel(as7341_channel_t channel);

#   uint8_t getInterruptStatus(void);
#   bool clearInterruptStatus(void);

#   bool spectralInterruptTriggered(void);
#   uint8_t spectralINTSource(void);
#   bool spectralLowTriggered(void);
#   bool spectralHighTriggered(void);

#   bool enableLED(bool enable_led);

#   bool setLEDCurrent(uint8_t led_current);

#   bool getIsDataReady();
#   bool setBank(bool low); // low true gives access to 0x60 to 0x74

# protected:
#   virtual bool _init(int32_t sensor_id);
#   uint8_t last_spectral_int_source =
#       0; The value of the last reading of the spectral interrupt source
# register

#   Adafruit_I2CDevice *i2c_dev = NULL; Pointer to I2C bus interface

# private:
#   void enableSMUX(void);
#   void SmuxConfigRAM(void);
#   void writeRegister(byte addr, byte val);
# };

# #endif
