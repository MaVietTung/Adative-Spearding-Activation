# Book Recommender System

Bài tập lớn môn Hệ gợi ý.

<u>Đề tài</u>: Gợi ý sách.

## Introduction 

Với đề tài về gợi ý sách, nhóm sử dụng phương pháp **Adative Spreading Activation**, chi tiết của thuật toán được 
trình bày trong [paper](https://link.springer.com/chapter/10.1007/11546924_10) và báo cáo của nhóm.
Để đánh giá hiệu quả của phương pháp này, hai bộ dữ liệu được sử dụng là 
[Book Crossing](http://www2.informatik.uni-freiburg.de/~cziegler/BX/) và [Goodbook](https://www.kaggle.com/zygmunt/goodbooks-10k).
Hệ thống được triển khai dưới dạng một api service giúp kiểm tra, đánh giá và sử dụng dễ dàng hơn.

## Setup 

Project được lưu trữ trên github tại nhánh develop [link](https://github.com/MaVietTung/Adative-Spearding-Activation/tree/develop)  
Để tải xuống mã nguồn, sử dụng lệnh:
```
$ git clone -b develop https://github.com/MaVietTung/Adative-Spearding-Activation.git
```

Do số lượng user, sách và rating là rất lớn, thực hiện thêm một bước lưu dữ liệu thành nhiều file json.
Mỗi file là một góc nhìn khác nhau về bộ dữ liệu như góc nhìn theo từng user, theo từng book,... Điều này 
giúp tăng tốc độ truy xuất đến từng phần phần tử.
```
$ python prepare_data.py
```

## Run application  

```
$ python main.py -d <DATASET>
```
Hệ thống chạy trên [localhost:8096](http://localhost:8096)
> Optional:
> * -d, --data: Chỉ định bộ dữ liệu được sử dụng. ```BX``` (BookCrossing) hoặc ```GB``` (GoodBook). Mặc định là ```BX```.

Ví dụ: Để chạy chương trình với bộ dữ liệu GoodBook:
```
$ python main.py -d GB
```

## Usage 

Hệ thống được triển khai với 5 api:

### Train 

Tính toán ma trận độ tương đồng giữa các user.  

**Note**:
* Để tính toán ma trận độ tương đồng, hệ thống cần chạy liên tục 14 giờ (với bộ BookCrossing)
và 12 giờ (với bộ GoodBook).
* Ma trận độ tương đồng đã tính toán được lưu tại
[BookCrossing](https://drive.google.com/file/d/1-AIrktweFx0FJHRDA-sIFtaezwgJljJ3/view?usp=sharing)
và [GoodBook](https://drive.google.com/file/d/1V-FMQwtlRxkQwtcXBatN2M5ZmDKq0O_F/view?usp=sharing).
* Có thể tải xuống ma trận độ tương đồng và lưu với tên ***result_train_similarities.json*** trong thư mục **data_matrix_similarities** của bộ dữ liệu tương ứng
để dùng cho qua trình dự đoán, gợi ý và đánh giá.

> GET /train
> 
> Return
> * ```time```: Thời gian tính toán 

### Predict rate

Dự đoán rating của user cho một cuốn sách.

> POST /predict  
> 
> Body
> * ```user```: User ID
> * ```book```: Book ID
> 
> Return
> * ```predicted```: Rating dự đoán
> * ```time```: Thời gian dự đoán 

### Recommend 

Gợi ý ra top 10 cuốn sách mà user có thể sẽ quan tâm. 

> POST /recommend
> 
> Body
> * ```user```: User ID
> 
> Return
> * ```recommend```: Danh sách các cuốn sách được gợi ý
> * ```time```: Thời gian gợi ý

### Evaluation Error 

Đánh giá hiệu quả của việc dự đoán rating bằng việc so sánh rating dự đoán với rating thực.  
Sử dụng 2 chỉ số đo tỉ lệ lỗi là MAE và RMSE.

> GET /eval_error
> 
> Return
> * ```MAE```: Mean Absolute Error
> * ```RMSE```: Root Mean Square Error
> * ```predicted_ratio```: Tỷ lệ dự đoán được
> * ```time```: Thời gian đánh giá

### Evaluation 

Đánh giá hiệu quả của việc gợi ý. Sử dụng các độ đo Precision, Recall, F1 score và Rank score.  
Được tính trung bình trên 1 số lượng user được chọn ngẫu nhiên từ tập test.

> POST /evaluate
> 
> Body
> * ```n_samples```: Số lượng user để tính trung bình
> 
> Return
> * ```precision```: Precision trung bình 
> * ```recall```: Recall trung bình
> * ```f1_score```: F1 score trung bình 
> * ```rankscore```: Rank score trung bình
> * ```time```: Thời gian đánh giá 
