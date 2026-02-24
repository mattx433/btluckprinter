from serial import Serial
import escpos.printer
import argparse

class D11sPrinter:
    def __init__(self, path):
        self.path = path
        self.device = None
    def open(self):
        self.device = Serial(self.path)
        self.device.timeout = 1
    def close(self):
        self.device.close()
    def get_model(self):
        self.device.write(b"\x10\xFF\x20\xF0")
        return self.device.read(32)
    def get_version(self):
        self.device.write(b"\x10\xFF\x20\xF1")
        return self.device.read(32)
    def get_serial(self):
        self.device.write(b"\x10\xFF\x20\xF2")
        return self.device.read(32)
    def get_battery(self):
        self.device.write(b"\x10\xFF\x50\xF1")
        return self.device.read(2)[1]
    def get_paper(self):
        self.device.write(b"\x10\xFF\x40")
        return self.device.read(1)[0] == 0x00
    def get_shutdown_time(self):
        self.device.write(b"\x10\xFF\x13")
        return self.device.read(2)[1]
    def get_density(self):
        self.device.write(b"\x10\xFF\x11")
        # TODO: interpret
        return self.device.read(3)
    def set_density(self, density = 0x01):
        # 0 = light, 1 = medium, 2 = thick
        self.device.write(b"\x10\xff\x10\x00" + bytes([density]))
        assert self.device.read(2) == b"OK"
    def set_label_paper(self):
        # TODO: add parameter (fourth byte)
        self.device.write(b"\x10\xff\x84\x00")
        self.device.flush()
        self.device.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        assert self.device.read(2) == b"OK"
    def enable_printer(self):
        self.device.write(b"\x10\xFF\xFE\x01")
    def stop_print_job(self):
        self.device.write(b"\x10\xFF\xFE\x45")
    def feed_label(self):
        self.device.write(b"\x1D\x0C")
    def finish(self):
        self.feed_label()
        self.stop_print_job()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="luckprinter.py", description="Print images with a Fichero printer")
    parser.add_argument("filename")
    parser.add_argument("-p", "--port", default="/dev/rfcomm0")
    args = parser.parse_args()
    printer = D11sPrinter(args.port)
    printer.open()
    assert printer.get_paper()
    printer.set_density()
    printer.set_label_paper()
    printer.enable_printer()
    dummy = escpos.printer.Dummy(profile="default")
    dummy.image(args.filename)
    printer.device.write(dummy.output)
    printer.finish()
    printer.device.flush()
