# Báo cáo Lab 16 – AWS CPU LightGBM

Học viên: Lê Văn Sang. Ngày thực hành: 02/10/2026.

Lần thực hành nộp bài được triển khai lại tại `us-east-1` theo yêu cầu README, trong tài khoản lab `800464327055`. Kết quả và ảnh bên dưới thuộc lần chạy mới này; hạ tầng đã được destroy sau khi thu bằng chứng.

## Nhận xét (9 dòng)

1. Triển khai bằng Terraform trên AWS; máy CPU t3.medium được truy cập qua Bastion, còn NAT cung cấp đường tải thư viện và dữ liệu.
2. Sử dụng Credit Card Fraud Detection; chia dữ liệu có stratify và seed 42, với 182.276 dòng train, 45.569 dòng validation và 56.962 dòng test.
3. Thời gian đọc CSV là 2,469375 giây; thời gian huấn luyện LightGBM với 2 luồng CPU là 2,370892 giây.
4. Early stopping trên validation chọn best iteration = 1; test được giữ riêng và không dùng để chọn số vòng huấn luyện.
5. AUC-ROC đạt 0,939058 và Accuracy đạt 0,999210; Accuracy cao cần được xem cùng các chỉ số phát hiện gian lận vì dữ liệu mất cân bằng.
6. Tại ngưỡng xác suất 0,5, Precision = 0,773196, Recall = 0,765306 và F1 = 0,769231, cho thấy vẫn còn giao dịch gian lận bị bỏ sót.
7. Latency trung bình một dòng sau warm-up là 1,179898 ms; throughput khoảng 724.557,586043 dòng/giây khi đo batch 1.000 dòng, lặp 20 lần.
8. Bằng chứng tài nguyên được lấy sau benchmark nên phản ánh trạng thái sau khi chạy, không đại diện cho mức CPU/RAM cực đại trong training; số byte mạng là bộ đếm tích lũy.
9. Billing ban đầu ngày 02/10/2026 chưa có dữ liệu; ảnh bổ sung ngày 04/10/2026 cho thấy Month-to-date cost = USD 0,27 tại Management account 391016433737 và biểu đồ có EC2 - Other, EC2 Compute, Elastic Load Balancing, VPC, S3; chưa lọc riêng tài khoản lab 800464327055 hoặc region, nên không quy toàn bộ tổng này cho lần chạy us-east-1.

## Bảng benchmark

| Metric | Kết quả |
|---|---:|
| Thời gian load data | 2,469375 giây |
| Thời gian training | 2,370892 giây |
| Best iteration | 1 |
| AUC-ROC | 0,939058 |
| Accuracy | 0,999210 |
| F1-Score | 0,769231 |
| Precision | 0,773196 |
| Recall | 0,765306 |
| Inference latency (1 row) | 1,179898 ms |
| Inference throughput (batch 1.000 rows) | 724.557,586043 dòng/giây |

Kết quả đầy đủ và cấu hình đo nằm trong `benchmark_result.json`. Bằng chứng terminal benchmark nằm trong `evidence/benchmark_output.png`; số liệu tài nguyên chép từ các screenshot của máy mới nằm trong `evidence/resource_usage.txt`.

Ảnh tài nguyên: `evidence/resource_top.png`, `evidence/resource_memory.png`, `evidence/resource_network.png`. Hai ảnh Bills ngày 02/10/2026 được giữ làm bằng chứng ban đầu chưa có dữ liệu. Bổ sung ngày 04/10/2026: `evidence/billing_home_2026-10-04.png` (tổng tháng USD 0,27), `evidence/billing_services_2026-10-04.png` (biểu đồ theo dịch vụ) và `evidence/billing_trends_2026-10-04.png` (phần cuối dashboard). Các ảnh chưa hiển thị số tiền riêng NAT Gateway hoặc lọc tài khoản lab; tổng dashboard là chi phí tháng đến hiện tại, không phải bằng chứng đã thanh toán.

## Dọn dẹp

Terraform báo `Destroy complete! Resources: 27 destroyed.` trong thư mục triển khai trên laptop. Screenshot: `evidence/terraform_destroy.png`. Đây là xác nhận Terraform đã xóa các tài nguyên do state của lần triển khai này quản lý; không phải kiểm kê toàn bộ tài khoản AWS.
