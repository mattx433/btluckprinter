# btluckprinter
Quick and dirty GUI for Bluetooth thermal label printers that use the `com.luckprinter.sdk_new` SDK.

## Note
You probably want to use the considerably more polished [fichero-printer](https://github.com/0xMH/fichero-printer) repository.
The main difference is that this repository is designed to operate in the Bluetooth Classic mode.

## Usage instructions
1. Use your OS bluetooth settings to pair with the printer.
If the name ends in `_BLE`, wait a bit until it shows up without the BLE suffix.
2. Run the program.
3. Enter the serial port name in the Port box.
On Windows, you can get this by opening Device Manager.

On Linux, use `ls /dev/rfcomm*`. In most cases the default will work.
4. Select an image file.
JPG and PNG should work. Your image should be resized to:
- 96x207 (for 14x30mm paper)
- 96x276 (for 14x40mm paper)
- 96x344 (for 14x50mm paper)
5. Click Print.

## Known printers
Tested with:
- Fichero Label Printer - [Action PL](https://www.action.com/pl-pl/p/3212141/drukarka-etykiet-fichero/)

Seems identical, so will likely work:
- Silvercrest Label Printer - [blog post](https://atctwo.net/posts/2024/07/16/thermal-printer.html)
