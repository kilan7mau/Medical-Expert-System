import pandas as pd

# Dữ liệu đã dịch sang tiếng Việt
data = [
    {"Disease": "Đái tháo đường", "serial number": 1, "Symptoms": "Khát nước tăng\nĐi tiểu thường xuyên\nĐói quá mức\nSụt cân không rõ nguyên nhân\nMệt mỏi\nCáu gắt\nMờ mắt\nVết thương lâu lành\nNhiễm trùng thường xuyên, như nhiễm trùng nướu hoặc da"},
    {"Disease": "Xơ vữa động mạch vành^Bệnh tim mạch vành", "serial number": 2, "Symptoms": "Đau ngực\nCảm giác nặng hoặc tức ở giữa ngực, có thể lan ra cánh tay, cổ, hàm, lưng hoặc dạ dày\nCảm giác nóng rát\nĐau ở cánh tay hoặc vai\nKhó thở\nĐổ mồ hôi\nChóng mặt\nMệt mỏi"},
    {"Disease": "Viêm phổi", "serial number": 3, "Symptoms": "Sốt\nĐổ mồ hôi hoặc ớn lạnh\nKhó thở khi thực hiện các hoạt động bình thường hoặc ngay cả khi nghỉ ngơi\nThở nhanh\nHo ngày càng nặng, có thể kèm đờm màu vàng/xanh hoặc có máu\nĐau ngực khi thở hoặc ho – do viêm màng phổi\nBuồn nôn\nTiêu chảy\nNôn mửa"},
    {"Disease": "Hen suyễn", "serial number": 4, "Symptoms": "Khó thở\nTức ngực hoặc đau ngực\nKhó ngủ do khó thở, ho hoặc thở khò khè\nTiếng rít hoặc khò khè khi thở ra (thở khò khè là dấu hiệu phổ biến của hen suyễn ở trẻ em)\nCác cơn ho hoặc thở khò khè trở nặng do virus đường hô hấp, như cảm lạnh hoặc cúm"},
    {"Disease": "Thiếu máu", "serial number": 5, "Symptoms": "Mệt mỏi\nYếu sức\nDa nhợt nhạt hoặc vàng\nNhịp tim không đều\nKhó thở\nChóng mặt hoặc choáng váng\nĐau ngực\nTay chân lạnh\nĐau đầu"},
    {"Disease": "Suy giáp", "serial number": 6, "Symptoms": "Mệt mỏi\nTrầm cảm\nTáo bón\nCảm giác lạnh\nDa khô\nTăng cân\nYếu cơ\nGiảm tiết mồ hôi\nNhịp tim chậm\nĐau và cứng khớp\nTóc khô, thưa\nKhó thụ thai hoặc thay đổi kinh nguyệt\nKhàn giọng (thay đổi giọng bất thường)"},
    {"Disease": "Hội chứng suy giảm miễn dịch mắc phải^HIV", "serial number": 7, "Symptoms": "Sốt\nĐau đầu\nĐau cơ và đau khớp\nPhát ban\nĐau họng và loét miệng đau\nSưng hạch bạch huyết, chủ yếu ở cổ\nTiêu chảy\nSụt cân\nHo\nĐổ mồ hôi đêm"},
    {"Disease": "Mất nước", "serial number": 8, "Symptoms": "Khát nước cực độ\nĐi tiểu ít hơn\nNước tiểu sẫm màu\nMệt mỏi\nChóng mặt\nKhô miệng\nLờ đờ"},
    {"Disease": "Béo phì", "serial number": 9, "Symptoms": "Khó thở hoặc thở ngắn\nTăng tiết mồ hôi\nNgáy\nKhông thể đối phó với hoạt động thể chất đột ngột\nCảm thấy rất mệt mỏi mỗi ngày\nĐau lưng và khớp\nThiếu tự tin và lòng tự trọng\nCảm giác bị cô lập"},
    {"Disease": "Viêm khớp", "serial number": 10, "Symptoms": "Đau khớp\nCứng khớp\nSưng khớp\nĐỏ da quanh khớp\nGiảm phạm vi chuyển động\nCảm thấy mệt mỏi\nChán ăn"},
    {"Disease": "Viêm phế quản", "serial number": 11, "Symptoms": "Ho dai dẳng, có thể kèm đờm màu vàng xám\nThở khò khè\nSốt nhẹ và ớn lạnh\nCảm giác tức ngực\nĐau họng\nĐau nhức cơ thể\nKhó thở\nĐau đầu\nNghẹt mũi và xoang"},
    {"Disease": "Viêm tụy", "serial number": 12, "Symptoms": "Đau bụng trên\nĐau bụng nặng hơn sau khi ăn\nSốt\nBuồn nôn\nNôn mửa\nSụt cân không chủ ý\nPhân có dầu, mùi hôi (phân mỡ)\nNhịp tim nhanh"},
    {"Disease": "Loét dạ dày", "serial number": 13, "Symptoms": "Đau rát dạ dày\nCảm giác đầy bụng, chướng bụng hoặc ợ hơi\nBuồn nôn nhẹ\nNôn mửa nghiêm trọng\nSụt cân\nĐau bụng – đau dữ dội, khu trú\nChán ăn"},
    {"Disease": "Viêm dạ dày", "serial number": 14, "Symptoms": "Đau nhức hoặc rát (khó tiêu) ở bụng trên, có thể nặng hơn hoặc giảm khi ăn\nBuồn nôn\nNôn mửa\nCảm giác đầy bụng sau khi ăn\nChướng bụng\nĐau bụng\nChán ăn và khó tiêu"},
    {"Disease": "Viêm gan", "serial number": 15, "Symptoms": "Mệt mỏi\nTriệu chứng giống cúm\nNước tiểu sẫm màu\nPhân nhạt màu\nĐau bụng\nChán ăn\nSụt cân không rõ nguyên nhân\nDa và mắt vàng, có thể là dấu hiệu của vàng da\nSốt"},
    {"Disease": "Cúm", "serial number": 16, "Symptoms": "Đau đầu\nĐau nhức cơ, đặc biệt ở lưng, cánh tay và chân\nSốt\nỚn lạnh và đổ mồ hôi\nĐau họng\nHo khan, dai dẳng\nYếu sức\nNghẹt mũi\nMệt mỏi và yếu sức"},
    {"Disease": "Lao", "serial number": 17, "Symptoms": "Ho kéo dài ba tuần trở lên\nHo ra máu\nĐau ngực, hoặc đau khi thở hoặc ho\nSụt cân không chủ ý\nMệt mỏi\nSốt\nĐổ mồ hôi đêm\nỚn lạnh\nChán ăn"},
    {"Disease": "Sốt rét", "serial number": 18, "Symptoms": "Sốt\nỚn lạnh\nĐau đầu\nBuồn nôn và nôn mửa\nĐổ mồ hôi\nĐau bụng\nHo\nYếu sức toàn thân\nĐau cơ dữ dội\nĐau lưng dưới"},
    {"Disease": "Sốt xuất huyết", "serial number": 19, "Symptoms": "Sốt cao đột ngột\nĐau đầu dữ dội\nĐau sau mắt\nĐau khớp và cơ nghiêm trọng\nMệt mỏi\nBuồn nôn\nNôn mửa\nPhát ban da, xuất hiện từ hai đến năm ngày sau khi bắt đầu sốt\nChảy máu nhẹ (như chảy máu mũi, chảy máu nướu, hoặc dễ bầm tím)"},
    {"Disease": "Virus Corona", "serial number": 20, "Symptoms": "Sốt\nHo\nKhó thở\nMệt mỏi\nỚn lạnh, đôi khi kèm run\nĐau nhức cơ thể\nĐau đầu\nĐau họng\nMất khứu giác hoặc vị giác\nBuồn nôn\nTiêu chảy"},
    {"Disease": "Viêm kết mạc", "serial number": 21, "Symptoms": "Cảm giác nóng rát ở mắt\nĐóng vảy ở mắt\nĐỏ mắt"},
    {"Disease": "Dị ứng mắt", "serial number": 22, "Symptoms": "Kích ứng ở mắt\nĐỏ mắt"},
]

# Tạo DataFrame
df = pd.DataFrame(data)

# Xuất ra file Excel
df.to_excel("symptoms_vi.xlsx", index=False, sheet_name="Symptoms")

print("File 'symptoms_vi.xlsx' đã được tạo thành công!")