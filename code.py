from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QUrl
import sys, os, json

class MainMenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("TRUEMOOD-MENU.ui", self)
        self.setWindowTitle("Main Menu")
        self.setFixedSize(1150, 750)
        self.player = QMediaPlayer()

        self.init_files()
        self.load_mode()

        self.findChild(QtWidgets.QPushButton, "switchmode").clicked.connect(self.toggle_mode)
        self.findChild(QtWidgets.QPushButton, "logoutButton").clicked.connect(self.logout)
        self.findChild(QtWidgets.QPushButton, "changeAvatarButton").clicked.connect(self.change_avatar)
        self.findChild(QtWidgets.QPushButton, "likeButton").clicked.connect(self.go_to_liked_songs)

        self.findChild(QtWidgets.QPushButton, "playjumpingmachine").clicked.connect(self.play_music_jump)
        self.findChild(QtWidgets.QPushButton, "playButton2").clicked.connect(self.switch_to_page)
        self.findChild(QtWidgets.QPushButton, "playButton").clicked.connect(self.switch_to_stack2)
        self.findChild(QtWidgets.QPushButton, "pushButton").clicked.connect(self.switch_to_stack4)
        self.findChild(QtWidgets.QPushButton, "pushButton_2").clicked.connect(self.switch_to_stack5)
        self.findChild(QtWidgets.QPushButton, "pushButton_7").clicked.connect(self.switch_to_stack6)

        self.avatar_label = self.findChild(QtWidgets.QLabel, "avatarLabel")
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget_1")
        if not self.stacked_widget:
            print("Lỗi: Không tìm thấy StackedWidget_1! Kiểm tra lại file .ui")

        self.findChild(QtWidgets.QPushButton, "menuButton").clicked.connect(self.go_to_home)

        self.load_avatar()

    def play_music_jump(self):
        url = QUrl.fromLocalFile("jumpingmachine.mp3")
        self.player.setSource(url)
        self.player.play()
        print("🔊 Đang phát: jumpingmachine.mp3")

    def switch_to_stack5(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(4)  # Chuyển sang Stack 5
            print("🔄 Đã chuyển sang Stack 5 (Negav)")
        else:
            print("⚠️ Lỗi: Không tìm thấy StackedWidget_1!")

    def switch_to_stack6(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(5)  # Chuyển sang Stack 6
            print("🔄 Đã chuyển sang Stack 6 (GreyD)")
        else:
            print("⚠️ Lỗi: Không tìm thấy StackedWidget_1!")

    def switch_to_stack4(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(3)  # Chuyển sang Stack 4
            print("🔄 Đã chuyển sang Stack 4!")
        else:
            print("⚠️ Lỗi: Không tìm thấy StackedWidget_1!")

    def switch_to_stack2(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(1)  # Chuyển sang Stack 2
            print("🔄 Đã chuyển sang Stack 2!")
        else:
            print("⚠️ Lỗi: Không tìm thấy StackedWidget_1!")

    def switch_to_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_home(self):
        """Quay về Stack 1 khi bấm menuButton"""
        self.stacked_widget.setCurrentIndex(0)

    def go_to_liked_songs(self):
        """Chuyển đến Stack 4 (liked songs) khi bấm likeButton"""
        self.stacked_widget.setCurrentIndex(4)  # Đảm bảo nó nhảy đúng stack chứa label_like

    def init_files(self):
        if not os.path.exists("liked_songs.json"):
            with open("liked_songs.json", "w", encoding="utf-8") as f:
                json.dump([], f)
        if not os.path.exists("settings.json"):
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump({"dark_mode": False}, f)
        if not os.path.exists("avatar_path.txt"):
            with open("avatar_path.txt", "w", encoding="utf-8") as f:
                f.write("")

    def load_mode(self):
        with open("settings.json", "r") as f:
            settings = json.load(f)
            self.is_dark_mode = settings.get("dark_mode", False)
        self.apply_mode()

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        with open("settings.json", "w") as f:
            json.dump({"dark_mode": self.is_dark_mode}, f)
        self.apply_mode()

    def apply_mode(self):
        self.setStyleSheet("background-color: #2E2E2E; color: white;" if self.is_dark_mode else "background-color: white; color: black;")

    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def change_avatar(self):
        path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh đại diện", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            try:
                pixmap = QtGui.QPixmap(path)
                if pixmap.isNull():
                    raise ValueError("File ảnh không hợp lệ hoặc bị hỏng.")

                with open("avatar_path.txt", "w", encoding="utf-8") as f:
                    f.write(path)

                self.set_avatar(path)

            except Exception as e:
                print("Lỗi khi cập nhật avatar:", e)

    def load_avatar(self):
        try:
            with open("avatar_path.txt", "r", encoding="utf-8") as f:
                path = f.read().strip()
                if path and os.path.exists(path):
                    self.set_avatar(path)
        except Exception as e:
            print(f"Error loading avatar: {e}")

    def set_avatar(self, path):
        try:
            pixmap = QtGui.QPixmap(path).scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.avatar_label.setPixmap(pixmap)
        except Exception as e:
            print("Lỗi khi đặt avatar:", e)

    def add_song_to_liked(self, song_name, song_path):
        song_info = {"song_name": song_name, "song_path": song_path}

        with open("liked_songs.json", "r", encoding="utf-8") as f:
            try:
                liked_songs = json.load(f)
            except json.JSONDecodeError:
                liked_songs = []

        if isinstance(liked_songs, list) and not any(song.get("song_path") == song_info["song_path"] for song in liked_songs):
            liked_songs.append(song_info)
            with open("liked_songs.json", "w", encoding="utf-8") as f:
                json.dump(liked_songs, f, indent=4)
            self.show_message("✔️", f"Đã thêm {song_name} vào danh sách yêu thích💖")

    def show_message(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("TRUEMOOD.ui", self)
        self.findChild(QtWidgets.QPushButton, "pushButton").clicked.connect(self.login)  # Nút "Log In"
        self.findChild(QtWidgets.QPushButton, "pushButton_2").clicked.connect(self.open_register)  # Nút "Sign up"

    def login(self):
        username = self.findChild(QtWidgets.QLineEdit, "username").text()  # Trường nhập tên người dùng
        password = self.findChild(QtWidgets.QLineEdit, "password").text()  # Trường nhập mật khẩu

        try:
            with open("accounts.json", "r", encoding="utf-8") as f:
                accounts = json.load(f)
        except json.JSONDecodeError:
            accounts = []

        for acc in accounts:
            if acc["username"] == username and acc["password"] == password:
                print(f"Đăng nhập thành công với: {username}")
                self.main_menu_window = MainMenuWindow()
                self.main_menu_window.show()
                self.close()
                return

        self.show_message("❌", "Sai tên đăng nhập hoặc mật khẩu.")

    def open_register(self):
        self.register_window = RegisterWindow()  # Đã sửa thành RegisterWindow()
        self.register_window.show()
        self.close()

    def show_message(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.exec()

class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("REGISTER.ui", self)  # Đảm bảo bạn có file REGISTER.ui
        self.findChild(QtWidgets.QPushButton, "Login").clicked.connect(self.go_back)

    def go_back(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
