# Báo cáo Lab 16 – AWS CPU LightGBM

Học viên: Lê Văn Sang. Ngày thực hành: 02/10/2026.

Cấu hình Terraform nộp bài đặt region `ap-southeast-2` (Sydney), khác mặc định `us-east-1` của README. Bảng chi phí ước tính cho us-east-1 trong README không được dùng làm chi phí thực tế của lần triển khai này.

## Nhận xét (9 dòng)

1. Triển khai bằng Terraform trên AWS; máy CPU t3.medium được truy cập qua Bastion, còn NAT cung cấp đường tải thư viện và dữ liệu.
2. Sử dụng Credit Card Fraud Detection; chia dữ liệu có stratify và seed 42, với 182.276 dòng train, 45.569 dòng validation và 56.962 dòng test.
3. Thời gian đọc CSV là 2,216457 giây; thời gian huấn luyện LightGBM với 2 luồng CPU là 2,300053 giây.
4. Early stopping trên validation chọn best iteration = 1; test được giữ riêng và không dùng để chọn số vòng huấn luyện.
5. AUC-ROC đạt 0,939058 và Accuracy đạt 0,999210; Accuracy cao cần được xem cùng các chỉ số phát hiện gian lận vì dữ liệu mất cân bằng.
6. Tại ngưỡng xác suất 0,5, Precision = 0,773196, Recall = 0,765306 và F1 = 0,769231, cho thấy vẫn còn giao dịch gian lận bị bỏ sót.
7. Latency trung bình một dòng sau warm-up là 1,163818 ms; throughput khoảng 736.101,312272 dòng/giây khi đo batch 1.000 dòng, lặp 20 lần.
8. Bằng chứng tài nguyên được lấy sau benchmark nên phản ánh trạng thái sau khi chạy, không đại diện cho mức CPU/RAM cực đại trong training; số byte mạng là bộ đếm tích lũy.
9. Tại thời điểm chụp 19:43 ngày 02/10/2026 (GMT+7), Bills của Management account 391016433737 hiển thị “No data” và tổng tạm tính USD 0,00; chưa có chi phí riêng cho tài khoản lab 800464327055 nên không kết luận lab miễn phí hoặc ghi ước tính README thành phí thực tế.

## Bảng benchmark

| Metric | Kết quả |
|---|---:|
| Thời gian load data | 2,216457 giây |
| Thời gian training | 2,300053 giây |
| Best iteration | 1 |
| AUC-ROC | 0,939058 |
| Accuracy | 0,999210 |
| F1-Score | 0,769231 |
| Precision | 0,773196 |
| Recall | 0,765306 |
| Inference latency (1 row) | 1,163818 ms |
| Inference throughput (batch 1.000 rows) | 736.101,312272 dòng/giây |

Kết quả đầy đủ và cấu hình đo nằm trong `benchmark_result.json`. Bằng chứng terminal benchmark nằm trong `evidence/benchmark_output.png`; số liệu tài nguyên thực đọc qua SSH nằm trong `evidence/resource_usage.txt`.

Ảnh tài nguyên: `evidence/resource_top.png`, `evidence/resource_memory.png`, `evidence/resource_network.png`. Ảnh Bills gồm tổng quan `evidence/billing_bills.png` và phần Charges by account `evidence/billing_bills_accounts.png`. Cả hai ảnh Billing chưa có dữ liệu chi phí theo dịch vụ hoặc tài khoản; cần bổ sung khi AWS cập nhật nếu người chấm yêu cầu.

## Dọn dẹp

Terraform báo `Destroy complete! Resources: 27 destroyed.` trong thư mục triển khai trên laptop. Screenshot: `evidence/terraform_destroy.png`. Đây là xác nhận Terraform đã xóa các tài nguyên do state của lần triển khai này quản lý; không phải kiểm kê toàn bộ tài khoản AWS.
