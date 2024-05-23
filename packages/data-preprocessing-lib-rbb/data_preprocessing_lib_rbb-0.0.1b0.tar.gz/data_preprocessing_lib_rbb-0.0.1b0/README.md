# Data Preprocessing Library

A comprehensive data preprocessing library in Python. This library provides various functions for data cleaning, transformation, and manipulation operations, designed to make your data preprocessing tasks easier and more efficient.

## Features

- **Handling Missing Values**: Mean, median, constant imputation, and deletion.
- **Outlier Detection and Correction**: IQR method with threshold.
- **Data Standardization and Normalization**: Min-Max and Standard normalization.
- **Text Cleaning and Manipulation**: Remove stopwords, lowercase conversion, punctuation removal, lemmatization (requires NLTK).
- **Feature Engineering**: Create new features from existing ones.
- **Data Type Conversion**: Convert to numeric, categorical, and datetime.
- **Encoding Categorical Data**: One-hot encoding and label encoding.
- **Date and Time Manipulation**: Extract date components, calculate date differences.

## Usage

**Here's an example of how to use the library:**

- # Load the data
    - data = pd.read_csv('synthetic_sample_data.csv')

- # Handling missing values
    - missing_handler = MissingValueHandler(strategy="mean")
    - data = missing_handler.fit_transform(data)

- # Outlier detection and correction
    - outlier_handler = OutlierHandler(method="iqr", threshold=1.5)
    - data = outlier_handler.fit_transform(data)

- # Data standardization
    - scaler = Scaler(method="standard")
    - data = scaler.fit_transform(data)

- # Text cleaning
    - text_cleaner = TextCleaner(remove_stopwords=True, lemmatize=True)
      - if 'Summary' in data.columns:
            data['Summary'] = data['Summary'].astype(str).apply(text_cleaner.clean)

- # Encoding categorical data
    - if 'Genre' in data.columns:
        data, _ = CategoricalEncoder.label_encode(data, 'Genre')
    - if 'Shooting Location' in data.columns:
        data, _ = CategoricalEncoder.one_hot_encode(data, 'Shooting Location')

  - # Date and time manipulation
      - if 'Release Date' in data.columns:
        data = DateTimeHandler.convert_to_datetime(data, 'Release Date', format='%d/%m/%Y')
        data = DateTimeHandler.extract_date_component(data, 'Release Date', 'year')

  - # Feature engineering
      - if 'Budget in USD' in data.columns and 'Awards' in data.columns:
            data = FeatureEngineer.add_difference(data, 'Budget in USD', 'Awards', 'Budget_Awards_Diff')
      - if 'Rating' in data.columns and 'Popular' in data.columns:
            data = FeatureEngineer.add_product(data, 'Rating', 'Popular', 'Rating_Times_Popular')

- # Data type conversion
    - if 'Rating' in data.columns:
        data = DataTypeConverter.to_numeric(data, 'Rating')
    - if 'Genre' in data.columns:
        data = DataTypeConverter.to_categorical(data, 'Genre')

    print(data.head())


## Licence

-   This project is licensed under the **MIT License**.

## Contact

- **Author**: Rafet Bartuğ Bartınlı
- **Email**: rafetbartug@gmail.com

## Installation

- To install the library, use the following command:

```bash
pip install data_preprocessing_lib_rbb
```

 # Veri Ön İşleme Kütüphanesi

Python'da bir veri ön işleme kütüphanesi. Bu kütüphane, veri temizleme, dönüştürme ve manipülasyon işlemleri için çeşitli fonksiyonlar sunar, veri ön işleme görevlerinizi daha kolay ve verimli hale getirmek için tasarlanmıştır.

## Özellikler

- **Handling Missing Values**: Ortalama, medyan, sabit değer ile doldurma ve silme.
- **Outlier Detection and Correction**:  IQR yöntemi ile eşik değer kullanarak aykırı değer tespiti ve düzeltilmesi.
- **Data Standardization and Normalization**: Min-Max ve Standart normalizasyon işlemleri.
- **Text Cleaning and Manipulation**: Durdurma kelimelerini çıkarma, küçük harfe çevirme, noktalama işaretlerini çıkarma, kelimeyi köküne indirgeme (NLTK kütüphanesinin kullanımını gerektirir).
- **Feature Engineering**:  Mevcut özelliklerden yeni özellikler oluşturma.
- **Data Type Conversion**: Sayısal, kategorik ve gün/saat dönüşümleri.
- **Encoding Categorical Data**: One-hot kodlama ve label kodlama.
- **Date and Time Manipulation**:  Tarih bileşenlerini çıkarma, tarih farklarını hesaplama.

## Kullanım

**Kütüphaneyi nasıl kullanacağınıza dair bir örnek:**

- # Veriyi yükle
    - data = pd.read_csv('synthetic_sample_data.csv')

- # Eksik değerlerin işlenmesi
    - missing_handler = MissingValueHandler(strategy="mean")
    - data = missing_handler.fit_transform(data)

- # Aykırı değerlerin tespiti ve düzeltilmesi
    - outlier_handler = OutlierHandler(method="iqr", threshold=1.5)
    - data = outlier_handler.fit_transform(data)

- # # Verinin standartlaştırılması
    - scaler = Scaler(method="standard")
    - data = scaler.fit_transform(data)

- # Metin temizleme
    - text_cleaner = TextCleaner(remove_stopwords=True, lemmatize=True)
      - if 'Summary' in data.columns:
            data['Summary'] = data['Summary'].astype(str).apply(text_cleaner.clean)

- # Kategorik verilerin kodlanması
    - if 'Genre' in data.columns:
        data, _ = CategoricalEncoder.label_encode(data, 'Genre')
    - if 'Shooting Location' in data.columns:
        data, _ = CategoricalEncoder.one_hot_encode(data, 'Shooting Location')

  - # Tarih ve zaman manipülasyonu
      - if 'Release Date' in data.columns:
        data = DateTimeHandler.convert_to_datetime(data, 'Release Date', format='%d/%m/%Y')
        data = DateTimeHandler.extract_date_component(data, 'Release Date', 'year')

  - # Özellik mühendisliği
      - if 'Budget in USD' in data.columns and 'Awards' in data.columns:
            data = FeatureEngineer.add_difference(data, 'Budget in USD', 'Awards', 'Budget_Awards_Diff')
      - if 'Rating' in data.columns and 'Popular' in data.columns:
            data = FeatureEngineer.add_product(data, 'Rating', 'Popular', 'Rating_Times_Popular')

  - # Veri tipi dönüşümü
      - if 'Rating' in data.columns:
          data = DataTypeConverter.to_numeric(data, 'Rating')
      - if 'Genre' in data.columns:
          data = DataTypeConverter.to_categorical(data, 'Genre')

      print(data.head())


## Lisans

- Bu proje **MIT Lisansı** altında lisanslanmıştır.

## İletişim

- **Author**: Rafet Bartuğ Bartınlı
- **Email**: rafetbartug@gmail.com

## Kurulum

- Kütüphaneyi kurmak için aşağıdaki komutu kullanın:

```bash
pip install data_preprocessing_lib_rbb
```
