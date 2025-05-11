import webbrowser

def multi_input(input_str, options=[]):
    print(input_str)
    choice = None
    options.append("không có")
    while choice is None:
        print("0) không có")
        for i in range(len(options) - 1):
            print(f"{i + 1}) {options[i]}")
        print("Lựa chọn của bạn: ", end='')
        try:
            choice = [int(x) - 1 for x in input().split()]
            for x in choice:
                if x >= len(options):
                    raise ValueError("Giá trị không hợp lệ")
                if x == -1 and len(choice) > 1:
                    raise ValueError("Không thể chọn 'không có' cùng với các giá trị khác")
        except Exception as e:
            print("Nhập không hợp lệ. Vui lòng thử lại")
            choice = None
    return [options[i] for i in choice]

def yes_no(input_str):
    input_str += " (có/không): "
    ans = None
    while ans is None:
        ans = input(input_str).lower()
        if ans == "c" or ans == "có" or ans == "co":
            return "có"
        elif ans == "k" or ans == "không" or ans == "khong":
            return "không"
        else:
            ans = None

def suggest_disease(disease, symptoms):
    print(f"\nBạn có thể đang mắc bệnh {disease}")
    symptoms = '- ' + '\n - '.join(symptoms)
    print(f"Kết luận này dựa trên các triệu chứng của bạn trong số sau đây:\n {symptoms}")
    open_doc = yes_no(f"\nBạn có muốn biết thêm về bệnh {disease} không?")
    if open_doc == "có":
        webbrowser.open(f"Treatment/html/{disease}.html", new=2)
    exit(0)