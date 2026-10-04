# Hồ sơ nộp Lab 16

Đã chuẩn bị:
- `benchmark.py`: mã nguồn lấy từ máy CPU đã chạy.
- `benchmark_result.json`: kết quả thực lấy từ máy CPU.
- `evidence/benchmark_output.png`: ảnh terminal benchmark học viên gửi.
- `evidence/resource_usage.txt`: số liệu chép từ ảnh top, free -h, ip -s link sau benchmark trên máy us-east-1.
- `terraform/`: mã nguồn Terraform và startup scripts; kèm lock file provider.
- `bao_cao.md`: báo cáo ngắn và bảng kết quả.

Đã bổ sung screenshot:
1. `evidence/resource_top.png`: lệnh top trên máy CPU.
2. `evidence/resource_memory.png`: free -h.
3. `evidence/resource_network.png`: ip -s link.
4. `evidence/billing_bills.png`: tổng quan Bills, kỳ tháng 10/2026, chụp 02/10/2026.
5. `evidence/billing_bills_accounts.png`: phần Charges by account của Bills.

Cập nhật Billing ngày 04/10/2026: đã có tổng chi phí tháng đến hiện tại USD 0,27 và biểu đồ theo dịch vụ trong Management account. Ảnh mới chưa lọc riêng tài khoản lab 800464327055 hoặc us-east-1, cũng chưa có dòng phí NAT Gateway riêng; không coi tổng dashboard là chi phí riêng của lần benchmark hoặc bằng chứng đã thanh toán.

Giữ hai ảnh Bills ngày 02/10/2026 để đối chiếu trạng thái ban đầu chưa có dữ liệu. Ba ảnh bổ sung là `evidence/billing_home_2026-10-04.png`, `evidence/billing_services_2026-10-04.png`, `evidence/billing_trends_2026-10-04.png`.

Không có private key, Kaggle credentials, AWS credentials, Terraform state hoặc thư mục provider .terraform trong bộ nộp bài. Lần triển khai us-east-1 đã được destroy thành công; ảnh xác nhận nằm trong evidence/terraform_destroy.png. Khi cần tái triển khai mã nguồn này, tạo SSH key mới với tên lab-key/lab-key.pub theo README.

`terraform_source.zip` chứa thư mục terraform theo mục mã nguồn trong README. ZIP tổng chứa toàn bộ hồ sơ và các ảnh đã thu; kiểm tra hạn chế Billing nêu trên trước khi nộp. Đã bổ sung evidence/terraform_destroy.png: Terraform xác nhận Destroy complete! Resources: 27 destroyed.

Dọn dẹp chỉ sau khi tải kết quả về và thu đủ bằng chứng: chạy terraform destroy tại đúng thư mục đã apply, đợi Destroy complete!, rồi kiểm tra EC2, NAT Gateway, ALB, EBS và Elastic IP của lab đã được xóa. Không xóa state trước khi destroy.
## Xác nhận triển khai và tái chạy benchmark

Ảnh `evidence/terraform_apply.png` cho thấy Terraform tạo 27 tài nguyên và ALB có hostname thuộc us-east-1. Tên output `gpu_private_ip` được dùng chung trong mã gốc; lần chạy này dùng CPU vì enable_gpu=false.

Ở lần chạy us-east-1, kiểm tra import ban đầu thiếu LightGBM, nên đã cài thư viện thủ công trên Compute Node bằng các lệnh sau. Không khẳng định startup script đã tự cài thành công.

```bash
sudo apt-get update
sudo apt-get install -y python3-pip libgomp1 unzip
python3 -m pip install lightgbm scikit-learn pandas numpy kaggle
```

Để chạy benchmark, đặt `benchmark.py` và `creditcard.csv` trong cùng thư mục, rồi chạy `python3 benchmark.py`. Dataset tải từ Kaggle `mlg-ulb/creditcardfraud`, dùng credentials riêng của người chạy. Dataset và credentials không nằm trong bộ nộp.

Đo throughput dùng batch 1.000 dòng, báo cáo theo dòng/giây. Cảnh báo eval_set deprecated trong ảnh không làm lần chạy thất bại; phiên bản LightGBM thực tế là 4.7.0.
