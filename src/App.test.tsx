import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders enhanced web application', () => {
  render(<App />);
  const headerElement = screen.getByText(/Enhanced Web Application/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders dark mode toggle', () => {
  render(<App />);
  const toggleElement = screen.getByTestId('dark-mode-toggle');
  expect(toggleElement).toBeInTheDocument();
});

test('renders automation pipeline demo text', () => {
  render(<App />);
  const demoText = screen.getByText(/Automated enhancement pipeline demo/i);
  expect(demoText).toBeInTheDocument();
});
