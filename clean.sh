#!/bin/bash

# Script untuk mencari dan menghapus semua direktori __pycache__
# dari direktori saat ini ke bawah (rekursif).

echo "Mencari dan menghapus folder __pycache__..."

# Cari semua direktori (-type d) dengan nama "__pycache__"
# dan jalankan 'rm -rf' pada setiap hasil yang ditemukan.
# Opsi -exec ... {} + lebih efisien daripada -exec ... \;
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Pembersihan __pycache__ selesai."