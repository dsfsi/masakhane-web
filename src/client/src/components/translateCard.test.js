import { render, fireEvent } from '@testing-library/react';

import TranslateCard from './translateCard';

describe('TranslateCard', () => {
  test('renders TranslateCard component', () => {
    render(<TranslateCard />);
  });

  it('calls "onClick" prop on button click', () => {
    // Render new instance in every test to prevent leaking state
    const onClick = jest.fn();
    const { getByText } = render(<button onClick={onClick}>Translate</button>);
  
    fireEvent.click(getByText(/Translate/i));
    expect(onClick).toHaveBeenCalled();
  });

  it('calls "onChange" prop on textarea and updates value', () => {
    // Render new instance in every test to prevent leaking state
    const onChange = jest.fn();
    const { getByText } = render(<textarea placeholder="Enter Text" onChange={onChange}>Enter text here</textarea>);

    const input = getByText(/Enter text here/i);

    fireEvent.change(input, { target: { value: 'Good Day' } })
    expect(input.value).toBe('Good Day');
  });

  it('calls "onChange" prop on textarea', () => {
    const onChange = jest.fn();
    const { getByText } = render(<textarea placeholder="Enter Text" onChange={onChange}>Enter text here</textarea>);
  
    const input = getByText(/Enter text here/i);

    fireEvent.change(input, { target: { value: 'Good Day' } });
    expect(onChange).toHaveBeenCalledTimes(1);
  });

  it('updates translation textarea with translated text', () => {
    const onClick = jest.fn();
    const { findAllByText } = render(<textarea id="translation">...</textarea>);
    const { getByText } = render(<button onClick={onClick}>Translate</button>);
  
    const input = findAllByText(/.../i);
    const button = getByText(/Translate/i);

    fireEvent.click(button);
    expect(input.value).toBe('translated text');
  });
});