bluetooth.onBluetoothConnected(function () {
    status = true
})
bluetooth.onBluetoothDisconnected(function () {
    status = false
})
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    rx = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    basic.showString(rx)
})
let rx = ""
let status = false
bluetooth.setTransmitPower(7)
bluetooth.startUartService()
bluetooth.startTemperatureService()
status = false
basic.forever(function () {
    if (status) {
        basic.showString("C")
    } else {
        basic.showString("D")
    }
    bluetooth.uartWriteValue("Lichtstaerke", input.lightLevel())
    bluetooth.uartWriteValue("Temperatur", input.temperature())
    bluetooth.uartWriteValue("Beschleunigung", input.acceleration(Dimension.X))
    bluetooth.uartWriteValue("Lautstaerke", input.soundLevel())
    bluetooth.uartWriteValue("Drehung", input.rotation(Rotation.Pitch))
    basic.setLedColor(0x00ff00)
    basic.pause(100)
    basic.turnRgbLedOff()
    basic.pause(1000)
})
