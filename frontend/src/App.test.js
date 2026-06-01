import { render, screen } from '@testing-library/react';
import App from './App';

test('renders plant disease app title', () => {
  render(<App />);
  const headingElement = screen.getByText(/plant disease detection/i);
  expect(headingElement).toBeInTheDocument();
});
