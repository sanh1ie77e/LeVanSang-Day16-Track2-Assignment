# Hồ sơ nộp Lab 16

Đã chuẩn bị:
- `benchmark.py`: mã nguồn lấy từ máy CPU đã chạy.
- `benchmark_result.json`: kết quả thực lấy từ máy CPU.
- `evidence/benchmark_output.png`: ảnh terminal benchmark học viên gửi.
- `evidence/resource_usage.txt`: kết quả top, free -h, ip -s link đọc qua SSH sau benchmark.
- `terraform/`: mã nguồn Terraform và startup scripts; kèm lock file provider.
- `bao_cao.md`: báo cáo ngắn và bảng kết quả.

Đã bổ sung screenshot:
1. `evidence/resource_top.png`: lệnh top trên máy CPU.
2. `evidence/resource_memory.png`: free -h.
3. `evidence/resource_network.png`: ip -s link.
4. `evidence/billing_bills.png`: tổng quan Bills, kỳ tháng 10/2026, chụp 02/10/2026.
5. `evidence/billing_bills_accounts.png`: phần Charges by account của Bills.

Hạn chế của bằng chứng Billing: trang Management account chưa có dữ liệu; chưa thể hiện chi phí EC2/NAT hoặc chi phí riêng của tài khoản lab 800464327055. Báo cáo đã ghi rõ trạng thái này. Nếu người chấm cần chi phí thực tế theo dịch vụ, bổ sung ảnh sau khi dữ liệu cập nhật, lọc đúng tài khoản lab trong Cost Explorer; không cần giữ tài nguyên chạy để chờ cập nhật.

Nếu Billing chưa có dữ liệu, ghi rõ chưa cập nhật tại thời điểm chụp; không giữ hạ tầng chạy chỉ để chờ hóa đơn.

Không có private key, Kaggle credentials, AWS credentials, Terraform state hoặc thư mục provider .terraform trong bộ nộp bài. Cặp SSH key và state gốc vẫn được giữ ở thư mục triển khai để còn truy cập/destroy. Khi cần tái triển khai mã nguồn này, tạo SSH key mới với tên lab-key/lab-key.pub theo README.

`terraform_source.zip` chứa thư mục terraform theo mục mã nguồn trong README. ZIP tổng chứa toàn bộ hồ sơ và các ảnh đã thu; kiểm tra hạn chế Billing nêu trên trước khi nộp. Đã bổ sung evidence/terraform_destroy.png: Terraform xác nhận Destroy complete! Resources: 27 destroyed.

Dọn dẹp chỉ sau khi tải kết quả về và thu đủ bằng chứng: chạy terraform destroy tại đúng thư mục đã apply, đợi Destroy complete!, rồi kiểm tra EC2, NAT Gateway, ALB, EBS và Elastic IP của lab đã được xóa. Không xóa state trước khi destroy.
