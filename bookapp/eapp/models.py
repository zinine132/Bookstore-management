from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from eapp import app, db

class UserRoleEnum(UserEnum):
    KHACH_HANG = 1
    NHAN_VIEN = 2
    QUAN_LY = 3
    QUAN_TRI = 4

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

sach_the_loai = db.Table('sach_the_loai', Column('sach_id', Integer, ForeignKey('sach.id'), primary_key=True), Column('the_loai_id',  Integer,ForeignKey('the_loai.id'), primary_key=True))

tac_gia_sach = db.Table('tac_gia_sach', Column('tac_gia_id', Integer, ForeignKey('tac_gia.id'), primary_key=True), Column('sach_id', Integer, ForeignKey('sach.id'), primary_key=True))

class NguoiDung(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    user_name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.KHACH_HANG)

class KhachHang(NguoiDung):
    __tablename__ = "khach_hang"
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    phone = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    don_dats = relationship("DonDatHang", backref='khach_hang', lazy=True)

class NhanVien(NguoiDung):
    __tablename__ = "nhan_vien"

    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    hoa_dons = relationship("HoaDon", backref='nhan_vien', lazy=True)

class QuanTri(NhanVien):
    __tablename__ = "quan_tri"

    id = Column(Integer, ForeignKey(NhanVien.id), primary_key=True)
    quy_dinhs = relationship("QuyDinh", backref='quan_tri', lazy=True)

class QuanLy(NhanVien):
    __tablename__ = "quan_ly"

    id = Column(Integer, ForeignKey(NhanVien.id), primary_key=True)
    phieu_nhap_sachs = relationship("PhieuNhapSach", backref='quan_ly', lazy=True)

class DonDatHang(BaseModel):
    __tablename__ = "don_dat_hang"

    create_date = Column(Date, default=datetime.now)
    total_amount = Column(Float, default=0)
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)

    thanh_toan = relationship("ThanhToan", backref='don_dat_hang', uselist=False, lazy=True)
    chi_tiet_don_hangs = relationship("ChiTietDonHang", backref='don_dat_hang', lazy=True)
    hoa_don = relationship("HoaDon", backref="don_dat_hang", uselist=False, lazy=True)

class ThanhToan(BaseModel):
    __tablename__ = "thanh_toan"

    pay_method = Column(String(50), nullable=False)
    total_amount = Column(Float, default=0)
    status = Column(String(50), nullable=False)

    don_dat_hang_id = Column(Integer, ForeignKey(DonDatHang.id), unique=True, nullable=False)

class Sach(BaseModel):
    __tablename__ = "sach"

    book_name = Column(String(200), nullable=False)
    price = Column(Float, default=0)
    quantity = Column(Integer, default=0)

    the_loais = relationship("TheLoai", secondary=sach_the_loai, back_populates="sachs", lazy=True)
    tac_gias = relationship("TacGia", secondary=tac_gia_sach, back_populates="sachs", lazy=True)

    chi_tiet_don_hangs = relationship("ChiTietDonHang", backref="sach", lazy=True)
    chi_tiet_hoa_dons = relationship("ChiTietHoaDon", backref="sach", lazy=True)
    chi_tiet_phieu_nhaps = relationship("ChiTietPhieuNhapSach", backref="sach", lazy=True)

class ChiTietDonHang(BaseModel):
    __tablename__ = "chi_tiet_don_hang"

    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    total_money = Column(Float, default=0)

    dot_dat_hang_id = Column(Integer, ForeignKey(DonDatHang.id), nullable=False)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)

class HoaDon(BaseModel):
    __tablename__ = "hoa_don"

    create_date = Column(Date, default=datetime.now)
    total_amount = Column(Float, default=0)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)

    chi_tiet_hoa_dons = relationship("ChiTietHoaDon", backref='hoa_don', lazy=True)
    don_dat_hang_id = Column(Integer, ForeignKey(DonDatHang.id), unique=True, nullable=True)

class ChiTietHoaDon(BaseModel):
    __tablename__ = "chi_tiet_hoa_don"

    quantity = Column(Integer, default=0)
    selling_price = Column(Float, default=0)

    hoa_don_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)

class PhieuNhapSach(BaseModel):
    __tablename__ = "phieu_nhap_sach"

    create_date = Column(Date, default=datetime.now)

    quan_ly_id = Column(Integer, ForeignKey(QuanLy.id), nullable=False)
    chi_tiet_phieu_nhaps = relationship('ChiTietPhieuNhapSach', backref='phieu_nhap_sach', uselist=False, lazy=True)

class ChiTietPhieuNhapSach(BaseModel):
    __tablename__ = "chi_tiet_phieu_nhap_sach"

    price_entry = Column(Float, default=0)
    quantity = Column(Integer, default=0)
    total_amount_entry = Column(Float, nullable=False)

    phieu_nhap_id = Column(Integer, ForeignKey(PhieuNhapSach.id), nullable=False)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)

class QuyDinh(BaseModel):
    __tablename__ = "quy_dinh"

    quantity_entry_min = Column(Integer, default=150)
    inventory_quantity_min = Column(Integer, default=300)
    cancer_time = Column(Integer, default=24)

    quan_tri_id = Column(Integer, ForeignKey(QuanTri.id), nullable=False)

class TheLoai(BaseModel):
    __tablename__ = "the_loai"

    category_name = Column(String(200), nullable=False)

    sachs = relationship("Sach", secondary=sach_the_loai, back_populates="the_loais", lazy=True)

class TacGia(BaseModel):
    __tablename__ = "tac_gia"

    author_name = Column(String(200), nullable=False)

    sachs = relationship("Sach", secondary=tac_gia_sach, back_populates="tac_gias", lazy=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        import hashlib

        admin = QuanTri(
            name="Quản trị viên",
            email="admin@nhasach.vn",
            user_name="admin",
            password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
            user_role=UserRoleEnum.QUAN_TRI,
        )
        db.session.add(admin)
        db.session.commit()

        tl1 = TheLoai(category_name="Văn học")
        tl2 = TheLoai(category_name="Kinh tế")
        tl3 = TheLoai(category_name="Công nghệ thông tin")
        db.session.add_all([tl1, tl2, tl3])

        tg1 = TacGia(author_name="Nguyễn Nhật Ánh")
        tg2 = TacGia(author_name="Dale Carnegie")
        db.session.add_all([tg1, tg2])
        db.session.commit()

        s1 = Sach(book_name="Mắt biếc", price=110000, quantity=50, the_loais=[tl1], tac_gias=[tg1])
        s2 = Sach(book_name="Đắc nhân tâm", price=86000, quantity=100, the_loais=[tl2], tac_gias=[tg2])
        db.session.add_all([s1, s2])

        qd = QuyDinh(
            quan_tri_id=admin.id,
            quantity_entry_min=150,
            inventory_quantity_min=300,
            cancer_time=24,
        )
        db.session.add(qd)
        db.session.commit()

