// frontend/src/__tests__/LoginForm.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import LoginForm from '../YourForm'; // Đổi đường dẫn nếu component không nằm trong YourForm.js

describe('Login Form', () => {
  test('Hiện lỗi khi mật khẩu trống', () => {
    render(<LoginForm />);
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'user@example.com' },
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByText(/Mật khẩu không được trống/i)).toBeInTheDocument();
  });

  test('Đăng nhập thành công (mock)', () => {
    render(<LoginForm />);
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'user@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'abc123' },
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByText(/Login successful/i)).toBeInTheDocument(); // Cần bạn hiển thị câu này khi login thành công
  });
});
