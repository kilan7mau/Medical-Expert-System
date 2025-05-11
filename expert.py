import webbrowser
from experta import *
from prolog import HeThongChuanDoanYTe


if __name__ == "__main__":
    engine = HeThongChuanDoanYTe()
    engine.reset()
    engine.run()
    print("Các triệu chứng không khớp với bất kỳ bệnh nào trong cơ sở dữ liệu của tôi.")