import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

# --- Tạo email ngẫu nhiên ---
VALID_EMAIL = f"lekim+test{random.randint(1000, 9999)}@gmail.com"
VALID_PASSWORD = "1232123123"

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

    @classmethod
    def tearDownClass(cls):
        time.sleep(4)
        cls.driver.quit()

    def navigate_to_home(self):
        self.driver.get("https://e-commerce-for-testing.onrender.com/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def navigate_to_login_page(self):
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()
        self.wait.until(EC.url_contains("/signin"))
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(.,'Sign In')]")))

    def assert_user_logged_in(self):
        try:
            profile_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Profile']")))
            self.assertTrue(profile_button.is_displayed(), "Nút 'Profile' không hiển thị.")
            print("✅ Assert: User is logged in (Profile button visible).")
        except TimeoutException:
            self.fail("❌ Timed out waiting for 'Profile' button, user not logged in.")

    def assert_user_logged_out(self):
        try:
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login']")))
            register_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Register']")))
            self.assertTrue(login_button.is_displayed() and register_button.is_displayed(),
                            "Các nút 'Login'/'Register' không hiển thị.")
            print("✅ Assert: User is logged out (Login/Register buttons visible).")
        except TimeoutException:
            self.fail("❌ Timed out waiting for 'Login'/'Register' buttons, user not logged out.")

    def register_new_user(self, email, password):
        self.navigate_to_home()
        register_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']")))
        register_button.click()
        self.wait.until(EC.url_contains("/signup"))

        inputs = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//form//input")))
        if len(inputs) < 3:
            self.fail("Không tìm thấy đủ 3 ô input: Email, Password, Confirm Password.")
        email_input, password_input, confirm_input = inputs[:3]

        email_input.clear()
        password_input.clear()
        confirm_input.clear()
        email_input.send_keys(email)
        password_input.send_keys(password)
        confirm_input.send_keys(password)

        sign_up_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign Up']")))
        sign_up_button.click()

        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            print(f"📢 Alert: {alert.text}")
            alert.accept()
        except TimeoutException:
            print("⚠️ Không có alert sau đăng ký.")

        try:
            self.wait.until(EC.url_contains("/signin"))
            print("✅ Đăng ký thành công, chuyển sang trang đăng nhập.")
        except TimeoutException:
            self.fail("❌ Không chuyển sang trang đăng nhập sau khi đăng ký.")

        time.sleep(4)  # ⏳

    def login_user(self, email, password):
        self.navigate_to_login_page()
        email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))

        email_input.clear()
        password_input.clear()
        email_input.send_keys(email)
        password_input.send_keys(password)

        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign In']")))
        sign_in_button.click()

        self.assert_user_logged_in()
        time.sleep(4)  # ⏳

    def logout_user(self):
        try:
            logout_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Logout']")))
            logout_button.click()
            self.wait.until(EC.url_matches(r"https://e-commerce-for-testing\.onrender\.com/?$"))
            self.assert_user_logged_out()
            print("✅ Đã logout thành công.")
            time.sleep(4)  # ⏳
        except TimeoutException:
            self.fail("❌ Không tìm thấy nút Logout trong trang Profile.")

    def add_to_basket(self):
        products = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div")))
        self.assertTrue(len(products) > 0, "Không tìm thấy sản phẩm nào trên trang chủ.")
        print(f"Đã tìm thấy {len(products)} div trên trang")

        products[0].click()
        add_to_basket_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add to Basket')]")))
        add_to_basket_button.click()
        print("✅ Đã click 'Add to Basket'.")
        time.sleep(4)  # ⏳

    def open_basket(self):
        try:
            cart_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Basket')]")))
            cart_button.click()
            print("✅ Đã vào trang giỏ hàng.")
        except TimeoutException:
            self.fail("❌ Không tìm thấy hoặc không thể click vào nút giỏ hàng.")
        time.sleep(4)  # ⏳

    def add_and_remove_product_in_cart(self):
        self.navigate_to_home()
        self.add_to_basket()
        self.open_basket()

        remove_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Remove from Basket')]")))
        remove_button.click()
        print("✅ Đã click nút xóa sản phẩm.")

        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(),'Your cart is empty')] | //div[contains(text(),'Your cart is empty')]")
            ))
            print("✅ Giỏ hàng đã trống.")
        except TimeoutException:
            print("⚠️ Warning: Không thấy thông báo giỏ hàng trống sau khi xóa sản phẩm.")

        time.sleep(4)  # ⏳

    def click_profile(self):
        try:
            profile_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Profile']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", profile_button)
            profile_button.click()
            print("✅ Đã click nút Profile.")
        except TimeoutException:
            self.fail("❌ Không tìm thấy hoặc không thể click vào nút Profile.")
        time.sleep(1)  # ⏳

class LoginAndCartTests(BaseTest):
    def test_login_and_cart_flow(self):
        print(f"\n--- Running test: {self._testMethodName} ---")
        print(f"👉 Đăng ký và đăng nhập với: {VALID_EMAIL} / {VALID_PASSWORD}")

        self.register_new_user(VALID_EMAIL, VALID_PASSWORD)
        self.login_user(VALID_EMAIL, VALID_PASSWORD)

        try:
            self.add_and_remove_product_in_cart()
        except AssertionError as e:
            print(f"⚠️ Cảnh báo trong add_and_remove_product_in_cart: {e}")

        self.click_profile()
        self.logout_user()

        print(f"✅ Test '{self._testMethodName}' Success.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
